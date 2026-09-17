# -*- coding: utf-8 -*-
"""
Regression tests for the final local polish round: duplicate chart titles
removed, the P&L Drivers Status column no longer blank, Year Comparison's
two section headings are distinct, and the Data Quality reconciliation
table no longer displays raw floating-point noise.
"""
import inspect
from pathlib import Path

import pytest

from src import charts
from src.data_loader import get_loaded_workbook
from src.expense_analysis import STATUS_NOT_PRESENT, STATUS_NEW, STATUS_ZERO_BASE
from src.formatting import format_reconciliation_value
from src.translations import t
from src.ui_components import comparison_status_label

PAGES_DIR = Path(__file__).parent.parent / "src" / "pages"


# --- 1. Duplicate chart titles --------------------------------------------

CHART_FUNCS_WITH_SHOW_TITLE = [
    (charts.pl_trend_chart, ([2023, 2024], [-10, 10], "en"), {}),
    (charts.sorted_magnitude_bar_chart, (["a", "b"], [1, 2], "Some Title", "en"), {}),
    (charts.expense_heatmap_chart, ([2023, 2024], ["a"], [[1, 2]], "en"), {}),
    (charts.revenue_composition_chart, ([2023, 2024], {"A": [1, 2]}, "en"), {}),
    (charts.account_trend_chart, ([2023, 2024], [1, 2], "Account", "en"), {}),
    (charts.actual_vs_scenario_chart, (["A"], [1], [2], "en"), {}),
]


@pytest.mark.parametrize("fn,args,kwargs", CHART_FUNCS_WITH_SHOW_TITLE, ids=lambda x: getattr(x, "__name__", str(x)))
def test_chart_show_title_false_omits_plotly_title(fn, args, kwargs):
    fig = fn(*args, **{**kwargs, "show_title": False})
    layout_title = fig.layout.title
    assert layout_title.text is None


@pytest.mark.parametrize("fn,args,kwargs", CHART_FUNCS_WITH_SHOW_TITLE, ids=lambda x: getattr(x, "__name__", str(x)))
def test_chart_show_title_default_still_sets_a_title(fn, args, kwargs):
    # show_title defaults to True -- a chart used standalone (no external
    # title_with_info above it) must still be self-labeled.
    fig = fn(*args, **kwargs)
    assert fig.layout.title.text


def test_revenue_vs_expenses_and_employee_vs_revenue_and_waterfall_support_show_title():
    fig1 = charts.revenue_vs_expenses_chart([2023], [100], [90], "en", show_title=False)
    assert fig1.layout.title.text is None
    fig2 = charts.employee_vs_revenue_chart([2023], [100], [50], "en", show_title=False)
    assert fig2.layout.title.text is None
    fig3 = charts.cost_driver_waterfall_chart(2023, 2024, 100, [("a", 5, "Normal")], 0, 105, "en", show_title=False)
    assert fig3.layout.title.text is None


def test_no_page_overrides_a_chart_title_after_the_fact():
    # revenue_analysis.py previously called fig.update_layout(title=...)
    # right after building the chart, duplicating the title_with_info()
    # heading above it. That pattern must not come back on any page.
    for path in PAGES_DIR.glob("*.py"):
        src = path.read_text(encoding="utf-8")
        assert "update_layout(title=" not in src, f"{path.name} re-applies a chart title after construction"


def test_pages_pass_show_title_false_for_every_chart_immediately_after_a_section_heading():
    # A light structural check: every st.plotly_chart(...) call in the app
    # is either preceded by a title_with_info() (and so should suppress its
    # own title) or is the one documented exception (the selected-account
    # trend chart in expense_analysis.py, which has no matching external
    # heading and uses its title to show the chosen account's name).
    exceptions = {"src/pages/expense_analysis.py"}
    for path in PAGES_DIR.glob("*.py"):
        rel = f"src/pages/{path.name}"
        if rel in exceptions:
            continue
        src = path.read_text(encoding="utf-8")
        if "st.plotly_chart(" not in src:
            continue
        # Every chart-producing call on these pages must carry show_title
        # somewhere in the file if the page renders more than one chart
        # preceded by a matching title_with_info -- a full AST check is
        # overkill here; this is a smoke-level guard against regressing to
        # the old always-on-title pattern across the whole file.
        assert "show_title=False" in src, f"{path.name} has a chart but no show_title=False suppression"


# --- 2. P&L Drivers Status column ------------------------------------------

def test_comparison_status_label_normal_is_never_blank_for_a_nonzero_change():
    assert comparison_status_label("Normal", 100.0, "en") == "Increased"
    assert comparison_status_label("Normal", -100.0, "en") == "Decreased"
    assert comparison_status_label("Normal", 100.0, "ar") == "زيادة"
    assert comparison_status_label("Normal", -100.0, "ar") == "انخفاض"


def test_comparison_status_label_special_statuses_unchanged():
    assert comparison_status_label(STATUS_NEW, 50.0, "en") == t("compare.status_new", "en")
    assert comparison_status_label(STATUS_NOT_PRESENT, -50.0, "en") == t("compare.status_not_present", "en")
    assert comparison_status_label(STATUS_ZERO_BASE, None, "en") == t("compare.status_zero_base", "en")


def test_comparison_status_label_zero_change_normal_is_empty_not_error():
    # A Normal row with an exactly-zero change is a genuine edge case (not
    # expected in the increases/decreases tables, which are pre-filtered),
    # but must not raise or silently mislabel.
    assert comparison_status_label("Normal", 0.0, "en") == ""


def test_pl_drivers_page_status_values_are_never_blank_for_normal_rows():
    # End-to-end check against the real synthetic dataset: every row a real
    # base/comparison year pair would produce for the increases/decreases
    # tables gets a non-empty Status label.
    from src.analysis import pl_driver_analysis
    loaded = get_loaded_workbook()
    result = pl_driver_analysis(loaded, 2024, 2025, top_n=20)
    movers = result.top_expense_contributors
    assert not movers.empty
    for _, row in movers.iterrows():
        label_en = comparison_status_label(row["status"], row["absolute_change"], "en")
        label_ar = comparison_status_label(row["status"], row["absolute_change"], "ar")
        assert label_en != "", f"blank English status for {row['account_name']!r} (status={row['status']!r})"
        assert label_ar != "", f"blank Arabic status for {row['account_name']!r} (status={row['status']!r})"


def test_pl_drivers_page_no_longer_defines_a_local_blank_normal_mapping():
    src = (PAGES_DIR / "pl_drivers.py").read_text(encoding="utf-8")
    assert '"Normal": ""' not in src
    assert "comparison_status_label" in src


# --- 3. Year Comparison distinct headings ----------------------------------

def test_year_comparison_summary_and_detail_headings_are_distinct():
    assert t("compare.title_summary", "en") != t("compare.title_detail", "en")
    assert t("compare.title_summary", "ar") != t("compare.title_detail", "ar")
    for lang in ("en", "ar"):
        assert t("compare.title_summary", lang)
        assert t("compare.title_detail", lang)


def test_year_comparison_page_uses_distinct_heading_keys_not_repeated_title():
    src = (PAGES_DIR / "yearly_comparison.py").read_text(encoding="utf-8")
    assert 'title_with_info(t("compare.title_summary"' in src
    assert 'title_with_info(t("compare.title_detail"' in src
    # The old pattern -- the same "compare.title" key driving both section
    # headings -- must not reappear.
    assert src.count('title_with_info(t("compare.title"') == 0


def test_year_comparison_help_keys_unchanged():
    # The heading TEXT changed; the underlying help-popover content keys
    # (and therefore the calculations they describe) must not have moved.
    src = (PAGES_DIR / "yearly_comparison.py").read_text(encoding="utf-8")
    assert 'help_key="help.table_year_comparison_summary"' in src
    assert 'help_key="help.table_year_comparison_detail"' in src


# --- 4. Data Quality reconciliation display formatting ---------------------

def test_format_reconciliation_value_rounds_floating_point_noise_to_clean_zero():
    assert format_reconciliation_value(0.0000000001) == "0.00"
    assert format_reconciliation_value(-0.0000000009) == "0.00"
    assert format_reconciliation_value(0.0) == "0.00"
    assert format_reconciliation_value(-0.001) == "0.00"


def test_format_reconciliation_value_preserves_real_amounts():
    assert format_reconciliation_value(1234.5) == "1,234.50"
    assert format_reconciliation_value(-1234.5) == "-1,234.50"
    assert format_reconciliation_value(0.02) == "0.02"  # above the zero threshold


def test_data_quality_page_formats_reconciliation_columns_for_display():
    src = (PAGES_DIR / "data_quality.py").read_text(encoding="utf-8")
    assert "format_reconciliation_value" in src


def test_reconciliation_diff_display_never_shows_long_decimal_tails():
    # Regression guard on the real synthetic dataset: every year's
    # reconciliation_diff, once formatted for display, must not contain
    # more than 2 digits after the decimal point.
    import re
    from src.data_validation import run_full_validation
    loaded = get_loaded_workbook()
    report = run_full_validation(loaded)
    for raw in report.reconciliation_by_year["reconciliation_diff"]:
        formatted = format_reconciliation_value(raw)
        m = re.search(r"\.(\d+)$", formatted)
        assert m is not None
        assert len(m.group(1)) == 2, f"{raw} formatted as {formatted!r} has more than 2 decimal digits"
