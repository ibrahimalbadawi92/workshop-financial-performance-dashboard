# -*- coding: utf-8 -*-
"""
Expense-side analysis: management-group aggregation, employee cost analysis,
top-N concentration, cost-driver (base year vs comparison year) analysis,
and heatmap-ready pivots. Every function preserves the missing-vs-zero
distinction and never merges raw source accounts.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from src.data_loader import LoadedWorkbook
from src import expense_mapping

# Comparison-status labels used by account_level_comparison() / cost_driver_ranking().
STATUS_NORMAL = "Normal"
STATUS_ZERO_BASE = "Zero Base / أساس صفري"
STATUS_NEW = "New / حساب جديد"
STATUS_NOT_PRESENT = "Not Present / غير موجود في المصدر"


def _expenses_for_year(accounts_df: pd.DataFrame, year: int) -> pd.DataFrame:
    return accounts_df[(accounts_df["year"] == year) & (accounts_df["account_type"] == "Expense")].copy()


def _expenses_for_years(accounts_df: pd.DataFrame, years) -> pd.DataFrame:
    years = list(years)
    return accounts_df[(accounts_df["year"].isin(years)) & (accounts_df["account_type"] == "Expense")].copy()


def with_management_group(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["group_key"] = df["account_code_base"].map(expense_mapping.ACCOUNT_TO_GROUP)
    df["group_name_ar"] = df["group_key"].map(lambda k: expense_mapping.GROUPS[k].name_ar if k else None)
    df["group_name_en"] = df["group_key"].map(lambda k: expense_mapping.GROUPS[k].name_en if k else None)
    return df


def top_n_expenses_for_year(loaded: LoadedWorkbook, year: int, n: int = 5) -> pd.DataFrame:
    df = _expenses_for_year(loaded.accounts_df, year)
    total = df["amount"].sum()
    df = df.sort_values("amount", ascending=False).head(n).copy()
    df["share_of_total_expenses"] = df["amount"] / total if total else np.nan
    return df[["account_code", "account_code_base", "account_name_clean", "amount", "share_of_total_expenses"]]


def expense_concentration(loaded: LoadedWorkbook, year: int) -> dict:
    df = _expenses_for_year(loaded.accounts_df, year).sort_values("amount", ascending=False)
    total = df["amount"].sum()
    top5 = df.head(5)["amount"].sum()
    top10 = df.head(10)["amount"].sum()
    return {
        "year": year,
        "total_expenses": total,
        "top5_amount": top5,
        "top5_share": top5 / total if total else None,
        "top10_amount": top10,
        "top10_share": top10 / total if total else None,
        "n_accounts": len(df),
    }


def group_totals_for_year(loaded: LoadedWorkbook, year: int) -> pd.DataFrame:
    df = with_management_group(_expenses_for_year(loaded.accounts_df, year))
    total = df["amount"].sum()
    grp = df.groupby(["group_key", "group_name_ar", "group_name_en"], as_index=False)["amount"].sum()
    grp["share_of_total_expenses"] = grp["amount"] / total if total else np.nan
    return grp.sort_values("amount", ascending=False)


def group_totals_for_years(loaded: LoadedWorkbook, years) -> pd.DataFrame:
    """Sum of each management group's amount across all selected years
    (cumulative total -- the financially meaningful aggregation for a
    multi-year selection)."""
    df = with_management_group(_expenses_for_years(loaded.accounts_df, years))
    total = df["amount"].sum()
    grp = df.groupby(["group_key", "group_name_ar", "group_name_en"], as_index=False)["amount"].sum()
    grp["share_of_total_expenses"] = grp["amount"] / total if total else np.nan
    return grp.sort_values("amount", ascending=False)


def top_n_expenses_for_years(loaded: LoadedWorkbook, years, n: int = 5) -> pd.DataFrame:
    df = _expenses_for_years(loaded.accounts_df, years)
    agg = df.groupby(["account_code_base", "account_name_clean"], as_index=False)["amount"].sum()
    total = agg["amount"].sum()
    agg = agg.sort_values("amount", ascending=False).head(n).copy()
    agg["share_of_total_expenses"] = agg["amount"] / total if total else np.nan
    return agg


def group_drilldown(loaded: LoadedWorkbook, year: int, group_key: str) -> pd.DataFrame:
    """Level 1 -> Level 2 drill-down: original source accounts within one
    management group, for one year."""
    df = with_management_group(_expenses_for_year(loaded.accounts_df, year))
    df = df[df["group_key"] == group_key]
    group_total = df["amount"].sum()
    df = df.copy()
    df["share_of_group"] = df["amount"] / group_total if group_total else np.nan
    return df[[
        "account_code", "account_code_base", "account_name_clean", "amount", "share_of_group",
    ]].sort_values("amount", ascending=False)


def group_drilldown_for_years(loaded: LoadedWorkbook, years, group_key: str) -> pd.DataFrame:
    """Same as group_drilldown but summed across multiple selected years."""
    df = with_management_group(_expenses_for_years(loaded.accounts_df, years))
    df = df[df["group_key"] == group_key]
    agg = df.groupby(["account_code_base", "account_name_clean"], as_index=False)["amount"].sum()
    group_total = agg["amount"].sum()
    agg["share_of_group"] = agg["amount"] / group_total if group_total else np.nan
    return agg.sort_values("amount", ascending=False)


# --------------------------------------------------------------------------
# Employee Cost analysis
# --------------------------------------------------------------------------

@dataclass
class EmployeeCostYearResult:
    year: int
    total_employee_costs: float
    total_expenses: float
    total_revenue: float
    employee_costs_pct_of_expenses: Optional[float]
    employee_costs_pct_of_revenue: Optional[float]
    subgroup_totals: pd.DataFrame  # subgroup_key, name_ar, name_en, amount, share_of_employee_costs


def employee_cost_analysis(loaded: LoadedWorkbook, year: int) -> EmployeeCostYearResult:
    df = with_management_group(_expenses_for_year(loaded.accounts_df, year))
    emp_df = df[df["group_key"] == "employee_costs"].copy()
    total_employee_costs = emp_df["amount"].sum()

    yt = loaded.year_totals[year]
    total_expenses = yt.official_total_expenses
    total_revenue = yt.total_revenue

    emp_df["subgroup_key"] = emp_df["account_code_base"].map(
        expense_mapping.get_employee_cost_subgroup_for_account
    )
    sub_meta = expense_mapping.EMPLOYEE_COST_SUBGROUPS
    emp_df["subgroup_name_ar"] = emp_df["subgroup_key"].map(lambda k: sub_meta[k]["name_ar"] if k else None)
    emp_df["subgroup_name_en"] = emp_df["subgroup_key"].map(lambda k: sub_meta[k]["name_en"] if k else None)

    subgroup_totals = emp_df.groupby(
        ["subgroup_key", "subgroup_name_ar", "subgroup_name_en"], as_index=False
    )["amount"].sum()
    subgroup_totals["share_of_employee_costs"] = (
        subgroup_totals["amount"] / total_employee_costs if total_employee_costs else np.nan
    )
    subgroup_totals = subgroup_totals.sort_values("amount", ascending=False)

    return EmployeeCostYearResult(
        year=year,
        total_employee_costs=total_employee_costs,
        total_expenses=total_expenses,
        total_revenue=total_revenue,
        employee_costs_pct_of_expenses=(total_employee_costs / total_expenses) if total_expenses else None,
        employee_costs_pct_of_revenue=(total_employee_costs / total_revenue) if total_revenue else None,
        subgroup_totals=subgroup_totals,
    )


def employee_cost_analysis_for_years(loaded: LoadedWorkbook, years) -> EmployeeCostYearResult:
    """Cumulative Employee Cost analysis across a multi-year selection:
    numerator and denominator are both summed across years first, then
    divided (ratio of aggregated totals), never an average of annual
    percentages."""
    years = list(years)
    df = with_management_group(_expenses_for_years(loaded.accounts_df, years))
    emp_df = df[df["group_key"] == "employee_costs"].copy()
    total_employee_costs = emp_df["amount"].sum()

    total_expenses = sum(loaded.year_totals[y].official_total_expenses for y in years)
    total_revenue = sum(loaded.year_totals[y].total_revenue for y in years)

    emp_df["subgroup_key"] = emp_df["account_code_base"].map(
        expense_mapping.get_employee_cost_subgroup_for_account
    )
    sub_meta = expense_mapping.EMPLOYEE_COST_SUBGROUPS
    emp_df["subgroup_name_ar"] = emp_df["subgroup_key"].map(lambda k: sub_meta[k]["name_ar"] if k else None)
    emp_df["subgroup_name_en"] = emp_df["subgroup_key"].map(lambda k: sub_meta[k]["name_en"] if k else None)

    subgroup_totals = emp_df.groupby(
        ["subgroup_key", "subgroup_name_ar", "subgroup_name_en"], as_index=False
    )["amount"].sum()
    subgroup_totals["share_of_employee_costs"] = (
        subgroup_totals["amount"] / total_employee_costs if total_employee_costs else np.nan
    )
    subgroup_totals = subgroup_totals.sort_values("amount", ascending=False)

    return EmployeeCostYearResult(
        year=years[-1] if len(years) == 1 else None,
        total_employee_costs=total_employee_costs,
        total_expenses=total_expenses,
        total_revenue=total_revenue,
        employee_costs_pct_of_expenses=(total_employee_costs / total_expenses) if total_expenses else None,
        employee_costs_pct_of_revenue=(total_employee_costs / total_revenue) if total_revenue else None,
        subgroup_totals=subgroup_totals,
    )


# --------------------------------------------------------------------------
# Cost-driver / base-vs-comparison analysis
# --------------------------------------------------------------------------

def account_level_comparison(loaded: LoadedWorkbook, base_year: int, comparison_year: int) -> pd.DataFrame:
    """Full comparison table at the individual source-account level. Handles
    missing base/comparison accounts explicitly -- never fabricates an
    infinite percentage."""
    df = with_management_group(loaded.accounts_df[loaded.accounts_df["account_type"] == "Expense"])

    base_df = df[df["year"] == base_year].set_index("account_code_base")
    comp_df = df[df["year"] == comparison_year].set_index("account_code_base")

    all_codes = sorted(set(base_df.index) | set(comp_df.index))
    base_total = base_df["amount"].sum()
    comp_total = comp_df["amount"].sum()

    records = []
    for code in all_codes:
        in_base = code in base_df.index
        in_comp = code in comp_df.index

        base_amount = float(base_df.loc[code, "amount"]) if in_base else None
        comp_amount = float(comp_df.loc[code, "amount"]) if in_comp else None

        name = comp_df.loc[code, "account_name_clean"] if in_comp else base_df.loc[code, "account_name_clean"]
        group_key = comp_df.loc[code, "group_key"] if in_comp else base_df.loc[code, "group_key"]
        group_name_en = comp_df.loc[code, "group_name_en"] if in_comp else base_df.loc[code, "group_name_en"]
        group_name_ar = comp_df.loc[code, "group_name_ar"] if in_comp else base_df.loc[code, "group_name_ar"]

        if in_base and in_comp:
            abs_change = comp_amount - base_amount
            if base_amount == 0:
                status = STATUS_ZERO_BASE
                pct_change = None
            else:
                status = STATUS_NORMAL
                pct_change = abs_change / abs(base_amount)
        elif in_comp and not in_base:
            abs_change = comp_amount
            pct_change = None
            status = STATUS_NEW
        elif in_base and not in_comp:
            abs_change = -base_amount
            pct_change = None
            status = STATUS_NOT_PRESENT
        else:
            continue

        records.append({
            "account_code_base": code,
            "account_name": name,
            "group_key": group_key,
            "group_name_en": group_name_en,
            "group_name_ar": group_name_ar,
            "base_amount": base_amount,
            "comparison_amount": comp_amount,
            "absolute_change": abs_change,
            "pct_change": pct_change,
            "status": status,
            "share_of_expenses_base": (base_amount / base_total) if (in_base and base_total) else None,
            "share_of_expenses_comparison": (comp_amount / comp_total) if (in_comp and comp_total) else None,
        })

    result = pd.DataFrame(records)
    if not result.empty:
        result["share_change"] = result["share_of_expenses_comparison"] - result["share_of_expenses_base"]
        result = result.sort_values("absolute_change", key=lambda s: s.abs(), ascending=False)
    return result


def cost_driver_ranking(loaded: LoadedWorkbook, base_year: int, comparison_year: int, top_n: int = 10) -> pd.DataFrame:
    """Ranks expense accounts by their contribution to the total expense
    movement between two years."""
    cmp = account_level_comparison(loaded, base_year, comparison_year)
    if cmp.empty:
        return cmp
    total_expense_change = cmp["absolute_change"].sum()
    cmp = cmp.copy()
    cmp["contribution_to_expense_change"] = (
        cmp["absolute_change"] / total_expense_change if total_expense_change != 0 else np.nan
    )
    return cmp.head(top_n)


def expense_heatmap_pivot(loaded: LoadedWorkbook, metric: str = "amount") -> pd.DataFrame:
    """Rows = expense accounts, columns = years. Missing years are NaN
    (not present in source) -- distinct from a recorded 0.0.
    metric: 'amount' | 'pct_of_expenses' | 'pct_of_revenue'
    """
    df = loaded.accounts_df[loaded.accounts_df["account_type"] == "Expense"].copy()

    if metric == "pct_of_expenses":
        totals = {y: yt.official_total_expenses for y, yt in loaded.year_totals.items()}
        df["value"] = df.apply(lambda r: r["amount"] / totals[r["year"]] if totals[r["year"]] else np.nan, axis=1)
    elif metric == "pct_of_revenue":
        totals = {y: yt.total_revenue for y, yt in loaded.year_totals.items()}
        df["value"] = df.apply(lambda r: r["amount"] / totals[r["year"]] if totals[r["year"]] else np.nan, axis=1)
    else:
        df["value"] = df["amount"]

    pivot = df.pivot_table(
        index=["account_code_base", "account_name_clean"],
        columns="year",
        values="value",
        aggfunc="sum",
    )
    return pivot
