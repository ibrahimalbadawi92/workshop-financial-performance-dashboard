# -*- coding: utf-8 -*-
"""
Bilingual text registry. Every user-facing string in the app goes through
t(key, lang) so no page hardcodes duplicated copy in either language.

Portfolio / Data Privacy note: this project uses a fully synthetic dataset
(see scripts/generate_synthetic_data.py and the README). Every string below
describes that synthetic dataset and this project's own logic -- none of it
is derived from, or describes, any real company's records.
"""

STRINGS = {
    # --- App shell ---------------------------------------------------------
    "app_title": {"ar": "لوحة الأداء المالي للورشة", "en": "Workshop Financial Performance Dashboard"},
    "app_subtitle": {"ar": "دراسة حالة للملف المهني · بيانات اصطناعية بالكامل", "en": "Portfolio Case Study · Fully Synthetic Data"},
    "language": {"ar": "اللغة", "en": "Language"},
    "selected_period": {"ar": "الفترة المحددة", "en": "Selected Period"},
    "analysis_year": {"ar": "سنة التحليل", "en": "Analysis Year"},

    # --- Navigation ----------------------------------------------------------
    "nav.section": {"ar": "التنقل", "en": "Navigation"},
    "nav.executive_overview": {"ar": "نظرة تنفيذية", "en": "Executive Overview"},
    "nav.revenue_analysis": {"ar": "تحليل الإيرادات", "en": "Revenue Analysis"},
    "nav.expense_analysis": {"ar": "تحليل المصروفات", "en": "Expense Analysis"},
    "nav.pl_drivers": {"ar": "محركات الربح والخسارة", "en": "P&L Drivers"},
    "nav.year_comparison": {"ar": "مقارنة السنوات", "en": "Year Comparison"},
    "nav.break_even": {"ar": "تحليل نقطة التعادل", "en": "Break-Even Analysis"},
    "nav.what_if": {"ar": "تحليل السيناريوهات", "en": "What-If Scenario"},
    "nav.data_quality": {"ar": "جودة البيانات", "en": "Data Quality"},

    # --- Global filters ------------------------------------------------------
    "filters.years": {"ar": "السنوات", "en": "Years"},
    "filters.select_years": {"ar": "اختر سنة أو أكثر", "en": "Select one or more years"},
    "filters.all_years": {"ar": "كل السنوات", "en": "All Years"},
    "filters.base_year": {"ar": "سنة الأساس", "en": "Base Year"},
    "filters.comparison_year": {"ar": "سنة المقارنة", "en": "Comparison Year"},

    # --- KPI labels ------------------------------------------------------
    "kpi.total_revenue": {"ar": "إجمالي الإيرادات", "en": "Total Revenue"},
    "kpi.total_expenses": {"ar": "إجمالي المصروفات", "en": "Total Expenses"},
    "kpi.official_pl": {"ar": "صافي الربح / الخسارة", "en": "Official Net Profit / Loss"},
    "kpi.net_result_margin": {"ar": "هامش النتيجة الصافية", "en": "Net Result Margin"},
    "kpi.revenue_change": {"ar": "تغير الإيرادات", "en": "Revenue Change"},
    "kpi.expense_change": {"ar": "تغير المصروفات", "en": "Expense Change"},
    "kpi.expense_to_revenue_ratio": {"ar": "نسبة المصروفات إلى الإيرادات", "en": "Expense-to-Revenue Ratio"},
    "kpi.break_even_gap": {"ar": "فجوة نقطة التعادل", "en": "Break-even Gap"},
    "kpi.employee_costs": {"ar": "تكاليف الموظفين", "en": "Employee Costs"},
    "kpi.employee_costs_pct_revenue": {"ar": "تكاليف الموظفين / الإيرادات", "en": "Employee Costs / Revenue"},
    "kpi.employee_costs_pct_expenses": {"ar": "تكاليف الموظفين / المصروفات", "en": "Employee Costs / Total Expenses"},

    # Multi-year-only label variants: the underlying ratio is unchanged
    # (aggregated numerator / aggregated denominator) -- only the label
    # changes, to reduce the chance a reader mistakes a multi-year figure
    # for an average of annual percentages.
    "kpi.net_result_margin_cumulative": {"ar": "نسبة النتيجة الصافية إلى إيرادات الفترة", "en": "Cumulative Net Result Margin"},
    "kpi.expense_to_revenue_ratio_cumulative": {"ar": "نسبة المصروفات إلى إيرادات الفترة", "en": "Cumulative Expense-to-Revenue Ratio"},
    "kpi.employee_costs_pct_revenue_cumulative": {"ar": "نسبة تكاليف الموظفين إلى إيرادات الفترة", "en": "Cumulative Employee Costs / Revenue"},
    "kpi.employee_costs_pct_expenses_cumulative": {"ar": "نسبة تكاليف الموظفين إلى مصروفات الفترة", "en": "Cumulative Employee Costs / Expenses"},

    "kpi_def.total_revenue": {
        "ar": "مجموع كل بنود الإيرادات المسجلة في مجموعة البيانات (ايرادات الورشة + ايرادات متنوعة + خصم تسوية حيثما وجد).",
        "en": "Sum of every revenue line item recorded in the dataset (workshop revenue + other revenue + settlement discount, where present).",
    },
    "kpi_def.total_expenses": {
        "ar": "إجمالي المصروفات كما هو مسجل رسميًا للفترة.",
        "en": "Total Expenses as officially recorded for the period.",
    },
    "kpi_def.official_pl": {
        "ar": "صافي الربح / الخسارة الرسمي المسجل أو المحسوب لسنة البيانات، كما هو دون تعديل.",
        "en": "The official Profit/Loss recorded or calculated for that data year, unmodified.",
    },
    "kpi_def.net_result_margin": {
        "ar": "صافي الربح / الخسارة ÷ إجمالي الإيرادات.",
        "en": "Official Profit/Loss ÷ Total Revenue.",
    },
    "kpi_def.expense_to_revenue_ratio": {
        "ar": "إجمالي المصروفات ÷ إجمالي الإيرادات. يوضح مقدار المصروفات مقابل كل ريال من الإيراد.",
        "en": "Total Expenses ÷ Total Revenue. Shows the amount of expense incurred for each SAR of revenue.",
    },
    "kpi_def.break_even_gap": {
        "ar": "إجمالي المصروفات - إجمالي الإيرادات (بحد أدنى صفر). المبلغ المطلوب لتحقيق التعادل عند مستوى المصروفات الحالي.",
        "en": "Total Expenses - Total Revenue (floored at zero). The amount required to reach break-even at the current expense level.",
    },
    "kpi_def.employee_costs": {
        "ar": "مجموع كل الحسابات المصنّفة ضمن مجموعة \"تكاليف الموظفين\" التحليلية (رواتب، بدلات، تأمينات، اشتراكات نظامية، رسوم عمالة حكومية، نهاية خدمة، سفر).",
        "en": "Sum of every account classified under the \"Employee Costs\" analytical group (salaries, allowances, insurance, statutory contributions, government workforce fees, end-of-service, travel).",
    },
    "kpi_def.employee_costs_pct_revenue": {
        "ar": "إجمالي تكاليف الموظفين ÷ إجمالي الإيرادات. يوضح حجم التكاليف المرتبطة بالموظفين مقارنة بإيرادات الورشة.",
        "en": "Total Employee Costs ÷ Total Revenue. Shows employee-related costs relative to workshop revenue.",
    },
    "kpi_def.employee_costs_pct_expenses": {
        "ar": "إجمالي تكاليف الموظفين ÷ إجمالي المصروفات.",
        "en": "Total Employee Costs ÷ Total Expenses.",
    },

    "agg.sum_selected_period": {"ar": "إجمالي الفترة المحددة", "en": "Sum across selected period"},
    "agg.ratio_of_totals": {"ar": "نسبة الإجماليين المجمّعين", "en": "Ratio of aggregated totals"},
    "agg.latest_selected_year": {"ar": "آخر سنة محددة", "en": "Latest selected year"},
    "common.year_to_year_connector": {"ar": "إلى", "en": "to"},
    "agg.note_single_year": {
        "ar": "التغيرات المعروضة (▲/▼) هي بالمقارنة مع {year_range} (السنة السابقة مباشرة في مجموعة البيانات).",
        "en": "The changes shown (▲/▼) are versus {year_range}, the immediately preceding year in the dataset.",
    },
    "agg.note": {
        "ar": "عند اختيار أكثر من سنة، تُحسب المبالغ كإجمالي تراكمي، والنسب كنسبة إجمالي البسط إلى إجمالي المقام (وليس متوسط النسب السنوية). أما التغيرات المعروضة (▲/▼) فهي بالمقارنة بين أول سنة وآخر سنة ضمن الفترة المحددة {year_range}.",
        "en": "When multiple years are selected, amounts are cumulative totals and ratios are computed as aggregated numerator / aggregated denominator (not an average of annual percentages). The changes shown (▲/▼) compare the earliest to the latest selected year {year_range}.",
    },

    # --- Executive summary -----------------------------------------------
    "summary.title": {"ar": "الملخص التنفيذي", "en": "Executive Summary"},
    "summary.single_year": {
        "ar": "بلغت إيرادات الورشة في {year} نحو {revenue} مقابل مصروفات قدرها {expenses}، لتسجل الورشة خسارة قدرها {loss}. شكلت تكاليف الموظفين {emp_pct_exp} من إجمالي المصروفات و{emp_pct_rev} من الإيرادات.",
        "en": "In {year}, workshop revenue totaled {revenue} versus {expenses} of expenses, resulting in a recorded loss of {loss}. Employee-related costs represented {emp_pct_exp} of total expenses and {emp_pct_rev} of revenue.",
    },
    "summary.single_year_profit": {
        "ar": "بلغت إيرادات الورشة في {year} نحو {revenue} مقابل مصروفات قدرها {expenses}، محققة ربحًا قدره {profit}. شكلت تكاليف الموظفين {emp_pct_exp} من إجمالي المصروفات و{emp_pct_rev} من الإيرادات.",
        "en": "In {year}, workshop revenue totaled {revenue} versus {expenses} of expenses, resulting in a recorded profit of {profit}. Employee-related costs represented {emp_pct_exp} of total expenses and {emp_pct_rev} of revenue.",
    },
    "summary.multi_year": {
        "ar": "بلغ إجمالي إيرادات الورشة خلال الفترة المحددة ({years}) نحو {revenue} مقابل إجمالي مصروفات قدره {expenses}، بخسارة تراكمية قدرها {loss}. شكلت تكاليف الموظفين {emp_pct_exp} من إجمالي المصروفات في هذه الفترة.",
        "en": "Across the selected period ({years}), workshop revenue totaled {revenue} against {expenses} of expenses, a cumulative recorded loss of {loss}. Employee-related costs represented {emp_pct_exp} of total expenses over this period.",
    },
    "summary.multi_year_profit": {
        "ar": "بلغ إجمالي إيرادات الورشة خلال الفترة المحددة ({years}) نحو {revenue} مقابل إجمالي مصروفات قدره {expenses}، محققة ربحًا تراكميًا قدره {profit}. شكلت تكاليف الموظفين {emp_pct_exp} من إجمالي المصروفات في هذه الفترة.",
        "en": "Across the selected period ({years}), workshop revenue totaled {revenue} against {expenses} of expenses, a cumulative recorded profit of {profit}. Employee-related costs represented {emp_pct_exp} of total expenses over this period.",
    },

    # --- Charts ------------------------------------------------------------
    "chart.revenue_vs_expenses": {"ar": "الإيرادات مقابل المصروفات حسب السنة", "en": "Revenue vs Expenses by Year"},
    "chart.pl_trend": {"ar": "اتجاه صافي الربح / الخسارة", "en": "Official Profit/Loss Trend"},
    "chart.expense_composition": {"ar": "تركيبة المصروفات حسب المجموعة التحليلية", "en": "Expense Composition by Management Group"},
    "chart.employee_vs_revenue": {"ar": "تكاليف الموظفين مقابل الإيرادات", "en": "Employee Costs vs Revenue"},
    "chart.break_even_trend": {"ar": "اتجاه فجوة نقطة التعادل", "en": "Break-even Gap Trend"},
    "chart.top_expenses": {"ar": "أكبر بنود المصروفات", "en": "Top Expense Accounts"},
    "chart.expense_trend": {"ar": "اتجاه المصروف المختار", "en": "Selected Expense Trend"},
    "chart.expense_heatmap": {"ar": "خريطة حرارية للمصروفات", "en": "Expense Heatmap"},
    "chart.revenue_composition": {"ar": "تركيبة الإيرادات", "en": "Revenue Composition"},
    "chart.revenue_trend": {"ar": "اتجاه الإيرادات", "en": "Revenue Trend"},
    "chart.employee_subgroups": {"ar": "مكونات تكاليف الموظفين", "en": "Employee Cost Components"},
    "chart.cost_driver_waterfall": {"ar": "جسر التغير في المصروفات", "en": "Expense Change Bridge"},
    "chart.actual_vs_scenario": {"ar": "الفعلي مقابل السيناريو", "en": "Actual vs Scenario"},
    "axis.year": {"ar": "السنة", "en": "Year"},
    "axis.amount_sar": {"ar": "المبلغ (ر.س)", "en": "Amount (SAR)"},
    "legend.revenue": {"ar": "الإيرادات", "en": "Revenue"},
    "legend.expenses": {"ar": "المصروفات", "en": "Expenses"},
    "legend.employee_costs": {"ar": "تكاليف الموظفين", "en": "Employee Costs"},
    "legend.profit_loss": {"ar": "صافي الربح / الخسارة", "en": "Profit / Loss"},
    "legend.base_year": {"ar": "سنة الأساس", "en": "Base Year"},
    "legend.comparison_year": {"ar": "سنة المقارنة", "en": "Comparison Year"},
    "legend.actual": {"ar": "فعلي", "en": "Actual"},
    "legend.scenario": {"ar": "سيناريو", "en": "Scenario"},

    # --- Revenue analysis ---------------------------------------------------
    "revenue.workshop": {"ar": "ايرادات الورشة", "en": "Workshop Revenue"},
    "revenue.other": {"ar": "ايرادات متنوعة", "en": "Other Revenue"},
    "revenue.settlement_discount": {"ar": "خصم تسوية", "en": "Settlement Discount"},
    "revenue.classification_note": {
        "ar": "يُصنَّف \"خصم تسوية\" ضمن الإيرادات في هذه اللوحة، ولا يُخصم من المصروفات -- وهو خيار تصنيف محاسبي معتمد لهذا النموذج التحليلي، وليس معيارًا محاسبيًا عامًا.",
        "en": "\"Settlement Discount\" is classified as revenue in this dashboard and is not netted against expenses -- an accounting-treatment choice made for this analytical model, not a general accounting standard.",
    },

    # --- Expense analysis ----------------------------------------------------
    "expense.view_group": {"ar": "عرض المجموعات التحليلية", "en": "Management Group View"},
    "expense.view_account": {"ar": "عرض الحسابات الأصلية", "en": "Original Account View"},
    "expense.top5": {"ar": "أكبر 5 بنود", "en": "Top 5"},
    "expense.top10": {"ar": "أكبر 10 بنود", "en": "Top 10"},
    "expense.concentration_stat": {
        "ar": "تمثل أكبر {n} بنود مصروفات {share} من إجمالي المصروفات في {year}.",
        "en": "The top {n} expense categories represent {share} of total expenses in {year}.",
    },
    "expense.select_account": {"ar": "اختر حسابًا لعرض اتجاهه التاريخي", "en": "Select an account to view its historical trend"},
    "expense.select_metric": {"ar": "المقياس", "en": "Metric"},
    "expense.metric_amount": {"ar": "المبلغ (ر.س)", "en": "SAR Amount"},
    "expense.metric_pct_expenses": {"ar": "% من إجمالي المصروفات", "en": "% of Total Expenses"},
    "expense.metric_pct_revenue": {"ar": "% من الإيرادات", "en": "% of Revenue"},
    "expense.drilldown_title": {"ar": "الحسابات الأصلية ضمن هذه المجموعة", "en": "Original accounts within this group"},
    "expense.account_code": {"ar": "رقم الحساب", "en": "Account Code"},
    "expense.account_name": {"ar": "اسم الحساب", "en": "Account Name"},
    "expense.share_of_group": {"ar": "الحصة من المجموعة", "en": "Share of Group"},

    # --- Employee cost section ------------------------------------------------
    "employee.section_title": {"ar": "تحليل تكاليف الموظفين", "en": "Employee Cost Analysis"},
    "employee.salaries_wages": {"ar": "الأجور والرواتب", "en": "Salaries & Wages"},
    "employee.allowances": {"ar": "بدلات السكن والإجازة", "en": "Housing & Vacation Allowances"},
    "employee.insurance": {"ar": "تأمين الموظفين", "en": "Employee Insurance"},
    "employee.statutory": {"ar": "الاشتراكات النظامية (التأمينات الاجتماعية)", "en": "Statutory Contributions (GOSI)"},
    "employee.gov_fees": {"ar": "رسوم العمالة الحكومية", "en": "Government Workforce Fees"},
    "employee.end_of_service": {"ar": "مخصص نهاية الخدمة", "en": "End-of-Service Provision"},
    "employee.travel": {"ar": "السفر والانتقالات", "en": "Travel & Transportation"},
    "employee.other": {"ar": "تكاليف أخرى متعلقة بالموظفين", "en": "Other Employee-Related Costs"},
    "employee.no_headcount_note": {
        "ar": "لا تتوفر بيانات عدد الموظفين ضمن مجموعة البيانات، ولذلك لا يتم احتساب تكلفة الموظف الواحد ولا الاستنتاج بشأن كفاية عدد الموظفين.",
        "en": "Headcount data is not available in the dataset, so cost-per-employee is not calculated and no conclusion about staffing adequacy is drawn.",
    },
    "employee.exceeds_revenue_note": {
        "ar": "تجاوزت تكاليف الموظفين إيرادات الورشة خلال الفترة المحددة.",
        "en": "Employee-related costs exceeded workshop revenue over the selected period.",
    },
    "employee.investigate_note": {
        "ar": "قد ترغب الإدارة في مراجعة المحركات التشغيلية وراء تكاليف الموظفين.",
        "en": "Management may wish to investigate the operational drivers behind employee-related costs.",
    },

    # --- P&L drivers ----------------------------------------------------------
    "pl_drivers.page_question": {"ar": "ما الذي أدى إلى تغير الأداء المالي للورشة؟", "en": "What drove the change in workshop financial performance?"},
    "pl_drivers.revenue_component": {"ar": "أثر تغير الإيرادات", "en": "Revenue Movement"},
    "pl_drivers.expense_component": {"ar": "أثر تغير المصروفات", "en": "Expense Movement"},
    "pl_drivers.top_increases": {"ar": "أكبر الزيادات في المصروفات", "en": "Top Expense Increases"},
    "pl_drivers.top_decreases": {"ar": "أكبر الانخفاضات في المصروفات", "en": "Top Expense Decreases"},
    "loss.not_present_tooltip": {"ar": "غير موجود في سنة المقارنة", "en": "Not Present in comparison year"},
    "loss.not_present_disclaimer": {
        "ar": "هذا الحساب غير موجود في بيانات {year}، لذلك لا ينبغي تفسير الانخفاض الظاهر على أنه تخفيض مؤكد في التكلفة.",
        "en": "This account is not present in the {year} data; therefore, the apparent decrease should not be interpreted as a confirmed cost reduction.",
    },
    "loss.not_present_table_note": {
        "ar": "الصفوف المشار إليها بـ \"غير موجود في المصدر\" تعني أن الحساب غير موجود في بيانات سنة المقارنة؛ ولا ينبغي تفسير الفرق المحتسب على أنه تخفيض مؤكد في التكلفة.",
        "en": "Rows marked \"Not Present\" indicate an account absent from the comparison year's data; the calculated difference should not be interpreted as a confirmed cost reduction.",
    },
    "loss.largest_contributor": {
        "ar": "أكبر مساهم رقمي في تغير المصروفات بين {base} و{comparison} كان \"{account}\" بمبلغ {amount}.",
        "en": "The largest numerical contributor to the change in expenses between {base} and {comparison} was \"{account}\" at {amount}.",
    },

    # --- Year comparison -----------------------------------------------------
    "compare.title": {"ar": "مقارنة تفصيلية بين سنتين", "en": "Detailed Two-Year Comparison"},
    "compare.title_summary": {"ar": "مقارنة المؤشرات الرئيسية بين سنتين", "en": "Two-Year KPI Comparison"},
    "compare.title_detail": {"ar": "المقارنة التفصيلية على مستوى الحساب", "en": "Account-Level Comparison"},
    "compare.account": {"ar": "الحساب", "en": "Account"},
    "compare.base_amount": {"ar": "مبلغ سنة الأساس", "en": "Base Amount"},
    "compare.comparison_amount": {"ar": "مبلغ سنة المقارنة", "en": "Comparison Amount"},
    "compare.absolute_change": {"ar": "التغير المطلق", "en": "Absolute Change"},
    "compare.pct_change": {"ar": "نسبة التغير", "en": "% Change"},
    "compare.share_base": {"ar": "الحصة (سنة الأساس)", "en": "Share (Base Year)"},
    "compare.share_comparison": {"ar": "الحصة (سنة المقارنة)", "en": "Share (Comparison Year)"},
    "compare.share_change": {"ar": "تغير الحصة", "en": "Share Change"},
    "compare.status_new": {"ar": "حساب جديد", "en": "New"},
    "compare.status_not_present": {"ar": "غير موجود في المصدر", "en": "Not Present"},
    "compare.status_zero_base": {"ar": "أساس صفري", "en": "Zero Base"},
    "compare.status_increased": {"ar": "زيادة", "en": "Increased"},
    "compare.status_decreased": {"ar": "انخفاض", "en": "Decreased"},
    "compare.group": {"ar": "المجموعة", "en": "Group"},
    "compare.status": {"ar": "الحالة", "en": "Status"},

    # --- Break-even ----------------------------------------------------------
    "breakeven.current_revenue": {"ar": "الإيرادات الحالية", "en": "Current Revenue"},
    "breakeven.current_expenses": {"ar": "المصروفات الحالية", "en": "Current Expenses"},
    "breakeven.current_result": {"ar": "النتيجة الحالية (ربح/خسارة)", "en": "Current Result (Profit/Loss)"},
    "breakeven.break_even_revenue": {"ar": "إيراد نقطة التعادل", "en": "Break-even Revenue"},
    "breakeven.gap": {"ar": "فجوة نقطة التعادل", "en": "Break-even Gap"},
    "breakeven.required_revenue_increase_pct": {"ar": "نسبة زيادة الإيراد المطلوبة", "en": "Required Revenue Increase %"},
    "breakeven.required_expense_reduction_pct": {"ar": "نسبة خفض المصروفات المطلوبة", "en": "Required Expense Reduction %"},
    "breakeven.already_above": {"ar": "تم تجاوز نقطة التعادل لسنة التحليل هذه", "en": "Break-even has already been exceeded for this Analysis Year"},
    "breakeven.surplus_amount": {"ar": "فائض الإيراد فوق نقطة التعادل", "en": "Revenue surplus above break-even"},
    "breakeven.surplus_pct": {"ar": "نسبة الفائض فوق نقطة التعادل", "en": "Surplus % above break-even"},
    "breakeven.disclaimer": {
        "ar": "هذه احتسابات حسابية لنقطة التعادل بناءً على أرقام سنة واحدة، وليست توقعًا ماليًا. لا تُفضّل هذه اللوحة أحد الخيارين (زيادة الإيراد أو خفض المصروف) على الآخر.",
        "en": "These are mathematical break-even calculations based on a single year's figures, not a financial forecast. This dashboard does not recommend one option (revenue increase or expense reduction) over the other.",
    },

    # --- What-if ---------------------------------------------------------------
    "whatif.revenue_increase_pct": {"ar": "نسبة زيادة الإيرادات", "en": "Revenue Increase %"},
    "whatif.expense_reduction_pct": {"ar": "نسبة خفض المصروفات", "en": "Expense Reduction %"},
    "whatif.actual_section": {"ar": "البيانات الفعلية", "en": "Actual Data"},
    "whatif.scenario_section": {"ar": "السيناريو الافتراضي", "en": "User-Defined Scenario"},
    "whatif.reaches_break_even": {"ar": "يصل السيناريو إلى نقطة التعادل (أو يتجاوزها)", "en": "Scenario reaches (or stays above) break-even"},
    "whatif.does_not_reach": {"ar": "لا يصل السيناريو إلى نقطة التعادل", "en": "Scenario does not reach break-even"},
    "whatif.gap_remaining": {"ar": "الفجوة المتبقية حتى التعادل", "en": "Remaining gap to break-even"},

    # --- Dataset completeness note ---------------------------------------------
    "note.latest_title": {"ar": "ملاحظة اكتمال البيانات", "en": "Data Completeness Note"},
    "note.latest_body": {
        "ar": "تنبيه: بيانات 2017 لا تتضمن حساب \"صيانة المرافق\" كبند منفصل ضمن مجموعة البيانات، ولذلك يجب تفسير المقارنات التي تشمل هذه السنة بحذر.",
        "en": "Note: 2017 does not include a separate \"Facility Maintenance\" line item in the dataset. Comparisons involving that year should therefore be interpreted with caution.",
    },

    # --- Data quality ------------------------------------------------------------
    "dq.source_path": {"ar": "مسار ملف البيانات", "en": "Data File Path"},
    "dq.years_loaded": {"ar": "السنوات المحملة", "en": "Years Loaded"},
    "dq.sheets_loaded": {"ar": "ملفات البيانات المحملة", "en": "Data Files Loaded"},
    "dq.reconciliation_status": {"ar": "حالة التسوية", "en": "Reconciliation Status"},
    "dq.mapping_coverage": {"ar": "تغطية التصنيف التحليلي", "en": "Management Mapping Coverage"},
    "dq.account_counts": {"ar": "عدد الحسابات", "en": "Account Counts"},
    "dq.structural_warnings": {"ar": "تنبيهات هيكلية", "en": "Structural Warnings"},
    "dq.label_note_title": {"ar": "ملاحظة تسمية غير قياسية", "en": "Non-Standard Label Note"},
    "dq.limitation_note_title": {"ar": "ملاحظة اكتمال البيانات", "en": "Data Completeness Limitation"},
    "dq.test_status": {"ar": "حالة الاختبارات الآلية", "en": "Automated Test Status"},

    # --- Common ------------------------------------------------------------------
    "common.year": {"ar": "سنة", "en": "Year"},
    "common.years": {"ar": "سنوات", "en": "Years"},
    "common.select": {"ar": "اختر", "en": "Select"},
    "common.of": {"ar": "من", "en": "of"},
    "common.increase": {"ar": "زيادة", "en": "increase"},
    "common.decrease": {"ar": "انخفاض", "en": "decrease"},
    "common.na": {"ar": "غير متاح", "en": "N/A"},
    "common.other": {"ar": "أخرى", "en": "Other"},
    "common.methodology": {"ar": "منهجية الاحتساب", "en": "Methodology"},
    "common.definition": {"ar": "التعريف", "en": "Definition"},
    "common.formula": {"ar": "الصيغة", "en": "Formula"},
    "common.table_view": {"ar": "عرض جدولي", "en": "Table View"},
}

# The info-popover system's bilingual content lives in its own file
# (src/help_translations.py) for maintainability, but is merged into this
# same STRINGS dict at import time so it goes through the identical t()
# lookup as every other UI string -- one translation system, not two.
from src.help_translations import HELP_STRINGS  # noqa: E402
STRINGS.update(HELP_STRINGS)


def t(key: str, lang: str) -> str:
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(lang, entry.get("en", key))


NOT_PRESENT_IN_SOURCE_AR = "غير موجود في المصدر"
NOT_PRESENT_IN_SOURCE_EN = "Not Present in Source"
