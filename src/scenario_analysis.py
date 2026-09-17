# -*- coding: utf-8 -*-
"""
User-driven what-if scenarios. Pure arithmetic on top of actual year data --
never a forecast, never a suggested target. All percentages default to 0%
and must be supplied explicitly by the caller (the UI layer).
"""

from dataclasses import dataclass

from src.data_loader import LoadedWorkbook


@dataclass
class ScenarioResult:
    year: int
    actual_revenue: float
    actual_expenses: float
    actual_pl: float
    revenue_increase_pct: float
    expense_reduction_pct: float
    scenario_revenue: float
    scenario_expenses: float
    scenario_pl: float
    reaches_break_even: bool
    gap_to_break_even: float  # 0 if reached; otherwise remaining shortfall


def run_scenario(
    loaded: LoadedWorkbook,
    year: int,
    revenue_increase_pct: float = 0.0,
    expense_reduction_pct: float = 0.0,
) -> ScenarioResult:
    yt = loaded.year_totals[year]
    actual_revenue = yt.total_revenue
    actual_expenses = yt.official_total_expenses
    actual_pl = yt.official_pl_amount

    scenario_revenue = actual_revenue * (1 + revenue_increase_pct)
    scenario_expenses = actual_expenses * (1 - expense_reduction_pct)
    scenario_pl = scenario_revenue - scenario_expenses

    return ScenarioResult(
        year=year,
        actual_revenue=actual_revenue,
        actual_expenses=actual_expenses,
        actual_pl=actual_pl,
        revenue_increase_pct=revenue_increase_pct,
        expense_reduction_pct=expense_reduction_pct,
        scenario_revenue=scenario_revenue,
        scenario_expenses=scenario_expenses,
        scenario_pl=scenario_pl,
        reaches_break_even=scenario_pl >= 0,
        gap_to_break_even=max(-scenario_pl, 0.0),
    )


SCENARIO_DISCLAIMER_AR = (
    "قيم السيناريو افتراضية يحددها المستخدم لأغراض تحليلية ولا تمثل توقعًا أو اعتمادًا ماليًا."
)
SCENARIO_DISCLAIMER_EN = (
    "Scenario values are user-defined for analytical purposes and do not represent a forecast "
    "or approved financial target."
)
