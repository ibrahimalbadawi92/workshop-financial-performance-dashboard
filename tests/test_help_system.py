# -*- coding: utf-8 -*-
"""
Coverage for the info-popover help system across all 8 dashboard pages:
every KPI/chart/table that shows an info icon must have real bilingual help
content behind it, and none of it may describe the real internal project's
confidential facts (the 2019 label quirk, the 2025 provision/depreciation
omission, "management approved" framing).
"""
import re
from pathlib import Path

from src.translations import STRINGS
from src.help_translations import HELP_STRINGS
from src.ui_components import _has_help_content

PAGES_DIR = Path(__file__).parent.parent / "src" / "pages"

_HELP_SUFFIXES = ("definition", "calculation", "how_to_read", "notes")


def _help_keys_used_in_pages() -> set:
    keys = set()
    pattern = re.compile(r'help_key="(help\.[a-zA-Z0-9_]+)"')
    popover_pattern = re.compile(r'info_popover\(\s*"(help\.[a-zA-Z0-9_]+)"')
    for path in PAGES_DIR.glob("*.py"):
        src = path.read_text(encoding="utf-8")
        keys.update(pattern.findall(src))
        keys.update(popover_pattern.findall(src))
    return keys


ALL_USED_HELP_KEYS = _help_keys_used_in_pages()


def test_help_keys_were_actually_found_in_pages():
    assert len(ALL_USED_HELP_KEYS) >= 35


def test_every_used_help_key_has_content():
    missing = [k for k in ALL_USED_HELP_KEYS if not _has_help_content(k)]
    assert missing == [], f"help_key referenced in a page but has no HELP_STRINGS content: {missing}"


def test_every_help_content_key_is_bilingual():
    missing = []
    for key, entry in HELP_STRINGS.items():
        if not entry.get("ar") or not entry.get("en"):
            missing.append(key)
    assert missing == [], f"Help strings missing an ar/en value: {missing}"


def test_section_header_labels_are_bilingual():
    for suffix in _HELP_SUFFIXES:
        key = f"help.section.{suffix}"
        assert key in STRINGS
        assert STRINGS[key]["ar"] and STRINGS[key]["en"]


def test_every_main_kpi_has_help():
    required = [
        "help.kpi_total_revenue", "help.kpi_total_expenses", "help.kpi_official_pl",
        "help.kpi_net_result_margin", "help.kpi_expense_to_revenue_ratio",
        "help.kpi_break_even_gap", "help.kpi_employee_costs",
        "help.kpi_employee_costs_pct_revenue",
    ]
    for key in required:
        assert _has_help_content(key), f"Missing help content for required KPI: {key}"


def test_every_main_chart_has_help():
    required = [
        "help.chart_revenue_vs_expenses", "help.chart_pl_trend", "help.chart_expense_composition",
        "help.chart_revenue_trend", "help.chart_revenue_composition",
        "help.chart_top_expenses", "help.chart_expense_heatmap",
        "help.chart_employee_subgroups", "help.chart_employee_vs_revenue",
        "help.chart_cost_driver_waterfall", "help.chart_actual_vs_scenario",
    ]
    for key in required:
        assert _has_help_content(key), f"Missing help content for required chart: {key}"


def test_every_important_table_has_help():
    required = [
        "help.table_revenue_comparison", "help.table_expense_group_view",
        "help.table_expense_account_view", "help.table_expense_movers",
        "help.table_year_comparison_summary", "help.table_year_comparison_detail",
        "help.dq_reconciliation_table",
    ]
    for key in required:
        assert _has_help_content(key), f"Missing help content for required table: {key}"


def test_break_even_and_whatif_kpis_have_help():
    required = [
        "help.breakeven_current_revenue", "help.breakeven_current_expenses",
        "help.breakeven_current_result", "help.breakeven_break_even_revenue",
        "help.breakeven_required_revenue_increase", "help.breakeven_required_expense_reduction",
        "help.whatif_revenue_slider", "help.whatif_expense_slider", "help.whatif_scenario_pl",
    ]
    for key in required:
        assert _has_help_content(key), f"Missing help content for required Break-Even/What-If item: {key}"


def test_data_quality_kpis_have_help():
    for key in ("help.dq_years_loaded", "help.dq_sheets_loaded", "help.dq_account_counts"):
        assert _has_help_content(key)


def test_dq_label_note_key_exists_and_is_bilingual():
    key = "help.dq_label_note.definition"
    assert key in STRINGS
    assert STRINGS[key]["ar"] and STRINGS[key]["en"]


def test_dq_label_note_placeholders_survive_formatting():
    for lang in ("ar", "en"):
        STRINGS["help.dq_label_note.definition"][lang].format(year=2018, label="Result")


def test_help_text_contains_no_confidential_2019_or_2025_facts():
    forbidden_patterns = [
        r"end-of-service provision and depreciation",
        r"\bالورشة»",  # the real nonstandard 2019 label, quoted
    ]
    for key, entry in HELP_STRINGS.items():
        for lang, text in entry.items():
            for pattern in forbidden_patterns:
                assert not re.search(pattern, text), f"Confidential fact leaked in HELP_STRINGS[{key!r}][{lang!r}]"


def test_no_management_approved_phrasing_in_help_text():
    forbidden = ["management's approved", "management's instruction", "management approved"]
    for key, entry in HELP_STRINGS.items():
        text_en = entry.get("en", "").lower()
        for phrase in forbidden:
            assert phrase not in text_en, f"Forbidden phrase {phrase!r} found in HELP_STRINGS[{key!r}]['en']"
