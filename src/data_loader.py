# -*- coding: utf-8 -*-
"""
Loader for the synthetic workshop income-statement dataset.

This is a Portfolio demo. The data loaded here is 100% synthetic, generated
by scripts/generate_synthetic_data.py -- see that script's docstring and the
project README for the Data Privacy Statement. Nothing in this module reads
from, or depends on, any file outside this project directory.

Rules enforced here (same architecture as a production version would use):
- The dataset is opened read-only and is never written to by the app.
- Every number in the resulting model traces back to (account_code, year) in
  the source CSV.
- Revenue vs Expense classification uses the dataset's own account_type
  column (never inferred from amount sign).
- "Not present in a given year" is preserved as a distinct state from
  "recorded as zero" -- callers must not conflate the two.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ACCOUNTS_CSV_PATH = DATA_DIR / "synthetic_workshop_financial_data.csv"
OFFICIAL_TOTALS_CSV_PATH = DATA_DIR / "synthetic_official_totals.csv"

STANDARD_PL_LABEL_AR = "صافي الربح / الخسارة"
STANDARD_PL_LABEL_EN = "Net Profit / Loss"


@dataclass
class YearTotals:
    year: int
    total_revenue: float
    official_total_expenses: float
    total_expenses_from_rows: float
    official_pl_amount: float
    official_pl_label: str
    official_pl_label_en: str
    calculated_pl: float
    reconciliation_diff: float
    reconciliation_status: str
    label_nonstandard: bool


@dataclass
class LoadedWorkbook:
    """Named LoadedWorkbook (not LoadedDataset) to keep the same shape as
    every downstream analytical module expects -- this dashboard's data
    source changed (Excel workbook -> synthetic CSV), but the internal
    model it loads into did not."""
    accounts_df: pd.DataFrame          # long-format: one row per (year, account)
    year_totals: dict                  # year -> YearTotals
    warnings: list = field(default_factory=list)


def load_workbook_model() -> LoadedWorkbook:
    if not ACCOUNTS_CSV_PATH.exists() or not OFFICIAL_TOTALS_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Synthetic dataset not found at {ACCOUNTS_CSV_PATH} / {OFFICIAL_TOTALS_CSV_PATH}. "
            "Run scripts/generate_synthetic_data.py, or restore the data/ directory from the repo. "
            "STOP: do not proceed with placeholder or fallback data."
        )

    accounts_df = pd.read_csv(ACCOUNTS_CSV_PATH, dtype={"account_code": str})
    accounts_df["account_code_base"] = accounts_df["account_code"]
    accounts_df["account_name_clean"] = accounts_df.apply(
        lambda r: r["account_name_en"], axis=1
    )
    accounts_df["amount"] = accounts_df["amount"].astype(float)

    totals_df = pd.read_csv(OFFICIAL_TOTALS_CSV_PATH)

    warnings = []
    year_totals = {}

    for _, row in totals_df.iterrows():
        year = int(row["year"])
        year_accounts = accounts_df[accounts_df["year"] == year]
        total_revenue = float(year_accounts[year_accounts["account_type"] == "Revenue"]["amount"].sum())
        total_expenses_from_rows = float(year_accounts[year_accounts["account_type"] == "Expense"]["amount"].sum())

        official_total_expenses = float(row["official_total_expenses"])
        official_pl = float(row["official_pl_amount"])
        calculated_pl = total_revenue - total_expenses_from_rows
        recon_diff = official_pl - calculated_pl
        recon_status = "PASS" if abs(recon_diff) < 0.5 else "REVIEW"

        label_ar = str(row["official_pl_label_ar"])
        label_en = str(row["official_pl_label_en"])
        label_nonstandard = label_ar != STANDARD_PL_LABEL_AR

        year_totals[year] = YearTotals(
            year=year,
            total_revenue=total_revenue,
            official_total_expenses=official_total_expenses,
            total_expenses_from_rows=total_expenses_from_rows,
            official_pl_amount=official_pl,
            official_pl_label=label_ar,
            official_pl_label_en=label_en,
            calculated_pl=calculated_pl,
            reconciliation_diff=recon_diff,
            reconciliation_status=recon_status,
            label_nonstandard=label_nonstandard,
        )

    return LoadedWorkbook(accounts_df=accounts_df, year_totals=year_totals, warnings=warnings)


_CACHE: Optional[LoadedWorkbook] = None


def get_loaded_workbook(force_reload: bool = False) -> LoadedWorkbook:
    """Process-local cache. The Streamlit layer wraps this with
    st.cache_resource; kept plain here so it's usable from tests/scripts
    without Streamlit."""
    global _CACHE
    if _CACHE is None or force_reload:
        _CACHE = load_workbook_model()
    return _CACHE
