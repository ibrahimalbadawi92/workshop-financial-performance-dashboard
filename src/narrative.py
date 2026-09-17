# -*- coding: utf-8 -*-
"""
Rule-based executive summary text. Every number is pulled from the
validated backend -- nothing here is templated with hardcoded amounts, and
no external AI call is made.

Both the single-year and multi-year summaries branch on the sign of the
result (profit vs. loss) -- this dataset includes both profitable and
loss-making years, so the copy must never assume one direction.
"""
from src.data_loader import LoadedWorkbook
from src.financial_metrics import get_aggregate_metrics, get_year_metrics
from src.expense_analysis import employee_cost_analysis, employee_cost_analysis_for_years
from src.translations import t
from src.formatting import format_amount_full, format_pct, bidi_isolate
from src.ui_components import period_label_for_years


_bdi = bidi_isolate


def build_executive_summary(loaded: LoadedWorkbook, years, lang: str) -> str:
    years = sorted(years)
    if len(years) == 1:
        year = years[0]
        m = get_year_metrics(loaded, year)
        emp = employee_cost_analysis(loaded, year)
        revenue = _bdi(format_amount_full(m.total_revenue, lang=lang))
        expenses = _bdi(format_amount_full(m.total_expenses, lang=lang))
        emp_pct_exp = _bdi(format_pct(emp.employee_costs_pct_of_expenses))
        emp_pct_rev = _bdi(format_pct(emp.employee_costs_pct_of_revenue))
        if m.official_pl < 0:
            loss = _bdi(format_amount_full(abs(m.official_pl), lang=lang, parens_negative=False))
            return t("summary.single_year", lang).format(
                year=year, revenue=revenue, expenses=expenses, loss=loss,
                emp_pct_exp=emp_pct_exp, emp_pct_rev=emp_pct_rev,
            )
        else:
            profit = _bdi(format_amount_full(m.official_pl, lang=lang, parens_negative=False))
            return t("summary.single_year_profit", lang).format(
                year=year, revenue=revenue, expenses=expenses, profit=profit,
                emp_pct_exp=emp_pct_exp, emp_pct_rev=emp_pct_rev,
            )
    else:
        agg = get_aggregate_metrics(loaded, years)
        emp = employee_cost_analysis_for_years(loaded, years)
        revenue = _bdi(format_amount_full(agg.total_revenue, lang=lang))
        expenses = _bdi(format_amount_full(agg.total_expenses, lang=lang))
        emp_pct_exp = _bdi(format_pct(emp.employee_costs_pct_of_expenses))
        years_label = _bdi(period_label_for_years(years))
        if agg.official_pl < 0:
            loss = _bdi(format_amount_full(abs(agg.official_pl), lang=lang, parens_negative=False))
            return t("summary.multi_year", lang).format(
                years=years_label, revenue=revenue, expenses=expenses, loss=loss, emp_pct_exp=emp_pct_exp,
            )
        else:
            profit = _bdi(format_amount_full(agg.official_pl, lang=lang, parens_negative=False))
            return t("summary.multi_year_profit", lang).format(
                years=years_label, revenue=revenue, expenses=expenses, profit=profit, emp_pct_exp=emp_pct_exp,
            )
