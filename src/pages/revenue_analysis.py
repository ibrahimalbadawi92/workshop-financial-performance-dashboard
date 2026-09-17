# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

from src.translations import t
from src.ui_components import page_header, section_title, title_with_info, note_box, note_2025_if_relevant, fmt_amount, fmt_pct
from src.analysis import revenue_breakdown_by_year, REVENUE_LABEL_KEYS
from src.financial_metrics import get_selection_change
from src import charts


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.revenue_analysis", t("app_subtitle", lang), period_label)
    note_2025_if_relevant(selected_years, lang)
    note_box(t("revenue.classification_note", lang), icon="ℹ️")

    years_sorted = sorted(selected_years)
    df = revenue_breakdown_by_year(loaded, years_sorted)

    title_with_info(t("chart.revenue_trend", lang), lang, key="rev_trend_chart", help_key="help.chart_revenue_trend")
    total_by_year = df.groupby("year")["amount"].sum().reindex(years_sorted)
    fig = charts.account_trend_chart(years_sorted, total_by_year.tolist(), t("kpi.total_revenue", lang), lang, show_title=False)
    st.plotly_chart(fig, use_container_width=True)

    title_with_info(t("chart.revenue_composition", lang), lang, key="rev_comp_chart", help_key="help.chart_revenue_composition")
    series = {}
    for code, key in REVENUE_LABEL_KEYS.items():
        sub = df[df["account_code_base"] == code].set_index("year")["amount"]
        vals = [float(sub.get(y, 0.0)) if y in sub.index else 0.0 for y in years_sorted]
        if any(v != 0 for v in vals) or code in df["account_code_base"].unique():
            series[t(key, lang)] = vals
    if series:
        st.plotly_chart(charts.revenue_composition_chart(years_sorted, series, lang, show_title=False), use_container_width=True)

    title_with_info(t("compare.title", lang), lang, key="rev_compare_table", help_key="help.table_revenue_comparison")
    change = get_selection_change(loaded, selected_years)
    if change:
        rows = []
        for code, key in REVENUE_LABEL_KEYS.items():
            base_row = df[(df.year == change.base_year) & (df.account_code_base == code)]
            comp_row = df[(df.year == change.comparison_year) & (df.account_code_base == code)]
            base_amt = float(base_row["amount"].iloc[0]) if not base_row.empty else None
            comp_amt = float(comp_row["amount"].iloc[0]) if not comp_row.empty else None
            if base_amt is None and comp_amt is None:
                continue
            abs_change = (comp_amt or 0) - (base_amt or 0)
            pct_change = (abs_change / abs(base_amt)) if base_amt else None
            rows.append({
                t("compare.account", lang): t(key, lang),
                change.base_year: fmt_amount(base_amt, lang) if base_amt is not None else t("compare.status_not_present", lang),
                change.comparison_year: fmt_amount(comp_amt, lang) if comp_amt is not None else t("compare.status_not_present", lang),
                t("compare.absolute_change", lang): fmt_amount(abs_change, lang),
                t("compare.pct_change", lang): fmt_pct(pct_change) if pct_change is not None else "-",
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.caption(t("common.na", lang))

    with st.expander(t("common.table_view", lang)):
        display_df = df.copy()
        display_df["account_label"] = display_df["account_code_base"].map(
            lambda c: t(REVENUE_LABEL_KEYS.get(c, ""), lang) or c
        )
        st.dataframe(
            display_df[["year", "account_code", "account_label", "amount"]]
            .rename(columns={
                "year": t("common.year", lang), "amount": t("expense.metric_amount", lang),
            }),
            use_container_width=True, hide_index=True,
        )
