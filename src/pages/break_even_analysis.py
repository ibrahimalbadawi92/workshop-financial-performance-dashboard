# -*- coding: utf-8 -*-
import streamlit as st

from src.translations import t
from src.ui_components import (
    page_header, section_title, note_box, note_2025_if_relevant, kpi_row, fmt_amount, fmt_pct,
    analysis_year_badge, info_popover,
)
from src.financial_metrics import get_year_metrics


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.break_even", t("app_subtitle", lang), period_label)

    years_sorted = sorted(selected_years)
    default_year = years_sorted[-1]
    year = st.selectbox(t("common.year", lang), options=years_sorted, index=len(years_sorted) - 1, key="be_year")
    analysis_year_badge(year, lang)
    note_2025_if_relevant([year], lang)

    m = get_year_metrics(loaded, year)

    kpi_row([
        dict(label=t("breakeven.current_revenue", lang), value_str=fmt_amount(m.total_revenue, lang, compact=True), lang=lang,
             key="be_current_revenue", help_key="help.breakeven_current_revenue"),
        dict(label=t("breakeven.current_expenses", lang), value_str=fmt_amount(m.total_expenses, lang, compact=True), lang=lang,
             key="be_current_expenses", help_key="help.breakeven_current_expenses"),
        dict(label=t("breakeven.current_result", lang), value_str=fmt_amount(m.official_pl, lang, compact=True), lang=lang,
             key="be_current_result", help_key="help.breakeven_current_result", negative_value=m.official_pl < 0),
        dict(label=t("breakeven.break_even_revenue", lang), value_str=fmt_amount(m.total_expenses, lang, compact=True), lang=lang,
             key="be_break_even_revenue", help_key="help.breakeven_break_even_revenue"),
    ], n_cols=4)

    st.write("")

    # --- Profit-aware branch ------------------------------------------------
    # The break-even GAP formula never changes (max(expenses - revenue, 0) --
    # see src.financial_metrics.get_year_metrics); only how the page
    # PRESENTS a zero gap changes. A zero gap can mean two different things
    # and must never be shown the same way: revenue exactly at break-even,
    # or revenue already above it. Showing "Required Revenue Increase: 0.0%"
    # in the profitable case would read as if a target were still pending.
    if m.official_pl >= 0:
        kpi_row([
            dict(label=t("kpi.break_even_gap", lang), value_str=fmt_amount(m.break_even_gap, lang, compact=True), lang=lang,
                 key="be_gap", help_key="help.kpi_break_even_gap"),
        ], n_cols=4)
        note_box(t("breakeven.already_above", lang), icon="✅")

        surplus_pct_revenue = (m.surplus_over_break_even / m.total_revenue) if m.total_revenue else None
        c1, c2 = st.columns(2)
        with c1:
            with st.container(horizontal=True, gap="small", vertical_alignment="center"):
                st.markdown(f"**{t('breakeven.surplus_amount', lang)}**")
                info_popover("help.breakeven_break_even_revenue", lang, key="pop_be_surplus_amount")
            st.markdown(f"### {fmt_amount(m.surplus_over_break_even, lang, compact=True)}")
        with c2:
            with st.container(horizontal=True, gap="small", vertical_alignment="center"):
                st.markdown(f"**{t('breakeven.surplus_pct', lang)}**")
                info_popover("help.breakeven_break_even_revenue", lang, key="pop_be_surplus_pct")
            st.markdown(f"### {fmt_pct(surplus_pct_revenue)}")
    else:
        kpi_row([
            dict(label=t("kpi.break_even_gap", lang), value_str=fmt_amount(m.break_even_gap, lang, compact=True), lang=lang,
                 key="be_gap", help_key="help.kpi_break_even_gap"),
        ], n_cols=4)

        c1, c2 = st.columns(2)
        with c1:
            with st.container(horizontal=True, gap="small", vertical_alignment="center"):
                st.markdown(f"**{t('breakeven.required_revenue_increase_pct', lang)}**")
                info_popover("help.breakeven_required_revenue_increase", lang, key="pop_be_rev_increase")
            st.markdown(f"### {fmt_pct(m.required_revenue_increase_pct)}")
            st.caption(fmt_amount(m.required_revenue_increase, lang))
        with c2:
            with st.container(horizontal=True, gap="small", vertical_alignment="center"):
                st.markdown(f"**{t('breakeven.required_expense_reduction_pct', lang)}**")
                info_popover("help.breakeven_required_expense_reduction", lang, key="pop_be_exp_reduction")
            st.markdown(f"### {fmt_pct(m.required_expense_reduction_pct)}")
            st.caption(fmt_amount(m.required_expense_reduction, lang))

    note_box(t("breakeven.disclaimer", lang), icon="ℹ️", lang=lang)
