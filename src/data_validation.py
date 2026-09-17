# -*- coding: utf-8 -*-
"""
Validation layer. Every function here inspects the normalized model produced
by data_loader and reports facts -- it never silently repairs the source.
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from src.data_loader import LoadedWorkbook, STANDARD_PL_LABEL_EN
from src import expense_mapping


@dataclass
class ValidationReport:
    reconciliation_by_year: pd.DataFrame
    duplicate_codes_by_year: dict
    unmapped_expense_accounts: list
    accounts_missing_amount: list
    label_issues: list
    structural_notes: list
    overall_status: str  # "PASS" or "REVIEW"


DATASET_COMPLETENESS_CAUTION_YEAR = 2017


def requires_completeness_caution_note(years) -> bool:
    """True whenever the dataset's one year with a known completeness
    caveat (see src.translations note.latest_body) is part of the
    selection -- that year's Facility Maintenance account was not tracked
    as its own line, so comparisons involving it should be read with that
    in mind."""
    return DATASET_COMPLETENESS_CAUTION_YEAR in set(years)


def account_status(accounts_df: pd.DataFrame, year: int, account_code_base: str) -> dict:
    """Distinguish 'not present in this year's data' from 'recorded as zero'.

    Returns {"status": "not_present" | "present", "amount": float | None}
    """
    match = accounts_df[
        (accounts_df["year"] == year) & (accounts_df["account_code_base"] == account_code_base)
    ]
    if match.empty:
        return {"status": "not_present", "amount": None}
    amount = float(match.iloc[0]["amount"])
    return {"status": "present", "amount": amount}


def build_reconciliation_table(loaded: LoadedWorkbook) -> pd.DataFrame:
    records = []
    for year, yt in sorted(loaded.year_totals.items()):
        records.append({
            "year": year,
            "total_revenue": yt.total_revenue,
            "official_total_expenses": yt.official_total_expenses,
            "total_expenses_from_rows": yt.total_expenses_from_rows,
            "expenses_subtotal_diff": yt.official_total_expenses - yt.total_expenses_from_rows,
            "official_pl": yt.official_pl_amount,
            "calculated_pl": yt.calculated_pl,
            "reconciliation_diff": yt.reconciliation_diff,
            "status": yt.reconciliation_status,
            "official_pl_label": yt.official_pl_label,
            "label_nonstandard": yt.label_nonstandard,
        })
    return pd.DataFrame(records)


def check_duplicate_codes_within_year(accounts_df: pd.DataFrame) -> dict:
    dupes = {}
    for year, grp in accounts_df.groupby("year"):
        counts = grp["account_code_base"].value_counts()
        dup_codes = counts[counts > 1]
        if len(dup_codes) > 0:
            dupes[int(year)] = dup_codes.to_dict()
    return dupes


def check_expense_mapping_coverage(accounts_df: pd.DataFrame) -> list:
    """Every expense account present anywhere in the dataset must have a
    management-group mapping. Returns list of unmapped account codes."""
    expense_codes = set(accounts_df.loc[accounts_df["account_type"] == "Expense", "account_code_base"].unique())
    mapped_codes = set(expense_mapping.ACCOUNT_TO_GROUP.keys())
    unmapped = sorted(expense_codes - mapped_codes)
    return unmapped


def check_numeric_validity(accounts_df: pd.DataFrame) -> list:
    issues = []
    bad = accounts_df[~accounts_df["amount"].apply(lambda x: isinstance(x, (int, float)))]
    for _, r in bad.iterrows():
        issues.append(f"[{r['year']}] {r['account_code']} {r['account_name_ar']!r}: non-numeric amount")
    return issues


def run_full_validation(loaded: LoadedWorkbook) -> ValidationReport:
    recon_df = build_reconciliation_table(loaded)
    dupes = check_duplicate_codes_within_year(loaded.accounts_df)
    unmapped = check_expense_mapping_coverage(loaded.accounts_df)
    numeric_issues = check_numeric_validity(loaded.accounts_df)

    label_issues = []
    for year, yt in sorted(loaded.year_totals.items()):
        if yt.label_nonstandard:
            label_issues.append(
                f"[{year}] Official Profit/Loss row uses a non-standard dataset label "
                f"{yt.official_pl_label_en!r} instead of {STANDARD_PL_LABEL_EN!r}. "
                "Classified as Profit/Loss based on its position in the dataset; "
                "original label preserved verbatim."
            )

    structural_notes = list(loaded.warnings)

    overall_status = "PASS"
    if (recon_df["status"] != "PASS").any():
        overall_status = "REVIEW"
    if dupes:
        overall_status = "REVIEW"
    if unmapped:
        overall_status = "REVIEW"
    if numeric_issues:
        overall_status = "REVIEW"

    return ValidationReport(
        reconciliation_by_year=recon_df,
        duplicate_codes_by_year=dupes,
        unmapped_expense_accounts=unmapped,
        accounts_missing_amount=numeric_issues,
        label_issues=label_issues,
        structural_notes=structural_notes,
        overall_status=overall_status,
    )
