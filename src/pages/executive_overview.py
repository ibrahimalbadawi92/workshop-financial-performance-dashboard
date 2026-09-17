# -*- coding: utf-8 -*-
import streamlit as st

from src.translations import t
from src.ui_components import (
    page_header, section_title, title_with_info, kpi_row, executive_summary_box, method_note, note_2025_if_relevant,
    fmt_amount, fmt_pct, pct_paren, directional_amount_str, ratio_kpi_label,
)
from src.formatting import bidi_isolate
from src.financial_metrics import get_year_metrics, get_aggregate_metrics, get_selection_change
from src.expense_analysis import employee_cost_analysis, employee_cost_analysis_for_years, group_totals_for_years
from src.narrative import build_executive_summary
from src import charts


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.executive_overview", t("app_subtitle", lang), period_label)

    section_title(t("summary.title", lang))
    executive_summary_box(build_executive_summary(loaded, selected_years, lang), lang=lang)
    note_2025_if_relevant(selected_years, lang)

    multi = len(selected_years) > 1
    change = get_selection_change(loaded, selected_years)

    if multi:
        agg = get_aggregate_metrics(loaded, selected_years)
        total_revenue, total_expenses, official_pl = agg.total_revenue, agg.total_expenses, agg.official_pl
        net_margin, exp_ratio = agg.net_result_margin, agg.expense_to_revenue_ratio
        emp = employee_cost_analysis_for_years(loaded, selected_years)
        # change is always available here: a multi-year selection always has
        # an earliest and a latest year to compare.
        connector = t("common.year_to_year_connector", lang)
        year_range = bidi_isolate(f"({change.base_year} {connector} {change.comparison_year})")
        method_note(t("agg.note", lang).format(year_range=year_range), lang=lang)
    else:
        m = get_year_metrics(loaded, selected_years[0])
        total_revenue, total_expenses, official_pl = m.total_revenue, m.total_expenses, m.official_pl
        net_margin, exp_ratio = m.net_result_margin, m.expense_to_revenue_ratio
        emp = employee_cost_analysis(loaded, selected_years[0])
        if change:
            year_range = bidi_isolate(str(change.base_year))
            method_note(t("agg.note_single_year", lang).format(year_range=year_range), lang=lang)

    break_even_gap = max(total_expenses - total_revenue, 0.0)

    def change_str(value, pct):
        if value is None:
            return None
        return f"{directional_amount_str(value, lang, compact=True)} {pct_paren(pct)}"

    revenue_delta_str = change_str(change.revenue_change, change.revenue_change_pct) if change else None
    expense_delta_str = change_str(change.expense_change, change.expense_change_pct) if change else None
    if change:
        pl_delta_class = "neutral" if change.pl_change == 0 else ("good" if change.pl_change > 0 else "critical")
        pl_delta_str = directional_amount_str(change.pl_change, lang, compact=True)
    else:
        pl_delta_str, pl_delta_class = None, "neutral"

    # --- Primary story: Revenue -> Expenses -> Result -> Break-even Gap ---
    kpi_row([
        dict(label=t("kpi.total_revenue", lang), value_str=fmt_amount(total_revenue, lang, compact=True), lang=lang,
             key="exec_revenue", delta_str=revenue_delta_str, delta_class="neutral", help_key="help.kpi_total_revenue"),
        dict(label=t("kpi.total_expenses", lang), value_str=fmt_amount(total_expenses, lang, compact=True), lang=lang,
             key="exec_expenses", delta_str=expense_delta_str, delta_class="neutral", help_key="help.kpi_total_expenses"),
        dict(label=t("kpi.official_pl", lang), value_str=fmt_amount(official_pl, lang, compact=True), lang=lang,
             key="exec_pl", delta_str=pl_delta_str, delta_class=pl_delta_class, help_key="help.kpi_official_pl",
             negative_value=official_pl < 0),
        dict(label=ratio_kpi_label("kpi.net_result_margin", multi, lang), value_str=fmt_pct(net_margin), lang=lang,
             key="exec_margin", help_key="help.kpi_net_result_margin", negative_value=(net_margin or 0) < 0),
        dict(label=t("kpi.break_even_gap", lang), value_str=fmt_amount(break_even_gap, lang, compact=True), lang=lang,
             key="exec_gap", help_key="help.kpi_break_even_gap"),
    ], n_cols=5)

    st.write("")
    years_sorted = sorted(selected_years)
    rev_vals = [loaded.year_totals[y].total_revenue for y in years_sorted]
    exp_vals = [loaded.year_totals[y].official_total_expenses for y in years_sorted]
    pl_vals = [loaded.year_totals[y].official_pl_amount for y in years_sorted]

    c1, c2 = st.columns(2)
    with c1:
        title_with_info(t("chart.revenue_vs_expenses", lang), lang, key="exec_rev_exp_chart", help_key="help.chart_revenue_vs_expenses")
        st.plotly_chart(charts.revenue_vs_expenses_chart(years_sorted, rev_vals, exp_vals, lang, show_title=False), use_container_width=True)
    with c2:
        title_with_info(t("chart.pl_trend", lang), lang, key="exec_pl_trend_chart", help_key="help.chart_pl_trend")
        st.plotly_chart(charts.pl_trend_chart(years_sorted, pl_vals, lang, show_title=False), use_container_width=True)

    # --- Cost concentration: where the money goes -------------------------
    title_with_info(t("chart.expense_composition", lang), lang, key="exec_expense_comp_chart", help_key="help.chart_expense_composition")
    grp = group_totals_for_years(loaded, selected_years)
    st.plotly_chart(
        charts.sorted_magnitude_bar_chart(
            grp["group_name_en" if lang == "en" else "group_name_ar"].tolist(),
            grp["amount"].tolist(),
            t("chart.expense_composition", lang), lang, height=420, show_title=False,
        ),
        use_container_width=True,
    )

    # --- Employee Costs: visible as a measured pattern, kept compact ------
    st.write("")
    kpi_row([
        dict(label=ratio_kpi_label("kpi.expense_to_revenue_ratio", multi, lang), value_str=fmt_pct(exp_ratio), lang=lang,
             key="exec_exp_ratio", help_key="help.kpi_expense_to_revenue_ratio", secondary=True),
        dict(label=t("kpi.employee_costs", lang), value_str=fmt_amount(emp.total_employee_costs, lang, compact=True), lang=lang,
             key="exec_emp_costs", help_key="help.kpi_employee_costs", secondary=True),
        dict(label=ratio_kpi_label("kpi.employee_costs_pct_revenue", multi, lang), value_str=fmt_pct(emp.employee_costs_pct_of_revenue), lang=lang,
             key="exec_emp_pct_rev", help_key="help.kpi_employee_costs_pct_revenue", secondary=True,
             delta_str=(t("employee.exceeds_revenue_note", lang) if (emp.employee_costs_pct_of_revenue or 0) > 1 else None),
             delta_class="critical"),
    ], n_cols=3)
