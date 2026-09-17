# -*- coding: utf-8 -*-
"""
UI-adjacent logic tests: multi-year aggregation semantics, RTL-safe string
construction, and the profit-aware presentation rules added for this public
version (see src.pages.break_even_analysis and src.narrative).
"""
import pytest

from src.data_loader import get_loaded_workbook
from src.expense_analysis import employee_cost_analysis, employee_cost_analysis_for_years
from src.financial_metrics import get_year_metrics, get_aggregate_metrics
from src.formatting import bidi_isolate
from src.narrative import build_executive_summary


@pytest.fixture(scope="module")
def loaded():
    return get_loaded_workbook()


def test_multi_year_employee_pct_is_ratio_of_totals_not_average_of_percentages(loaded):
    years = [2017, 2022]  # a loss year and a strong-profit year -- their
    # annual employee-cost percentages differ enough that a naive average
    # would diverge from the correct aggregated-totals ratio.
    multi = employee_cost_analysis_for_years(loaded, years)
    naive_average = sum(
        employee_cost_analysis(loaded, y).employee_costs_pct_of_revenue for y in years
    ) / len(years)
    assert multi.employee_costs_pct_of_revenue != pytest.approx(naive_average)

    total_emp = sum(employee_cost_analysis(loaded, y).total_employee_costs for y in years)
    total_rev = sum(loaded.year_totals[y].total_revenue for y in years)
    assert multi.employee_costs_pct_of_revenue == pytest.approx(total_emp / total_rev)


def test_bidi_isolate_wraps_with_unicode_marks():
    result = bidi_isolate("2022-2023")
    assert result.startswith("⁦")
    assert result.endswith("⁩")
    assert "2022-2023" in result


def test_executive_summary_branches_on_sign_single_year(loaded):
    # 2017 is a loss year -- summary must say "loss", not "profit".
    summary_loss = build_executive_summary(loaded, [2017], "en")
    assert "loss" in summary_loss.lower()
    assert "profit of" not in summary_loss.lower()

    # 2022 is a profit year -- summary must say "profit", not "loss".
    summary_profit = build_executive_summary(loaded, [2022], "en")
    assert "profit" in summary_profit.lower()
    assert "loss of" not in summary_profit.lower()


def test_executive_summary_branches_on_sign_multi_year(loaded):
    # A selection whose aggregate is a net loss must use the loss template.
    agg_loss = get_aggregate_metrics(loaded, [2017, 2018])
    assert agg_loss.official_pl < 0
    summary = build_executive_summary(loaded, [2017, 2018], "en")
    assert "loss" in summary.lower()

    # A selection whose aggregate is a net profit must use the profit
    # template -- this is the exact regression this public version fixes
    # relative to the internal (all-loss) dataset, which never exercised
    # this branch.
    agg_profit = get_aggregate_metrics(loaded, [2021, 2022, 2023])
    assert agg_profit.official_pl > 0
    summary_profit = build_executive_summary(loaded, [2021, 2022, 2023], "en")
    assert "profit" in summary_profit.lower()
    assert "loss of" not in summary_profit.lower()


def test_break_even_gap_zero_does_not_imply_required_increase(loaded):
    # A profitable year's break-even gap is 0, and BOTH required-action
    # percentages must be 0 too -- never a stale/nonzero "required" figure
    # left over from some other year.
    m = get_year_metrics(loaded, 2022)
    assert m.official_pl > 0
    assert m.break_even_gap == 0.0
    assert m.required_revenue_increase_pct == 0.0
    assert m.required_expense_reduction_pct == 0.0
    assert m.surplus_over_break_even > 0
