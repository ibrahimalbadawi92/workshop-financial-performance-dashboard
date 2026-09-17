# -*- coding: utf-8 -*-
"""
Metric tests. Expected values here are either derived mathematically from
the loaded synthetic dataset itself (never a hardcoded external figure), or
are the synthetic year-level targets from scripts/generate_synthetic_data.py
(SAR 620,000 revenue in 2017, etc.) -- which are this project's own
independently-authored demo numbers, not any real company's figures.
"""
import math

import pandas as pd
import pytest

from src.data_loader import get_loaded_workbook
from src.financial_metrics import get_year_metrics, get_aggregate_metrics, compare_years
from src.expense_analysis import (
    top_n_expenses_for_year, expense_concentration, group_totals_for_year,
    employee_cost_analysis, account_level_comparison, cost_driver_ranking,
)
from src.data_validation import requires_completeness_caution_note


@pytest.fixture(scope="module")
def loaded():
    return get_loaded_workbook()


def test_year_metrics_2017_matches_synthetic_target(loaded):
    # 2017's independently-authored target: revenue=620,000, expenses=680,000
    # (scripts/generate_synthetic_data.py YEAR_TOTALS) -- a loss year.
    m = get_year_metrics(loaded, 2017)
    assert m.total_revenue == pytest.approx(620_000, abs=1)
    assert m.total_expenses == pytest.approx(680_000, abs=1)
    assert m.official_pl == pytest.approx(-60_000, abs=1)
    assert m.official_pl < 0
    assert m.break_even_gap == pytest.approx(60_000, abs=1)
    assert m.surplus_over_break_even == 0.0


def test_year_metrics_2022_is_a_profit_year(loaded):
    # 2022's target: revenue=810,000, expenses=760,000 -- the dataset's
    # strongest profitable year.
    m = get_year_metrics(loaded, 2022)
    assert m.official_pl == pytest.approx(50_000, abs=1)
    assert m.official_pl > 0
    assert m.break_even_gap == 0.0
    assert m.surplus_over_break_even == pytest.approx(50_000, abs=1)
    assert m.required_revenue_increase_pct == 0.0
    assert m.required_expense_reduction_pct == 0.0


def test_dataset_contains_both_profit_and_loss_years(loaded):
    # Explicit guard against ever regressing to an all-loss dataset (the
    # internal dashboard's dataset was all-loss; this public one must not be).
    pls = [yt.official_pl_amount for yt in loaded.year_totals.values()]
    assert any(v > 0 for v in pls), "synthetic dataset has no profitable year"
    assert any(v < 0 for v in pls), "synthetic dataset has no loss year"
    assert any(abs(v) < 20_000 for v in pls), "synthetic dataset has no near-break-even year"


def test_break_even_gap_matches_loss_magnitude_when_expenses_exceed_revenue(loaded):
    for year in loaded.year_totals:
        m = get_year_metrics(loaded, year)
        yt = loaded.year_totals[year]
        expected_gap = max(yt.official_total_expenses - yt.total_revenue, 0.0)
        assert m.break_even_gap == pytest.approx(expected_gap)
        expected_surplus = max(yt.total_revenue - yt.official_total_expenses, 0.0)
        assert m.surplus_over_break_even == pytest.approx(expected_surplus)


def test_break_even_gap_and_surplus_are_mutually_exclusive(loaded):
    for year in loaded.year_totals:
        m = get_year_metrics(loaded, year)
        assert m.break_even_gap == 0.0 or m.surplus_over_break_even == 0.0


def test_break_even_required_reduction_pct_is_zero_when_already_profitable(loaded):
    m = get_year_metrics(loaded, 2025)  # 2025 is a profit year in this dataset
    assert m.official_pl > 0
    assert m.required_expense_reduction_pct == 0.0
    assert m.required_revenue_increase_pct == 0.0


def test_break_even_required_reduction_pct_positive_when_loss(loaded):
    m = get_year_metrics(loaded, 2024)  # 2024 is a loss year in this dataset
    assert m.official_pl < 0
    assert m.required_expense_reduction_pct == pytest.approx(m.break_even_gap / m.total_expenses)
    assert m.required_revenue_increase_pct == pytest.approx(m.break_even_gap / m.total_revenue)


def test_aggregate_metrics_sum_correctly(loaded):
    agg = get_aggregate_metrics(loaded, [2017, 2018])
    m17 = get_year_metrics(loaded, 2017)
    m18 = get_year_metrics(loaded, 2018)
    assert agg.total_revenue == pytest.approx(m17.total_revenue + m18.total_revenue)
    assert agg.total_expenses == pytest.approx(m17.total_expenses + m18.total_expenses)
    assert agg.official_pl == pytest.approx(m17.official_pl + m18.official_pl)


def test_selected_year_change_2017_vs_2025(loaded):
    cmp = compare_years(loaded, 2017, 2025)
    m17 = get_year_metrics(loaded, 2017)
    m25 = get_year_metrics(loaded, 2025)
    assert cmp.revenue_change == pytest.approx(m25.total_revenue - m17.total_revenue)
    assert cmp.expense_change == pytest.approx(m25.total_expenses - m17.total_expenses)
    assert cmp.pl_change == pytest.approx(m25.official_pl - m17.official_pl)
    assert cmp.pl_change == pytest.approx(cmp.revenue_change - cmp.expense_change, abs=0.5)


def test_top_expense_wages_is_largest_every_year(loaded):
    for year in loaded.year_totals:
        top = top_n_expenses_for_year(loaded, year, n=1)
        assert top.iloc[0]["account_code_base"] == "5101", f"Salaries & Wages not top expense in {year}"


def test_expense_concentration_shares_between_0_and_1(loaded):
    for year in loaded.year_totals:
        c = expense_concentration(loaded, year)
        assert 0 < c["top5_share"] <= 1
        assert c["top5_share"] <= c["top10_share"] <= 1


def test_group_totals_sum_to_official_total_expenses(loaded):
    for year in loaded.year_totals:
        grp = group_totals_for_year(loaded, year)
        yt = loaded.year_totals[year]
        assert grp["amount"].sum() == pytest.approx(yt.official_total_expenses, abs=0.5)


def test_employee_cost_never_exceeds_total_expenses(loaded):
    for year in loaded.year_totals:
        r = employee_cost_analysis(loaded, year)
        assert r.total_employee_costs <= r.total_expenses + 0.5


def test_employee_cost_analysis_subgroups_sum_to_total(loaded):
    for year in loaded.year_totals:
        r = employee_cost_analysis(loaded, year)
        assert abs(r.subgroup_totals["share_of_employee_costs"].sum() - 1.0) < 1e-6


def test_cost_driver_ranking_no_infinite_pct(loaded):
    ranking = cost_driver_ranking(loaded, 2020, 2021, top_n=50)
    for v in ranking["pct_change"]:
        if pd.notna(v):
            assert math.isfinite(v)


def test_requires_completeness_caution_note():
    assert requires_completeness_caution_note([2016, 2017]) is True
    assert requires_completeness_caution_note([2017]) is True
    assert requires_completeness_caution_note([2020, 2021]) is False
