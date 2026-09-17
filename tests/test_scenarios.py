# -*- coding: utf-8 -*-
import pytest

from src.data_loader import get_loaded_workbook
from src.scenario_analysis import run_scenario


@pytest.fixture(scope="module")
def loaded():
    return get_loaded_workbook()


def test_zero_pct_scenario_equals_actual(loaded):
    result = run_scenario(loaded, 2022, revenue_increase_pct=0.0, expense_reduction_pct=0.0)
    assert result.scenario_revenue == pytest.approx(result.actual_revenue)
    assert result.scenario_expenses == pytest.approx(result.actual_expenses)
    assert result.scenario_pl == pytest.approx(result.actual_pl)


def test_scenario_on_loss_year_can_reach_break_even(loaded):
    # 2017 is a loss year (-60,000); a large enough revenue increase must
    # cross zero.
    result = run_scenario(loaded, 2017, revenue_increase_pct=0.15, expense_reduction_pct=0.0)
    assert result.reaches_break_even is True
    assert result.gap_to_break_even == 0.0


def test_scenario_on_loss_year_insufficient_increase_does_not_reach(loaded):
    result = run_scenario(loaded, 2017, revenue_increase_pct=0.01, expense_reduction_pct=0.0)
    assert result.reaches_break_even is False
    assert result.gap_to_break_even > 0


def test_scenario_on_profit_year_stays_above_break_even_at_zero_pct(loaded):
    # 2022 is already profitable -- the default (0%/0%) scenario must still
    # read as "reaches break-even" (it never regresses below it), not as an
    # error or an undefined state.
    result = run_scenario(loaded, 2022, revenue_increase_pct=0.0, expense_reduction_pct=0.0)
    assert result.reaches_break_even is True
    assert result.gap_to_break_even == 0.0


def test_scenario_expense_reduction_direction(loaded):
    result = run_scenario(loaded, 2024, revenue_increase_pct=0.0, expense_reduction_pct=0.10)
    assert result.scenario_expenses == pytest.approx(result.actual_expenses * 0.90)


def test_scenario_revenue_increase_direction(loaded):
    result = run_scenario(loaded, 2024, revenue_increase_pct=0.10, expense_reduction_pct=0.0)
    assert result.scenario_revenue == pytest.approx(result.actual_revenue * 1.10)
