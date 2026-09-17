# -*- coding: utf-8 -*-
"""
Loss/profit-driver decomposition: what does the data show about the change
in profit/loss between two selected years, broken into a revenue movement
and an expense movement, with the expense accounts that contributed most to
the expense movement ranked underneath.

Wording discipline: this module states what the numbers show ("the largest
numerical contributor to the increase in expenses was X"), never a
business-causality claim ("X proves inefficiency"). Any operational
interpretation is left to the reader.
"""

from dataclasses import dataclass

import pandas as pd

from src.data_loader import LoadedWorkbook
from src.financial_metrics import compare_years, YearComparison
from src.expense_analysis import cost_driver_ranking


REVENUE_LABEL_KEYS = {
    "4001": "revenue.workshop",
    "4002": "revenue.other",
    "4003": "revenue.settlement_discount",
}


def revenue_breakdown_by_year(loaded: LoadedWorkbook, years) -> pd.DataFrame:
    """One row per (year, revenue account) -- long format, source-traceable."""
    years = list(years)
    df = loaded.accounts_df[
        (loaded.accounts_df["year"].isin(years)) & (loaded.accounts_df["account_type"] == "Revenue")
    ].copy()
    return df.sort_values(["year", "account_code_base"])


def revenue_pivot_by_year(loaded: LoadedWorkbook, years) -> pd.DataFrame:
    """Wide pivot: rows=account, columns=year, values=amount. Missing years
    are NaN (not present), never assumed zero."""
    df = revenue_breakdown_by_year(loaded, years)
    return df.pivot_table(index=["account_code_base", "account_name_clean"], columns="year", values="amount", aggfunc="sum")


@dataclass
class PLDriverResult:
    comparison: YearComparison
    top_expense_contributors: pd.DataFrame


def pl_driver_analysis(loaded: LoadedWorkbook, base_year: int, comparison_year: int, top_n: int = 10) -> PLDriverResult:
    comparison = compare_years(loaded, base_year, comparison_year)
    top_contributors = cost_driver_ranking(loaded, base_year, comparison_year, top_n=top_n)
    return PLDriverResult(comparison=comparison, top_expense_contributors=top_contributors)
