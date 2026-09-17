# -*- coding: utf-8 -*-
import streamlit as st

from src.translations import t
from src.ui_components import (
    page_header, section_title, title_with_info, note_box, note_2025_if_relevant, fmt_amount, kpi_row,
    directional_amount_str, analysis_year_badge, info_popover,
)
from src.scenario_analysis import run_scenario, SCENARIO_DISCLAIMER_AR, SCENARIO_DISCLAIMER_EN
from src import charts


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.what_if", t("app_subtitle", lang), period_label)

    years_sorted = sorted(selected_years)
    year = st.selectbox(t("common.year", lang), options=years_sorted, index=len(years_sorted) - 1, key="wi_year")
    analysis_year_badge(year, lang)
    note_2025_if_relevant([year], lang)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(horizontal=True, gap="small", vertical_alignment="center"):
            st.markdown(f"**{t('whatif.revenue_increase_pct', lang)}**")
            info_popover("help.whatif_revenue_slider", lang, key="pop_wi_rev_slider")
        rev_pct = st.slider(t("whatif.revenue_increase_pct", lang), min_value=0, max_value=100, value=0, step=1,
                             key="wi_rev_slider", label_visibility="collapsed") / 100.0
    with c2:
        with st.container(horizontal=True, gap="small", vertical_alignment="center"):
            st.markdown(f"**{t('whatif.expense_reduction_pct', lang)}**")
            info_popover("help.whatif_expense_slider", lang, key="pop_wi_exp_slider")
        exp_pct = st.slider(t("whatif.expense_reduction_pct", lang), min_value=0, max_value=100, value=0, step=1,
                             key="wi_exp_slider", label_visibility="collapsed") / 100.0

    result = run_scenario(loaded, year, revenue_increase_pct=rev_pct, expense_reduction_pct=exp_pct)

    st.markdown(f"##### {t('whatif.actual_section', lang)}")
    kpi_row([
        dict(label=t("kpi.total_revenue", lang), value_str=fmt_amount(result.actual_revenue, lang, compact=True), lang=lang,
             key="wi_actual_revenue", help_key="help.kpi_total_revenue", secondary=True),
        dict(label=t("kpi.total_expenses", lang), value_str=fmt_amount(result.actual_expenses, lang, compact=True), lang=lang,
             key="wi_actual_expenses", help_key="help.kpi_total_expenses", secondary=True),
        dict(label=t("kpi.official_pl", lang), value_str=fmt_amount(result.actual_pl, lang, compact=True), lang=lang,
             key="wi_actual_pl", help_key="help.kpi_official_pl", secondary=True, negative_value=result.actual_pl < 0),
    ], n_cols=3)

    st.write("")
    st.markdown(f"##### {t('whatif.scenario_section', lang)}")

    revenue_delta = result.scenario_revenue - result.actual_revenue
    expense_delta = result.scenario_expenses - result.actual_expenses
    pl_delta = result.scenario_pl - result.actual_pl

    # Revenue/Expense deltas are the user's own chosen inputs -- informational,
    # not a judgment -- so they stay neutral-colored. Only the resulting P/L
    # movement is colored, and only when it is genuinely non-zero.
    pl_delta_class = "neutral" if pl_delta == 0 else ("good" if pl_delta > 0 else "critical")

    kpi_row([
        dict(label=t("kpi.total_revenue", lang), value_str=fmt_amount(result.scenario_revenue, lang, compact=True), lang=lang,
             key="wi_scenario_revenue", help_key="help.whatif_revenue_slider",
             delta_str=directional_amount_str(revenue_delta, lang), delta_class="neutral"),
        dict(label=t("kpi.total_expenses", lang), value_str=fmt_amount(result.scenario_expenses, lang, compact=True), lang=lang,
             key="wi_scenario_expenses", help_key="help.whatif_expense_slider",
             delta_str=directional_amount_str(expense_delta, lang), delta_class="neutral"),
        dict(label=t("kpi.official_pl", lang), value_str=fmt_amount(result.scenario_pl, lang, compact=True), lang=lang,
             key="wi_scenario_pl", help_key="help.whatif_scenario_pl",
             delta_str=directional_amount_str(pl_delta, lang), delta_class=pl_delta_class,
             negative_value=result.scenario_pl < 0),
    ], n_cols=3)

    if result.reaches_break_even:
        note_box(t("whatif.reaches_break_even", lang), icon="✅")
    else:
        note_box(f"{t('whatif.does_not_reach', lang)} — {t('whatif.gap_remaining', lang)}: {fmt_amount(result.gap_to_break_even, lang, compact=True)}", icon="ℹ️")

    title_with_info(t("chart.actual_vs_scenario", lang), lang, key="wi_chart", help_key="help.chart_actual_vs_scenario")
    labels = [t("kpi.total_revenue", lang), t("kpi.total_expenses", lang), t("kpi.official_pl", lang)]
    st.plotly_chart(
        charts.actual_vs_scenario_chart(
            labels,
            [result.actual_revenue, result.actual_expenses, result.actual_pl],
            [result.scenario_revenue, result.scenario_expenses, result.scenario_pl],
            lang, show_title=False,
        ),
        use_container_width=True,
    )

    note_box(SCENARIO_DISCLAIMER_AR if lang == "ar" else SCENARIO_DISCLAIMER_EN, icon="⚠️")
