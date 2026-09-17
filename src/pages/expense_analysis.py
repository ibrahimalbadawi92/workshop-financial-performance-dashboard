# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

from src.translations import t
from src.ui_components import (
    page_header, section_title, title_with_info, note_box, method_note, note_2025_if_relevant, fmt_amount, fmt_pct,
    ratio_kpi_label, kpi_row,
)
from src.expense_analysis import (
    group_totals_for_years, group_drilldown_for_years, top_n_expenses_for_years,
    expense_concentration, expense_heatmap_pivot, employee_cost_analysis_for_years,
)
from src import expense_mapping
from src import charts


def render(loaded, lang, selected_years, period_label):
    page_header(lang, "nav.expense_analysis", t("app_subtitle", lang), period_label)
    note_2025_if_relevant(selected_years, lang)

    years_sorted = sorted(selected_years)

    tab_group, tab_account = st.tabs([t("expense.view_group", lang), t("expense.view_account", lang)])

    with tab_group:
        title_with_info(t("expense.view_group", lang), lang, key="exp_group_view", help_key="help.table_expense_group_view")
        grp = group_totals_for_years(loaded, years_sorted)
        name_col = "group_name_en" if lang == "en" else "group_name_ar"
        st.plotly_chart(
            charts.sorted_magnitude_bar_chart(grp[name_col].tolist(), grp["amount"].tolist(),
                                               t("chart.expense_composition", lang), lang, height=460, show_title=False),
            use_container_width=True,
        )
        st.markdown(f"**{t('expense.drilldown_title', lang)}**")
        group_options = {row[name_col]: row["group_key"] for _, row in grp.iterrows()}
        chosen_label = st.selectbox(t("common.select", lang), options=list(group_options.keys()), key="group_drill_select")
        drill = group_drilldown_for_years(loaded, years_sorted, group_options[chosen_label]).copy()
        drill["amount"] = drill["amount"].map(lambda v: fmt_amount(v, lang))
        drill["share_of_group"] = drill["share_of_group"].map(lambda v: fmt_pct(v))
        drill = drill.rename(columns={
            "account_code_base": t("expense.account_code", lang), "account_name_clean": t("expense.account_name", lang),
            "amount": t("expense.metric_amount", lang), "share_of_group": t("expense.share_of_group", lang),
        })
        st.dataframe(drill, use_container_width=True, hide_index=True)

    with tab_account:
        title_with_info(t("expense.view_account", lang), lang, key="exp_account_view", help_key="help.table_expense_account_view")
        top_n = st.radio(" ", options=[5, 10], format_func=lambda n: t("expense.top5", lang) if n == 5 else t("expense.top10", lang),
                          horizontal=True, key="topn_radio", label_visibility="collapsed")
        top_df = top_n_expenses_for_years(loaded, years_sorted, n=top_n)
        title_with_info(t("chart.top_expenses", lang), lang, key="exp_top_n", help_key="help.chart_top_expenses")
        st.plotly_chart(
            charts.sorted_magnitude_bar_chart(top_df["account_name_clean"].tolist(), top_df["amount"].tolist(),
                                               t("chart.top_expenses", lang), lang, height=420, show_title=False),
            use_container_width=True,
        )
        conc = expense_concentration(loaded, years_sorted[-1])
        st.caption(t("expense.concentration_stat", lang).format(
            n=top_n, share=fmt_pct(conc["top5_share"] if top_n == 5 else conc["top10_share"]), year=years_sorted[-1]
        ))

        st.markdown(f"**{t('expense.select_account', lang)}**")
        all_expense = loaded.accounts_df[loaded.accounts_df.account_type == "Expense"]
        acct_options = (
            all_expense[["account_code_base", "account_name_clean"]].drop_duplicates().sort_values("account_name_clean")
        )
        label_map = {f"{r.account_name_clean} ({r.account_code_base})": r.account_code_base for r in acct_options.itertuples()}
        chosen = st.selectbox(t("common.select", lang), options=list(label_map.keys()), key="acct_trend_select")
        code = label_map[chosen]
        sub = all_expense[all_expense.account_code_base == code].set_index("year")["amount"]
        vals = [float(sub.get(y)) if y in sub.index else None for y in years_sorted]
        st.plotly_chart(charts.account_trend_chart(years_sorted, vals, chosen, lang), use_container_width=True)
        missing_years = [y for y, v in zip(years_sorted, vals) if v is None]
        if missing_years:
            st.caption(f"{t('compare.status_not_present', lang)}: {', '.join(str(y) for y in missing_years)}")

        title_with_info(t("chart.expense_heatmap", lang), lang, key="exp_heatmap", help_key="help.chart_expense_heatmap")
        metric_choice = st.radio(
            t("expense.select_metric", lang),
            options=["amount", "pct_of_expenses", "pct_of_revenue"],
            format_func=lambda k: {
                "amount": t("expense.metric_amount", lang),
                "pct_of_expenses": t("expense.metric_pct_expenses", lang),
                "pct_of_revenue": t("expense.metric_pct_revenue", lang),
            }[k],
            horizontal=True, key="heatmap_metric",
        )
        pivot = expense_heatmap_pivot(loaded, metric=metric_choice)
        pivot = pivot[[c for c in pivot.columns if c in years_sorted]]
        top_accounts = pivot.sum(axis=1, skipna=True).sort_values(ascending=False).head(20).index
        pivot = pivot.loc[top_accounts]
        labels = [f"{name}" for _, name in pivot.index]
        suffix = "" if metric_choice == "amount" else "%"
        z = pivot.values * (100 if metric_choice != "amount" else 1)
        st.plotly_chart(charts.expense_heatmap_chart(years_sorted, labels, z, lang, value_suffix=suffix, show_title=False), use_container_width=True)

    st.divider()
    section_title(t("employee.section_title", lang))
    emp = employee_cost_analysis_for_years(loaded, years_sorted)
    multi = len(years_sorted) > 1

    kpi_row([
        dict(label=t("kpi.employee_costs", lang), value_str=fmt_amount(emp.total_employee_costs, lang, compact=True), lang=lang,
             key="exp_emp_costs", help_key="help.kpi_employee_costs"),
        dict(label=ratio_kpi_label("kpi.employee_costs_pct_expenses", multi, lang), value_str=fmt_pct(emp.employee_costs_pct_of_expenses), lang=lang,
             key="exp_emp_pct_exp", help_key="help.kpi_employee_costs_pct_expenses"),
        dict(label=ratio_kpi_label("kpi.employee_costs_pct_revenue", multi, lang), value_str=fmt_pct(emp.employee_costs_pct_of_revenue), lang=lang,
             key="exp_emp_pct_rev", help_key="help.kpi_employee_costs_pct_revenue"),
    ], n_cols=3)

    if (emp.employee_costs_pct_of_revenue or 0) > 1:
        note_box(t("employee.exceeds_revenue_note", lang), icon="⚠️")

    title_with_info(t("chart.employee_subgroups", lang), lang, key="exp_emp_subgroups", help_key="help.chart_employee_subgroups")
    sub_name_col = "subgroup_name_en" if lang == "en" else "subgroup_name_ar"
    st.plotly_chart(
        charts.sorted_magnitude_bar_chart(
            emp.subgroup_totals[sub_name_col].tolist(), emp.subgroup_totals["amount"].tolist(),
            t("chart.employee_subgroups", lang), lang, height=380, show_title=False,
        ),
        use_container_width=True,
    )

    title_with_info(t("chart.employee_vs_revenue", lang), lang, key="exp_emp_vs_rev", help_key="help.chart_employee_vs_revenue")
    rev_vals = [loaded.year_totals[y].total_revenue for y in years_sorted]
    from src.expense_analysis import employee_cost_analysis as _emp_year
    emp_vals = [_emp_year(loaded, y).total_employee_costs for y in years_sorted]
    st.plotly_chart(charts.employee_vs_revenue_chart(years_sorted, rev_vals, emp_vals, lang, show_title=False), use_container_width=True)

    with st.expander(t("expense.drilldown_title", lang)):
        emp_drill = group_drilldown_for_years(loaded, years_sorted, "employee_costs").copy()
        emp_drill["amount"] = emp_drill["amount"].map(lambda v: fmt_amount(v, lang))
        emp_drill["share_of_group"] = emp_drill["share_of_group"].map(lambda v: fmt_pct(v))
        emp_drill = emp_drill.rename(columns={
            "account_code_base": t("expense.account_code", lang), "account_name_clean": t("expense.account_name", lang),
            "amount": t("expense.metric_amount", lang), "share_of_group": t("expense.share_of_group", lang),
        })
        st.dataframe(emp_drill, use_container_width=True, hide_index=True)

    note_box(t("employee.no_headcount_note", lang), icon="ℹ️")
    st.caption(t("employee.investigate_note", lang))
