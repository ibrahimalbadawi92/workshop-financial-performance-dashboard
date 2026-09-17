# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

from src.translations import t
from src.ui_components import (
    page_header, section_title, title_with_info, note_box, note_2025_if_relevant, fmt_amount, fmt_pct, kpi_row,
    comparison_status_label,
)
from src.formatting import bidi_isolate
from src.analysis import pl_driver_analysis
from src.expense_analysis import STATUS_NOT_PRESENT
from src import charts


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.pl_drivers", t("pl_drivers.page_question", lang), period_label)

    base_year = st.session_state.get("base_year")
    comparison_year = st.session_state.get("comparison_year")
    note_2025_if_relevant([base_year, comparison_year], lang)

    if base_year == comparison_year:
        note_box(t("filters.base_year", lang) + " = " + t("filters.comparison_year", lang), icon="⚠️")
        return

    result = pl_driver_analysis(loaded, base_year, comparison_year, top_n=10)
    cmp = result.comparison

    pl_delta_class = "neutral" if cmp.pl_change == 0 else ("good" if cmp.pl_change > 0 else "critical")
    kpi_row([
        dict(label=t("pl_drivers.revenue_component", lang), value_str=fmt_amount(cmp.revenue_change, lang, compact=True), lang=lang,
             key="pld_revenue_movement", help_key="help.kpi_revenue_movement",
             delta_str=(fmt_pct(cmp.revenue_change_pct) if cmp.revenue_change_pct is not None else None), delta_class="neutral"),
        dict(label=t("pl_drivers.expense_component", lang), value_str=fmt_amount(cmp.expense_change, lang, compact=True), lang=lang,
             key="pld_expense_movement", help_key="help.kpi_expense_movement",
             delta_str=(fmt_pct(cmp.expense_change_pct) if cmp.expense_change_pct is not None else None), delta_class="neutral"),
        dict(label=t("kpi.official_pl", lang) + " Δ", value_str=fmt_amount(cmp.pl_change, lang, compact=True), lang=lang,
             key="pld_pl_change", help_key="help.kpi_pl_change", delta_class=pl_delta_class),
    ], n_cols=3)

    st.caption(bidi_isolate(f"{base_year} → {comparison_year}"))

    title_with_info(t("chart.cost_driver_waterfall", lang), lang, key="pld_waterfall", help_key="help.chart_cost_driver_waterfall")
    top_movers = result.top_expense_contributors
    base_total = loaded.year_totals[base_year].official_total_expenses
    comp_total = loaded.year_totals[comparison_year].official_total_expenses
    shown = top_movers.head(8)
    movers_list = list(zip(shown["account_name"], shown["absolute_change"], shown["status"]))
    other_delta = (comp_total - base_total) - sum(m[1] for m in movers_list)
    fig = charts.cost_driver_waterfall_chart(base_year, comparison_year, base_total, movers_list, other_delta, comp_total, lang, show_title=False)
    st.plotly_chart(fig, use_container_width=True)

    if not top_movers.empty:
        top_row = top_movers.iloc[0]
        st.markdown(
            "**" + t("loss.largest_contributor", lang).format(
                base=bidi_isolate(str(base_year)), comparison=bidi_isolate(str(comparison_year)),
                account=top_row["account_name"],
                amount=bidi_isolate(fmt_amount(top_row["absolute_change"], lang)),
            ) + "**"
        )
        # The largest numerical change may be an account simply missing from
        # the comparison year's data, not a genuine cost reduction -- that
        # must be disclosed immediately, not implied as an improvement.
        if top_row["status"] == STATUS_NOT_PRESENT:
            note_box(
                t("loss.not_present_disclaimer", lang).format(year=bidi_isolate(str(comparison_year))),
                icon="ℹ️",
            )

    increases = top_movers[top_movers["absolute_change"] > 0].sort_values("absolute_change", ascending=False)
    decreases = top_movers[top_movers["absolute_change"] < 0].sort_values("absolute_change", ascending=True)

    def _fmt_table(df):
        out = df[["account_name", "group_name_en" if lang == "en" else "group_name_ar",
                   "base_amount", "comparison_amount", "absolute_change", "status"]].copy()
        out["status"] = out.apply(
            lambda row: comparison_status_label(row["status"], row["absolute_change"], lang), axis=1
        )
        for col in ["base_amount", "comparison_amount", "absolute_change"]:
            out[col] = out[col].map(lambda v: fmt_amount(v, lang) if pd.notna(v) else t("compare.status_not_present", lang))
        out.columns = [t("compare.account", lang), t("compare.group", lang), t("compare.base_amount", lang),
                       t("compare.comparison_amount", lang), t("compare.absolute_change", lang), t("compare.status", lang)]
        return out

    # Stacked full-width rather than side-by-side: at narrower desktop
    # widths (1440px) two half-width tables truncated columns like Status.
    title_with_info(t("pl_drivers.top_increases", lang), lang, key="pld_increases_table", help_key="help.table_expense_movers")
    st.dataframe(_fmt_table(increases), use_container_width=True, hide_index=True)
    title_with_info(t("pl_drivers.top_decreases", lang), lang, key="pld_decreases_table", help_key="help.table_expense_movers")
    st.dataframe(_fmt_table(decreases), use_container_width=True, hide_index=True)
    if (decreases["status"] == STATUS_NOT_PRESENT).any():
        st.caption(t("loss.not_present_table_note", lang))
