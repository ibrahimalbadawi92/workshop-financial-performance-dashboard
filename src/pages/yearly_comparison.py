# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

from src.translations import t
from src.ui_components import page_header, section_title, title_with_info, note_2025_if_relevant, fmt_amount, fmt_pct
from src.financial_metrics import get_year_metrics
from src.expense_analysis import (
    employee_cost_analysis, account_level_comparison, STATUS_NOT_PRESENT, STATUS_NEW, STATUS_ZERO_BASE,
)
from src import design_tokens as tok


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.year_comparison", t("compare.title", lang), period_label)

    base_year = st.session_state.get("base_year")
    comparison_year = st.session_state.get("comparison_year")
    note_2025_if_relevant([base_year, comparison_year], lang)

    m_base = get_year_metrics(loaded, base_year)
    m_comp = get_year_metrics(loaded, comparison_year)
    emp_base = employee_cost_analysis(loaded, base_year)
    emp_comp = employee_cost_analysis(loaded, comparison_year)

    rows = [
        (t("kpi.total_revenue", lang), fmt_amount(m_base.total_revenue, lang), fmt_amount(m_comp.total_revenue, lang)),
        (t("kpi.total_expenses", lang), fmt_amount(m_base.total_expenses, lang), fmt_amount(m_comp.total_expenses, lang)),
        (t("kpi.official_pl", lang), fmt_amount(m_base.official_pl, lang), fmt_amount(m_comp.official_pl, lang)),
        (t("kpi.net_result_margin", lang), fmt_pct(m_base.net_result_margin), fmt_pct(m_comp.net_result_margin)),
        (t("kpi.expense_to_revenue_ratio", lang), fmt_pct(m_base.expense_to_revenue_ratio), fmt_pct(m_comp.expense_to_revenue_ratio)),
        (t("kpi.employee_costs", lang), fmt_amount(emp_base.total_employee_costs, lang), fmt_amount(emp_comp.total_employee_costs, lang)),
        (t("kpi.employee_costs_pct_revenue", lang), fmt_pct(emp_base.employee_costs_pct_of_revenue), fmt_pct(emp_comp.employee_costs_pct_of_revenue)),
        (t("kpi.break_even_gap", lang), fmt_amount(m_base.break_even_gap, lang), fmt_amount(m_comp.break_even_gap, lang)),
    ]
    df_kpi = pd.DataFrame(rows, columns=["", str(base_year), str(comparison_year)])
    title_with_info(t("compare.title_summary", lang), lang, key="yc_summary_table", help_key="help.table_year_comparison_summary")
    st.dataframe(df_kpi, use_container_width=True, hide_index=True)

    title_with_info(t("compare.title_detail", lang), lang, key="yc_detail_table", help_key="help.table_year_comparison_detail")
    if base_year == comparison_year:
        st.caption(t("common.na", lang))
        return

    cmp = account_level_comparison(loaded, base_year, comparison_year)
    has_not_present = (cmp["status"] == STATUS_NOT_PRESENT).any()
    display = cmp.copy()
    display["status"] = display["status"].map(lambda s: {
        "Normal": "", STATUS_NEW: t("compare.status_new", lang),
        STATUS_NOT_PRESENT: t("compare.status_not_present", lang),
        STATUS_ZERO_BASE: t("compare.status_zero_base", lang),
    }.get(s, s))
    group_col = "group_name_en" if lang == "en" else "group_name_ar"
    display = display[[
        "account_name", group_col, "base_amount", "comparison_amount", "absolute_change", "pct_change",
        "share_of_expenses_base", "share_of_expenses_comparison", "share_change", "status",
    ]]
    display.columns = [
        t("compare.account", lang), t("compare.group", lang), t("compare.base_amount", lang), t("compare.comparison_amount", lang),
        t("compare.absolute_change", lang), t("compare.pct_change", lang),
        t("compare.share_base", lang), t("compare.share_comparison", lang), t("compare.share_change", lang),
        t("compare.status", lang),
    ]
    for col in [t("compare.base_amount", lang), t("compare.comparison_amount", lang), t("compare.absolute_change", lang)]:
        display[col] = display[col].map(lambda v: fmt_amount(v, lang) if pd.notna(v) else t("compare.status_not_present", lang))
    for col in [t("compare.pct_change", lang), t("compare.share_base", lang), t("compare.share_comparison", lang), t("compare.share_change", lang)]:
        display[col] = display[col].map(lambda v: fmt_pct(v) if pd.notna(v) else "-")
    st.dataframe(display, use_container_width=True, hide_index=True, height=520)
    if has_not_present:
        st.caption(t("loss.not_present_table_note", lang))
