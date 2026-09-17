# -*- coding: utf-8 -*-
"""
Bilingual help content for the info-popover system (KPI cards, charts,
tables, sections). Merged into src.translations.STRINGS at import time so
every entry goes through the same t(key, lang) lookup as the rest of the
app's UI text -- nothing here is hardcoded ad hoc inside a page file.

Each help item is a set of sibling keys:
    help.<id>.definition
    help.<id>.calculation
    help.<id>.how_to_read
    help.<id>.notes
Only the sections that make sense for that item are present; the
info_popover() component in src.ui_components renders whichever exist.

Every formula described here matches the actual backend implementation in
src.financial_metrics / src.expense_analysis / src.scenario_analysis --
nothing is an external benchmark, an ideal ratio, or an estimated value.
This text describes the synthetic Portfolio-demo dataset only.
"""

HELP_STRINGS = {
    # --- Section header labels ------------------------------------------
    "help.section.definition": {"ar": "التعريف", "en": "Definition"},
    "help.section.calculation": {"ar": "طريقة الحساب", "en": "Calculation"},
    "help.section.how_to_read": {"ar": "كيفية القراءة", "en": "How to Read"},
    "help.section.notes": {"ar": "ملاحظات مهمة", "en": "Important Notes"},

    # ======================================================================
    # KPI cards
    # ======================================================================
    "help.kpi_total_revenue.definition": {
        "ar": "إجمالي الإيرادات المسجلة والمتعلقة بالورشة للفترة المحددة.",
        "en": "Total recorded workshop-related revenue for the selected period.",
    },
    "help.kpi_total_revenue.calculation": {
        "ar": "مجموع كل حسابات الإيرادات في مجموعة البيانات، وتشمل: ايرادات الورشة، ايرادات متنوعة، وخصم تسوية حيثما وُجد.",
        "en": "Sum of all revenue accounts in the dataset: Workshop Revenue, Other Revenue, and Settlement Discount, where present.",
    },
    "help.kpi_total_revenue.notes": {
        "ar": "يُصنَّف «خصم تسوية» ضمن الإيرادات في هذا النموذج التحليلي، ولا يُخصم من المصروفات.",
        "en": "\"Settlement Discount\" is treated as revenue in this analytical model -- it is not netted against expenses.",
    },

    "help.kpi_total_expenses.definition": {
        "ar": "إجمالي المصروفات المسجلة للسنة/الفترة المحددة.",
        "en": "Total recorded expenses for the selected year/period.",
    },
    "help.kpi_total_expenses.calculation": {
        "ar": "مجموع كل حسابات المصروفات المسجلة في مجموعة البيانات لتلك السنة.",
        "en": "Sum of all expense accounts recorded in the dataset for that year.",
    },
    "help.kpi_total_expenses.notes": {
        "ar": "الإجمالي الرسمي يُقارَن دائمًا مع مجموع الحسابات الفردية كتحقق تسوية مستقل.",
        "en": "The official total is always cross-checked against the sum of individual accounts as an independent reconciliation test.",
    },

    "help.kpi_official_pl.definition": {
        "ar": "النتيجة الصافية الرسمية المسجلة لهذه السنة/الفترة.",
        "en": "The official net result recorded for this year/period.",
    },
    "help.kpi_official_pl.calculation": {
        "ar": "إجمالي الإيرادات − إجمالي المصروفات.",
        "en": "Total Revenue − Total Expenses.",
    },
    "help.kpi_official_pl.notes": {
        "ar": "تُسوّي اللوحة هذا الرقم بشكل مستقل مقابل النتيجة الرسمية؛ راجع صفحة «جودة البيانات» لتفاصيل التسوية.",
        "en": "The dashboard independently reconciles this figure against the official result -- see the Data Quality page for the reconciliation detail.",
    },

    "help.kpi_net_result_margin.definition": {
        "ar": "صافي الربح/الخسارة كنسبة من الإيرادات.",
        "en": "Official Net Profit/Loss expressed as a share of revenue.",
    },
    "help.kpi_net_result_margin.calculation": {
        "ar": "صافي الربح / الخسارة ÷ إجمالي الإيرادات.",
        "en": "Official Net Profit/Loss ÷ Total Revenue.",
    },
    "help.kpi_net_result_margin.notes": {
        "ar": "نسبة سالبة تعني خسارة مسجلة مقارنة بالإيرادات؛ نسبة موجبة تعني ربحًا مسجلا. كلما ارتفعت النسبة، كانت النتيجة المسجلة أفضل رقميًا.",
        "en": "A negative percentage means a recorded loss relative to revenue; a positive percentage means a recorded profit. The higher the percentage, the better the recorded result, numerically.",
    },

    "help.kpi_expense_to_revenue_ratio.calculation": {
        "ar": "إجمالي المصروفات ÷ إجمالي الإيرادات.",
        "en": "Total Expenses ÷ Total Revenue.",
    },
    "help.kpi_expense_to_revenue_ratio.notes": {
        "ar": "مثال: 95% تعني أن الورشة سجّلت 0.95 ر.س من المصروفات مقابل كل 1.00 ر.س من الإيرادات (أي هامش ربح). عند اختيار عدة سنوات، تُحسب النسبة كإجمالي المصروفات المجمّع ÷ إجمالي الإيرادات المجمّع لكل السنوات معًا، وليست متوسط النسب السنوية الفردية.",
        "en": "Example: 95% means the workshop recorded SAR 0.95 of expenses for every SAR 1.00 of revenue (i.e. a profit margin). When multiple years are selected, the ratio is aggregated expenses ÷ aggregated revenue across those years combined -- not the average of the individual annual percentages.",
    },

    "help.kpi_break_even_gap.calculation": {
        "ar": "عند تجاوز المصروفات للإيرادات: إجمالي المصروفات − إجمالي الإيرادات (بحد أدنى صفر). القيمة صفر إذا كانت الإيرادات تساوي المصروفات أو تتجاوزها.",
        "en": "When expenses exceed revenue: Total Expenses − Total Revenue (floored at zero). The value is zero when revenue equals or exceeds expenses.",
    },
    "help.kpi_break_even_gap.notes": {
        "ar": "يمثل هذا الرقم مقدار الإيراد الإضافي المطلوب، عند بقاء المصروفات دون تغيير، للوصول حسابيًا إلى نتيجة صفرية (لا ربح ولا خسارة). قيمة صفر تعني أن الإيرادات بلغت نقطة التعادل بالفعل أو تجاوزتها. وهو احتساب حسابي بحت وليس توقعًا.",
        "en": "This is the additional revenue required, at unchanged expenses, to mathematically reach a zero profit/loss result. A value of zero means revenue has already reached or exceeded break-even. It is a purely mathematical figure, not a forecast.",
    },

    "help.kpi_employee_costs.definition": {
        "ar": "مجموعة تحليلية تجمع الحسابات المصنّفة كمصروفات متعلقة بالموظفين، وتشمل: الأجور/الرواتب، البدلات، التأمين الطبي، الاشتراكات النظامية (التأمينات الاجتماعية)، رسوم العمالة الحكومية، مصروف نهاية الخدمة، وبنود السفر/الانتقالات المتعلقة بالموظفين.",
        "en": "An analytical grouping combining the employee-related expense accounts: salaries/wages, allowances, medical insurance, GOSI/statutory contributions, government workforce fees, end-of-service expense, and employee-related travel items.",
    },
    "help.kpi_employee_costs.notes": {
        "ar": "لا تتوفر بيانات عدد الموظفين ضمن مجموعة البيانات، ولذلك لا تحتسب اللوحة تكلفة الموظف الواحد ولا تستنتج أن عدد الموظفين مرتفع بشكل غير مبرر.",
        "en": "No headcount data exists in the dataset, so the dashboard does not calculate cost per employee or conclude that staffing is excessive.",
    },

    "help.kpi_employee_costs_pct_revenue.calculation": {
        "ar": "تكاليف الموظفين ÷ إجمالي الإيرادات.",
        "en": "Employee Costs ÷ Total Revenue.",
    },
    "help.kpi_employee_costs_pct_revenue.notes": {
        "ar": "قيمة أعلى من 100% تعني أن تكاليف الموظفين وحدها تجاوزت إجمالي الإيرادات المسجلة.",
        "en": "A value above 100% means employee-related costs alone exceeded total recorded revenue.",
    },

    "help.kpi_employee_costs_pct_expenses.calculation": {
        "ar": "تكاليف الموظفين ÷ إجمالي المصروفات.",
        "en": "Employee Costs ÷ Total Expenses.",
    },
    "help.kpi_employee_costs_pct_expenses.notes": {
        "ar": "توضح هذه النسبة حصة تكاليف الموظفين من إجمالي المصروفات المسجلة، دون أي استنتاج بشأن كفاءة أو كفاية عدد الموظفين.",
        "en": "Shows employee-related costs as a share of total recorded expenses, without any conclusion about staffing efficiency or adequacy.",
    },

    "help.kpi_revenue_movement.calculation": {
        "ar": "إيرادات سنة المقارنة − إيرادات سنة الأساس.",
        "en": "Comparison Year Revenue − Base Year Revenue.",
    },
    "help.kpi_expense_movement.calculation": {
        "ar": "مصروفات سنة المقارنة − مصروفات سنة الأساس.",
        "en": "Comparison Year Expenses − Base Year Expenses.",
    },
    "help.kpi_pl_change.calculation": {
        "ar": "أثر تغير الإيرادات − أثر تغير المصروفات.",
        "en": "Revenue Change − Expense Change.",
    },
    "help.kpi_pl_change.notes": {
        "ar": "نتيجة موجبة تعني أن النتيجة الصافية تحسّنت رقميًا مقارنة بسنة الأساس (سواء بتراجع خسارة أو بزيادة ربح). نتيجة سالبة تعني تراجع النتيجة رقميًا.",
        "en": "A positive result means the net result improved numerically versus the base year (whether that is a narrowing loss or a growing profit). A negative result means the numerical result declined.",
    },

    # ======================================================================
    # Executive Overview charts
    # ======================================================================
    "help.chart_revenue_vs_expenses.definition": {
        "ar": "يقارن الإيرادات والمصروفات المسجلة حسب السنة.",
        "en": "Compares recorded revenue and expenses by year.",
    },
    "help.chart_revenue_vs_expenses.how_to_read": {
        "ar": "الأزرق = الإيرادات، الأخضر المزرق = المصروفات. عندما تتجاوز المصروفات الإيرادات في سنة ما، فذلك يدل على عجز تشغيلي في تلك السنة؛ وعندما تتجاوز الإيرادات المصروفات، فذلك يدل على نتيجة ربحية.",
        "en": "Blue = Revenue, Teal = Expenses. When expenses exceed revenue in a year, that indicates an operating shortfall that year; when revenue exceeds expenses, that indicates a profitable result.",
    },
    "help.chart_revenue_vs_expenses.notes": {
        "ar": "الأرقام مأخوذة مباشرة من السنوات المحددة في مجموعة البيانات.",
        "en": "Figures come directly from the selected years in the dataset.",
    },

    "help.chart_pl_trend.definition": {
        "ar": "يعرض صافي الربح/الخسارة الرسمي لكل سنة.",
        "en": "Shows the official annual net profit/loss.",
    },
    "help.chart_pl_trend.calculation": {
        "ar": "الإيرادات − المصروفات.",
        "en": "Revenue − Expenses.",
    },
    "help.chart_pl_trend.how_to_read": {
        "ar": "الأعمدة أعلى الصفر (خضراء) = ربح مسجل. الأعمدة أسفل الصفر (حمراء) = خسارة مسجلة. كلما طال العمود، كانت النتيجة (ربحًا أو خسارة) أكبر.",
        "en": "Bars above zero (green) = a recorded profit. Bars below zero (red) = a recorded loss. A longer bar means a larger result in that direction.",
    },

    "help.chart_expense_composition.definition": {
        "ar": "يجمّع الحسابات الأصلية في مجموعة البيانات ضمن مجموعات تحليلية لتسهيل التحليل.",
        "en": "Groups original dataset accounts into analytical categories for easier analysis.",
    },
    "help.chart_expense_composition.how_to_read": {
        "ar": "العمود الأطول = مبلغ مصروف تراكمي أكبر.",
        "en": "A longer bar = a larger cumulative expense amount.",
    },
    "help.chart_expense_composition.notes": {
        "ar": "التجميع تحليلي فقط؛ تبقى الحسابات الأصلية قابلة للتتبع بشكل منفصل عبر «عرض الحسابات الأصلية».",
        "en": "Grouping is analytical only. Original accounts remain separately traceable via the Original Account View.",
    },

    # ======================================================================
    # Revenue Analysis
    # ======================================================================
    "help.chart_revenue_trend.definition": {
        "ar": "يعرض إجمالي الإيرادات لكل سنة.",
        "en": "Shows total revenue for each year.",
    },
    "help.chart_revenue_trend.calculation": {
        "ar": "مجموع حسابات الإيرادات في كل سنة.",
        "en": "Sum of revenue accounts in each year.",
    },

    "help.chart_revenue_composition.definition": {
        "ar": "يوضح مكونات الإيرادات لكل سنة: ايرادات الورشة، ايرادات متنوعة، وخصم تسوية حيثما وُجد.",
        "en": "Shows the revenue components for each year: Workshop Revenue, Other Revenue, and Settlement Discount, where present.",
    },
    "help.chart_revenue_composition.notes": {
        "ar": "«خصم تسوية» غير موجود في السنوات الأولى من مجموعة البيانات (2017-2019)؛ ويظهر بدءًا من 2020 -- وهو مثال آخر على حالة «غير موجود» وليس صفرًا مسجلًا.",
        "en": "\"Settlement Discount\" is not present in the earliest years of the dataset (2017-2019); it appears from 2020 onward -- another example of a \"Not Present\" state, not a recorded zero.",
    },

    "help.table_revenue_comparison.definition": {
        "ar": "مقارنة مبالغ حسابات الإيرادات بين سنة الأساس وسنة المقارنة.",
        "en": "Compares revenue account amounts between the base year and the comparison year.",
    },
    "help.table_revenue_comparison.calculation": {
        "ar": "التغير المطلق = مبلغ سنة المقارنة − مبلغ سنة الأساس.\nنسبة التغير = التغير المطلق ÷ مبلغ سنة الأساس.",
        "en": "Absolute Change = Comparison Year amount − Base Year amount.\n% Change = Absolute Change ÷ Base Year amount.",
    },
    "help.table_revenue_comparison.notes": {
        "ar": "إذا لم يكن الحساب موجودًا في سنة الأساس، لا تُحتسب نسبة تغير مضلّلة، ويظهر بدلًا من ذلك «غير موجود في المصدر».",
        "en": "If the account did not exist in the base year, no potentially misleading percentage is calculated -- \"Not Present in Source\" is shown instead.",
    },

    # ======================================================================
    # Expense Analysis
    # ======================================================================
    "help.table_expense_group_view.definition": {
        "ar": "يلخّص حسابات المصروفات ضمن مجموعات تحليلية.",
        "en": "Summarizes expense accounts into analytical management groups.",
    },
    "help.table_expense_group_view.notes": {
        "ar": "هذا التجميع لا يُعدّل دليل الحسابات الأصلي بأي شكل؛ وهو طبقة تحليلية إضافية فقط.",
        "en": "This is not a modification of the original chart of accounts -- it is an additional analytical layer only.",
    },

    "help.table_expense_account_view.definition": {
        "ar": "يعرض حسابات المصروفات الأصلية من مجموعة البيانات دون استبدال هويتها المصدرية.",
        "en": "Displays original expense accounts from the dataset without replacing their source identity.",
    },

    "help.chart_top_expenses.definition": {
        "ar": "يرتّب حسابات المصروفات حسب المبلغ ضمن الفترة المحددة.",
        "en": "Ranks expense accounts by amount within the selected period.",
    },
    "help.chart_top_expenses.notes": {
        "ar": "لا يُستخدم أي معيار مرجعي خارجي أو حد افتراضي؛ الترتيب مبني فقط على المبالغ الفعلية المسجلة.",
        "en": "No arbitrary or external benchmark is used -- ranking is based only on the actual recorded amounts.",
    },

    "help.chart_expense_heatmap.definition": {
        "ar": "خريطة حرارية للمصروفات: الصفوف = حسابات المصروفات، الأعمدة = السنوات.",
        "en": "An expense heatmap: rows = expense accounts, columns = years.",
    },
    "help.chart_expense_heatmap.how_to_read": {
        "ar": "يمكن اختيار المقياس: المبلغ، % من إجمالي المصروفات، أو % من الإيرادات. شدة اللون تعكس الحجم النسبي فقط، ولا تعني تلقائيًا أن القيمة «جيدة» أو «سيئة».",
        "en": "A metric can be selected: SAR amount, % of total expenses, or % of revenue. Color intensity represents relative magnitude only -- it does not automatically mean \"good\" or \"bad\".",
    },

    "help.chart_employee_subgroups.definition": {
        "ar": "يوضح مكونات تكاليف الموظفين ضمن المجموعات الفرعية: الأجور والرواتب، بدلات السكن والإجازة، تأمين الموظفين، الاشتراكات النظامية (GOSI)، رسوم العمالة الحكومية، مخصص نهاية الخدمة، السفر والانتقالات، وتكاليف أخرى متعلقة بالموظفين.",
        "en": "Shows the components of Employee Costs across the sub-groups: Salaries & Wages, Housing & Vacation Allowances, Employee Insurance, Statutory Contributions (GOSI), Government Workforce Fees, End-of-Service Provision, Travel & Transportation, and Other Employee-Related Costs.",
    },

    "help.chart_employee_vs_revenue.definition": {
        "ar": "يقارن إجمالي الإيرادات المسجلة مع إجمالي تكاليف الموظفين لكل سنة.",
        "en": "Compares total recorded revenue against total employee-related costs, by year.",
    },
    "help.chart_employee_vs_revenue.how_to_read": {
        "ar": "عندما يكون خط تكاليف الموظفين أعلى من خط الإيرادات، فهذا يعني أن تكاليف الموظفين تجاوزت إيرادات الورشة في تلك السنة.",
        "en": "When the employee-cost line is above the revenue line, employee-related costs exceeded workshop revenue in that year.",
    },
    "help.chart_employee_vs_revenue.notes": {
        "ar": "لا يُفسَّر هذا كدليل على زيادة عدد الموظفين عن الحاجة.",
        "en": "This should not be interpreted as proof of excess headcount.",
    },

    # ======================================================================
    # P&L Drivers page
    # ======================================================================
    "help.chart_cost_driver_waterfall.definition": {
        "ar": "جسر بصري يوضح كيف تغيّرت المصروفات من سنة الأساس إلى سنة المقارنة عبر أكبر الحسابات تأثيرًا.",
        "en": "A visual bridge showing how total expenses moved from the base year to the comparison year, through the most impactful accounts.",
    },
    "help.chart_cost_driver_waterfall.how_to_read": {
        "ar": "يبدأ من إجمالي مصروفات سنة الأساس. كل عمود وسيط يوضح تغير حساب مصروف واحد: الزيادات تُضاف إلى الإجمالي، والانخفاضات تُخصم منه. ينتهي العمود الأخير بإجمالي مصروفات سنة المقارنة.\n\nدلالة الألوان: أحمر = زيادة، أخضر = انخفاض مسجل فعلي، رمادي محايد = الحساب غير موجود في سنة المقارنة، كحلي = إجمالي الفتح/الإغلاق.",
        "en": "Starts from total expenses in the Base Year. Each intermediate bar shows how one expense account changed: increases add to the total, decreases reduce it. The final bar equals the Comparison Year total.\n\nColor logic: red = increase, green = a genuine recorded decrease, neutral gray = the account is Not Present in the comparison year, navy = the opening/closing totals.",
    },
    "help.chart_cost_driver_waterfall.notes": {
        "ar": "الأعمدة الرمادية «غير موجود» لا تعني بالضرورة توفيرًا مؤكدًا في التكلفة؛ فالحساب غائب فقط عن بيانات سنة المقارنة.",
        "en": "Gray \"Not Present\" bars must not be interpreted as a confirmed cost saving -- the account is simply absent from the comparison year's data.",
    },

    "help.table_expense_movers.definition": {
        "ar": "يعرض حسابات المصروفات مرتبة حسب حجم التغير بين سنة الأساس وسنة المقارنة.",
        "en": "Lists expense accounts ranked by the size of their change between the base year and the comparison year.",
    },
    "help.table_expense_movers.calculation": {
        "ar": "التغير المطلق = مبلغ سنة المقارنة − مبلغ سنة الأساس.",
        "en": "Absolute Change = Comparison Year amount − Base Year amount.",
    },
    "help.table_expense_movers.notes": {
        "ar": "«غير موجود في المصدر» تعني أن صف الحساب غير موجود في بيانات تلك السنة، وهي ليست بالضرورة مساوية لصفر حقيقي.",
        "en": "\"Not Present\" means the account row does not exist in that year's data -- it is not automatically equivalent to a true recorded zero.",
    },

    # ======================================================================
    # Year Comparison page
    # ======================================================================
    "help.table_year_comparison_summary.definition": {
        "ar": "يقارن أهم المؤشرات المالية بين سنة الأساس وسنة المقارنة، حيث يمثل كل عمود سنة واحدة.",
        "en": "Compares the core financial KPIs between the base year and the comparison year -- each column represents one individual year.",
    },

    "help.table_year_comparison_detail.definition": {
        "ar": "مقارنة تفصيلية على مستوى الحساب بين سنة الأساس وسنة المقارنة.",
        "en": "A detailed, account-level comparison between the base year and the comparison year.",
    },
    "help.table_year_comparison_detail.calculation": {
        "ar": "التغير المطلق = مبلغ سنة المقارنة − مبلغ سنة الأساس.\nنسبة التغير = التغير المطلق ÷ مبلغ سنة الأساس.\nالحصة = مصروف الحساب ÷ إجمالي مصروفات تلك السنة.\nتغير الحصة = حصة سنة المقارنة − حصة سنة الأساس.",
        "en": "Absolute Change = Comparison Year amount − Base Year amount.\n% Change = Absolute Change ÷ Base Year amount.\nShare = account expense ÷ total expenses of that year.\nShare Change = Comparison Year share − Base Year share.",
    },
    "help.table_year_comparison_detail.notes": {
        "ar": "«غير موجود» و«صفر» حالتان مختلفتان: الأولى تعني غياب الحساب عن بيانات تلك السنة، والثانية تعني أن الحساب مسجّل فعليًا بقيمة صفر.",
        "en": "\"Not Present\" and \"Zero\" are different states: the first means the account is absent from that year's data; the second means the account is actually recorded with a zero value.",
    },

    # ======================================================================
    # Break-Even Analysis page
    # ======================================================================
    "help.breakeven_current_revenue.definition": {
        "ar": "إجمالي الإيرادات المسجلة لسنة التحليل المحددة في هذه الصفحة.",
        "en": "Total recorded revenue for the Analysis Year selected on this page.",
    },
    "help.breakeven_current_expenses.definition": {
        "ar": "إجمالي المصروفات المسجلة لسنة التحليل المحددة في هذه الصفحة.",
        "en": "Total recorded expenses for the Analysis Year selected on this page.",
    },
    "help.breakeven_current_result.definition": {
        "ar": "صافي الربح/الخسارة الرسمي لسنة التحليل المحددة. قيمة موجبة = ربح مسجل، وقيمة سالبة = خسارة مسجلة.",
        "en": "The official Net Profit/Loss for the selected Analysis Year. A positive value is a recorded profit; a negative value is a recorded loss.",
    },
    "help.breakeven_break_even_revenue.definition": {
        "ar": "مستوى الإيراد الذي يعادل إجمالي المصروفات الحالية، أي نقطة التعادل عند بقاء المصروفات دون تغيير. قد تكون الإيرادات الفعلية أعلى أو أقل من هذا المستوى.",
        "en": "The revenue level that equals current total expenses -- i.e. the break-even point at unchanged expenses. Actual revenue may already be above or below this level.",
    },
    "help.breakeven_break_even_revenue.calculation": {
        "ar": "عند بقاء المصروفات دون تغيير: إيراد نقطة التعادل = إجمالي المصروفات.",
        "en": "At unchanged expenses: Break-even Revenue = Total Expenses.",
    },

    "help.breakeven_required_revenue_increase.calculation": {
        "ar": "(إجمالي المصروفات − إجمالي الإيرادات) ÷ إجمالي الإيرادات، بحد أدنى صفر. تكون صفرًا عندما تكون الإيرادات عند نقطة التعادل أو أعلى منها.",
        "en": "(Total Expenses − Total Revenue) ÷ Total Revenue, floored at zero. This is zero when revenue is already at or above break-even.",
    },
    "help.breakeven_required_revenue_increase.notes": {
        "ar": "هذا احتساب حسابي بحت لسيناريو محتمل، وليس توقعًا ماليًا أو توصية إدارية.",
        "en": "This is a purely mathematical scenario, not a financial forecast or a management recommendation.",
    },

    "help.breakeven_required_expense_reduction.calculation": {
        "ar": "(إجمالي المصروفات − إجمالي الإيرادات) ÷ إجمالي المصروفات، بحد أدنى صفر. تكون صفرًا عندما تكون الإيرادات عند نقطة التعادل أو أعلى منها.",
        "en": "(Total Expenses − Total Revenue) ÷ Total Expenses, floored at zero. This is zero when revenue is already at or above break-even.",
    },
    "help.breakeven_required_expense_reduction.notes": {
        "ar": "هذا احتساب حسابي بحت لسيناريو محتمل، وليس توقعًا ماليًا أو توصية إدارية. لا تُفضّل اللوحة خيار زيادة الإيراد على خيار خفض المصروف أو العكس.",
        "en": "This is a purely mathematical scenario, not a financial forecast or a management recommendation. The dashboard does not favor the revenue-increase option over the expense-reduction option, or vice versa.",
    },

    # ======================================================================
    # What-If Scenario page
    # ======================================================================
    "help.whatif_revenue_slider.definition": {
        "ar": "نسبة زيادة افتراضية يحددها المستخدم لأغراض المحاكاة التحليلية فقط.",
        "en": "A user-defined assumption used for analytical simulation only.",
    },
    "help.whatif_revenue_slider.calculation": {
        "ar": "إيراد السيناريو = الإيراد الفعلي × (1 + نسبة زيادة الإيرادات المختارة).",
        "en": "Scenario Revenue = Actual Revenue × (1 + selected Revenue Increase %).",
    },
    "help.whatif_expense_slider.definition": {
        "ar": "نسبة خفض افتراضية يحددها المستخدم لأغراض المحاكاة التحليلية فقط.",
        "en": "A user-defined assumption used for analytical simulation only.",
    },
    "help.whatif_expense_slider.calculation": {
        "ar": "مصروفات السيناريو = المصروفات الفعلية × (1 − نسبة خفض المصروفات المختارة).",
        "en": "Scenario Expenses = Actual Expenses × (1 − selected Expense Reduction %).",
    },

    "help.whatif_scenario_pl.calculation": {
        "ar": "صافي ربح/خسارة السيناريو = إيراد السيناريو − مصروفات السيناريو.",
        "en": "Scenario Profit/Loss = Scenario Revenue − Scenario Expenses.",
    },
    "help.whatif_scenario_pl.notes": {
        "ar": "قيمة افتراضية للمحاكاة التحليلية فقط، وليست توقعًا أو هدفًا معتمدًا.",
        "en": "A hypothetical value for analytical simulation only -- not a forecast or an approved target.",
    },

    "help.chart_actual_vs_scenario.definition": {
        "ar": "يقارن القيم الفعلية المسجلة مع نتائج السيناريو الافتراضي الذي حدده المستخدم لسنة التحليل المختارة.",
        "en": "Compares the actual recorded values against the user-defined scenario outcome for the selected Analysis Year.",
    },
    "help.chart_actual_vs_scenario.calculation": {
        "ar": "صافي ربح/خسارة السيناريو = إيراد السيناريو − مصروفات السيناريو.",
        "en": "Scenario Profit/Loss = Scenario Revenue − Scenario Expenses.",
    },
    "help.chart_actual_vs_scenario.notes": {
        "ar": "هذا ليس توقعًا ماليًا، ولا ميزانية، ولا هدفًا معتمدًا، ولا توصية إدارية. القيم افتراضية بالكامل يحددها المستخدم.",
        "en": "This is not a forecast, not a budget, not an approved target, and not a recommendation. The values are entirely user-defined.",
    },

    # ======================================================================
    # Data Quality page
    # ======================================================================
    "help.dq_years_loaded.definition": {
        "ar": "عدد سنوات مجموعة البيانات التي تم تحميلها بنجاح في النموذج التحليلي.",
        "en": "The number of dataset years successfully loaded into the analytical model.",
    },
    "help.dq_sheets_loaded.definition": {
        "ar": "عدد ملفات البيانات المصدرية التي تمت قراءتها (تفاصيل الحسابات + الإجماليات الرسمية).",
        "en": "The number of source data files read (account detail + official totals).",
    },
    "help.dq_account_counts.definition": {
        "ar": "عدد حسابات الإيرادات وحسابات المصروفات الفريدة المكتشفة عبر كل سنوات مجموعة البيانات.",
        "en": "The number of unique revenue accounts and unique expense accounts detected across all years in the dataset.",
    },

    "help.dq_reconciliation_table.definition": {
        "ar": "يُظهر هذا الجدول، لكل سنة، تحقق التسوية المستقل الذي تجريه اللوحة مقابل النتيجة الرسمية.",
        "en": "This table shows, for each year, the independent reconciliation check the dashboard runs against the official result.",
    },
    "help.dq_reconciliation_table.how_to_read": {
        "ar": "total_revenue: إجمالي الإيرادات المحسوب من حسابات الإيرادات.\nofficial_total_expenses: إجمالي المصروفات كما ورد في مجموعة البيانات الرسمية.\ntotal_expenses_from_rows: إجمالي المصروفات المحسوب من جمع الحسابات الفردية (للتحقق من تطابقه مع الرقم أعلاه).\nexpenses_subtotal_diff: الفرق بين الاثنين أعلاه (يجب أن يكون قريبًا جدًا من الصفر).\nofficial_pl: صافي الربح/الخسارة الرسمي.\ncalculated_pl: صافي الربح/الخسارة المحسوب بشكل مستقل (الإيرادات − المصروفات).\nreconciliation_diff: الفرق بين official_pl و calculated_pl.\nstatus: PASS إذا كان الفرق ضمن هامش التقريب العشري المقبول، وإلا REVIEW.",
        "en": "total_revenue: Total revenue computed from the revenue accounts.\nofficial_total_expenses: Total expenses as recorded in the official-totals data.\ntotal_expenses_from_rows: Total expenses computed by summing the individual accounts (checked against the figure above).\nexpenses_subtotal_diff: The difference between the two above (should be effectively zero).\nofficial_pl: The official Net Profit/Loss.\ncalculated_pl: The independently calculated Net Profit/Loss (Revenue − Expenses).\nreconciliation_diff: The difference between official_pl and calculated_pl.\nstatus: PASS when that difference is within acceptable floating-point tolerance, otherwise REVIEW.",
    },

    "help.dq_label_note.definition": {
        "ar": "ملاحظة {year}: صف صافي الربح/الخسارة في مجموعة البيانات لهذه السنة يحمل التسمية غير القياسية «{label}» بدلًا من «صافي الربح / الخسارة». تم تصنيفه كصافي ربح/خسارة بناءً على موضعه ضمن مجموعة البيانات، مع الاحتفاظ بالتسمية الأصلية دون تعديل.",
        "en": "Note ({year}): the Official Profit/Loss row for that year in the dataset carries the non-standard label \"{label}\" instead of \"Net Profit / Loss\". It was classified as Profit/Loss based on its position in the dataset, and the original label was preserved without modification.",
    },
}
