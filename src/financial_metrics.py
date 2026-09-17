# -*- coding: utf-8 -*-
"""
Core KPI formulas. Every formula here is the literal arithmetic definition
used throughout this project -- nothing is a forecast, benchmark, or
estimate. All inputs come from src.data_loader.LoadedWorkbook.
"""

from dataclasses import dataclass
from typing import Iterable, Optional

from src.data_loader import LoadedWorkbook


@dataclass
class YearMetrics:
    year: int
    total_revenue: float
    total_expenses: float
    official_pl: float
    net_result_margin: Optional[float]          # official_pl / total_revenue
    expense_to_revenue_ratio: Optional[float]    # total_expenses / total_revenue
    break_even_gap: float                        # max(total_expenses - total_revenue, 0)
    required_revenue_increase: float
    required_revenue_increase_pct: Optional[float]
    required_expense_reduction: float
    required_expense_reduction_pct: Optional[float]
    surplus_over_break_even: float                # max(total_revenue - total_expenses, 0)


def _safe_div(numerator: float, denominator: float) -> Optional[float]:
    if denominator == 0:
        return None
    return numerator / denominator


def get_year_metrics(loaded: LoadedWorkbook, year: int) -> YearMetrics:
    yt = loaded.year_totals[year]
    total_revenue = yt.total_revenue
    total_expenses = yt.official_total_expenses
    official_pl = yt.official_pl_amount

    gap = max(total_expenses - total_revenue, 0.0)
    surplus = max(total_revenue - total_expenses, 0.0)

    return YearMetrics(
        year=year,
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        official_pl=official_pl,
        net_result_margin=_safe_div(official_pl, total_revenue),
        expense_to_revenue_ratio=_safe_div(total_expenses, total_revenue),
        break_even_gap=gap,
        required_revenue_increase=gap,
        required_revenue_increase_pct=_safe_div(gap, total_revenue),
        required_expense_reduction=gap,
        required_expense_reduction_pct=_safe_div(gap, total_expenses),
        surplus_over_break_even=surplus,
    )


@dataclass
class AggregateMetrics:
    years: tuple
    total_revenue: float
    total_expenses: float
    official_pl: float
    net_result_margin: Optional[float]
    expense_to_revenue_ratio: Optional[float]


def get_aggregate_metrics(loaded: LoadedWorkbook, years: Iterable[int]) -> AggregateMetrics:
    """Sum of flow amounts across the selected years. Valid because each
    year's Total Revenue / Total Expenses / Official P/L are period flow
    amounts from independent annual income statements."""
    years = tuple(sorted(years))
    total_revenue = sum(loaded.year_totals[y].total_revenue for y in years)
    total_expenses = sum(loaded.year_totals[y].official_total_expenses for y in years)
    official_pl = sum(loaded.year_totals[y].official_pl_amount for y in years)
    return AggregateMetrics(
        years=years,
        total_revenue=total_revenue,
        total_expenses=total_expenses,
        official_pl=official_pl,
        net_result_margin=_safe_div(official_pl, total_revenue),
        expense_to_revenue_ratio=_safe_div(total_expenses, total_revenue),
    )


@dataclass
class YearComparison:
    base_year: int
    comparison_year: int
    revenue_change: float
    revenue_change_pct: Optional[float]
    expense_change: float
    expense_change_pct: Optional[float]
    pl_change: float
    pl_change_pct: Optional[float]
    pl_change_from_revenue_component: float
    pl_change_from_expense_component: float


def get_selection_change(loaded: LoadedWorkbook, years: Iterable[int]) -> Optional[YearComparison]:
    """Defines 'Revenue/Expense/P&L Change' for a year selection, unambiguously:
    - Single year selected: change vs the immediately preceding calendar year
      in the dataset, if one exists (else None).
    - Multiple years selected: change from the EARLIEST to the LATEST selected
      year (a period-start vs period-end comparison, not an average)."""
    years = sorted(years)
    if not years:
        return None
    if len(years) == 1:
        prior = years[0] - 1
        if prior not in loaded.year_totals:
            return None
        return compare_years(loaded, prior, years[0])
    return compare_years(loaded, years[0], years[-1])


def compare_years(loaded: LoadedWorkbook, base_year: int, comparison_year: int) -> YearComparison:
    base = loaded.year_totals[base_year]
    comp = loaded.year_totals[comparison_year]

    revenue_change = comp.total_revenue - base.total_revenue
    expense_change = comp.official_total_expenses - base.official_total_expenses
    pl_change = comp.official_pl_amount - base.official_pl_amount

    return YearComparison(
        base_year=base_year,
        comparison_year=comparison_year,
        revenue_change=revenue_change,
        revenue_change_pct=_safe_div(revenue_change, abs(base.total_revenue)),
        expense_change=expense_change,
        expense_change_pct=_safe_div(expense_change, abs(base.official_total_expenses)),
        pl_change=pl_change,
        pl_change_pct=_safe_div(pl_change, abs(base.official_pl_amount)),
        pl_change_from_revenue_component=revenue_change,
        pl_change_from_expense_component=-expense_change,
    )
