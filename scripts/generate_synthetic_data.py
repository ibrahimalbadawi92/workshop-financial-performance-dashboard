# -*- coding: utf-8 -*-
"""
Generates the fully synthetic demo dataset for the public Portfolio version
of this dashboard.

This dataset is 100% independently authored. It is NOT derived from, scaled
from, or fitted to any real company's figures -- no real values, ratios,
trends, or account codes were used as an input anywhere in this script. It
exists only to give the dashboard's analytical features (multi-year KPIs,
loss/profit-driver analysis, break-even, what-if, data-quality checks) a
realistic, internally-consistent, and analytically interesting dataset to
demonstrate, for a fictional small workshop business.

Run: python scripts/generate_synthetic_data.py
Writes:
  data/synthetic_workshop_financial_data.csv   (account-level detail)
  data/synthetic_official_totals.csv           (year-level reported totals)
"""
import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

YEARS = list(range(2017, 2026))

# --- Independent year-level story ------------------------------------------
# Early pressure -> a first near-break-even/profitable year -> a downturn
# shock -> recovery -> a strong profitable year -> a cost-structure shift
# that thins the margin -> a mild pull-back into loss -> a recovery close.
# Deliberately NOT an all-loss dataset, and deliberately not shaped to
# resemble any particular real trend.
YEAR_TOTALS = {
    2017: dict(revenue=620_000, expenses=680_000),
    2018: dict(revenue=690_000, expenses=715_000),
    2019: dict(revenue=750_000, expenses=738_000),
    2020: dict(revenue=640_000, expenses=705_000),
    2021: dict(revenue=705_000, expenses=690_000),
    2022: dict(revenue=810_000, expenses=760_000),
    2023: dict(revenue=860_000, expenses=845_000),
    2024: dict(revenue=890_000, expenses=910_000),
    2025: dict(revenue=940_000, expenses=905_000),
}

# --- Revenue composition ----------------------------------------------------
# "Settlement Discount" (a secondary revenue classification, analogous to an
# earned/settlement discount treated as revenue) is intentionally NOT
# present in the earlier years and appears from 2020 onward -- an
# independent "not present vs zero" example on the revenue side.
REVENUE_ACCOUNTS = {
    "4001": {"name_en": "Workshop Revenue", "name_ar": "ايرادات الورشة"},
    "4002": {"name_en": "Other Revenue", "name_ar": "ايرادات متنوعة"},
    "4003": {"name_en": "Settlement Discount", "name_ar": "خصم تسوية"},
}


def revenue_rows_for_year(year, total_revenue):
    other = round(total_revenue * 0.06, 2)
    settlement = round(total_revenue * 0.03, 2) if year >= 2020 else None
    workshop = round(total_revenue - other - (settlement or 0.0), 2)
    rows = [("4001", workshop), ("4002", other)]
    if settlement is not None:
        rows.append(("4003", settlement))
    return rows


# --- Expense management groups (generic accounting concepts) ---------------
GROUPS = {
    "employee_costs": {"name_en": "Employee Costs", "name_ar": "تكاليف الموظفين"},
    "government_regulatory_fees": {"name_en": "Government & Regulatory Fees", "name_ar": "الرسوم الحكومية والتنظيمية"},
    "occupancy_facilities": {"name_en": "Occupancy & Facilities", "name_ar": "الإشغال والمرافق"},
    "maintenance_repairs": {"name_en": "Maintenance & Repairs", "name_ar": "الصيانة والإصلاحات"},
    "insurance": {"name_en": "Insurance (non-employee)", "name_ar": "التأمين"},
    "administrative_professional": {"name_en": "Administrative & Professional", "name_ar": "المصروفات الإدارية والمهنية"},
    "marketing_advertising": {"name_en": "Marketing & Advertising", "name_ar": "التسويق والإعلان"},
    "operating_supplies": {"name_en": "Operating Supplies & Materials", "name_ar": "المواد والمستلزمات التشغيلية"},
    "depreciation": {"name_en": "Depreciation", "name_ar": "الإهلاك"},
    "cogs": {"name_en": "Cost of Goods Sold", "name_ar": "تكلفة البضاعة المباعة"},
    "fines_penalties": {"name_en": "Fines & Penalties", "name_ar": "الغرامات والجزاءات"},
    "zakat": {"name_en": "Zakat", "name_ar": "الزكاة"},
    "other_discounts": {"name_en": "Other / Discounts", "name_ar": "أخرى / خصومات"},
}

# Baseline (unnormalized) weight per group -- normalized to the year's total
# expenses after per-year narrative nudges below.
BASE_GROUP_WEIGHTS = {
    "employee_costs": 8.5,
    "occupancy_facilities": 1.4,
    "maintenance_repairs": 0.9,
    "operating_supplies": 1.1,
    "cogs": 0.7,
    "government_regulatory_fees": 0.45,
    "administrative_professional": 0.6,
    "marketing_advertising": 0.22,
    "insurance": 0.22,
    "depreciation": 0.45,
    "fines_penalties": 0.07,
    "zakat": 0.12,
    "other_discounts": 0.15,
}

# Per-year multiplicative nudges telling the independent cost-structure story:
# sticky wages during the 2020 downturn, a facilities step-up from 2023 (the
# margin-thinning cost-structure shift), and a 2024 admin/marketing push
# during the cost-pressure / recovery-attempt years.
YEAR_GROUP_NUDGES = {
    2020: {"employee_costs": 1.08},
    2023: {"occupancy_facilities": 1.6, "maintenance_repairs": 1.15},
    2024: {"administrative_professional": 1.3, "marketing_advertising": 1.4},
    2025: {"employee_costs": 0.97, "marketing_advertising": 1.2},
}

# --- Employee Cost sub-components (Level 2 drill-down) ----------------------
EMPLOYEE_SUBGROUPS = {
    "salaries_wages": {"name_en": "Salaries & Wages", "name_ar": "الأجور والرواتب"},
    "allowances": {"name_en": "Housing & Vacation Allowances", "name_ar": "بدلات السكن والإجازة"},
    "employee_insurance": {"name_en": "Employee Insurance", "name_ar": "تأمين الموظفين"},
    "statutory_contributions": {"name_en": "Statutory Contributions (GOSI)", "name_ar": "الاشتراكات النظامية (التأمينات الاجتماعية)"},
    "government_workforce_fees": {"name_en": "Government Workforce Fees", "name_ar": "رسوم العمالة الحكومية"},
    "end_of_service": {"name_en": "End-of-Service Provision", "name_ar": "مخصص نهاية الخدمة"},
    "travel": {"name_en": "Travel & Transportation", "name_ar": "السفر والانتقالات"},
    "other_employee_related": {"name_en": "Other Employee-Related Costs", "name_ar": "تكاليف أخرى متعلقة بالموظفين"},
}

# Expense accounts: code -> (group, subgroup_or_None, name_en, name_ar, weight)
EXPENSE_ACCOUNTS = {
    # --- Employee Costs
    "5101": ("employee_costs", "salaries_wages", "Salaries & Wages", "الأجور والرواتب", 5.5),
    "5102": ("employee_costs", "allowances", "Housing Allowance", "بدل السكن", 0.75),
    "5103": ("employee_costs", "allowances", "Vacation Allowance", "بدل الإجازة", 0.45),
    "5104": ("employee_costs", "employee_insurance", "Employee Medical Insurance", "التأمين الطبي للموظفين", 0.55),
    "5105": ("employee_costs", "statutory_contributions", "GOSI Contributions", "الاشتراكات النظامية (التأمينات الاجتماعية)", 0.85),
    "5106": ("employee_costs", "government_workforce_fees", "Labor Office Fees", "رسوم مكتب العمل", 0.30),
    "5107": ("employee_costs", "government_workforce_fees", "Residency (Iqama) Fees", "رسوم الإقامة", 0.25),
    "5108": ("employee_costs", "end_of_service", "End-of-Service Provision", "مخصص نهاية الخدمة", 0.45),
    "5109": ("employee_costs", "travel", "Staff Travel & Transport", "سفر وانتقالات الموظفين", 0.22),
    "5110": ("employee_costs", "other_employee_related", "Overtime & Bonuses", "المكافآت والعمل الإضافي", 0.18),
    "5111": ("employee_costs", "other_employee_related", "Staff Meals", "وجبات الموظفين", 0.10),
    # "not present" demo account -- absent (no row) 2017-2020, appears 2021+
    "5112": ("employee_costs", "other_employee_related", "Staff Training & Development", "تدريب وتطوير الموظفين", 0.12),

    # --- Government & Regulatory Fees
    "5201": ("government_regulatory_fees", None, "Municipality Fees", "رسوم البلدية", 0.6),
    "5202": ("government_regulatory_fees", None, "Commercial Registration Fees", "رسوم السجل التجاري", 0.4),

    # --- Occupancy & Facilities
    "5301": ("occupancy_facilities", None, "Workshop Rent", "إيجار الورشة", 0.65),
    "5302": ("occupancy_facilities", None, "Electricity", "الكهرباء", 0.18),
    "5303": ("occupancy_facilities", None, "Water", "المياه", 0.07),
    "5304": ("occupancy_facilities", None, "Facility Maintenance", "صيانة المرافق", 0.10),

    # --- Maintenance & Repairs
    "5401": ("maintenance_repairs", None, "Equipment Maintenance", "صيانة المعدات", 0.5),
    "5402": ("maintenance_repairs", None, "Vehicle Maintenance", "صيانة المركبات", 0.35),
    "5403": ("maintenance_repairs", None, "Tools Maintenance", "صيانة الأدوات", 0.15),

    # --- Insurance (non-employee)
    "5501": ("insurance", None, "Vehicle Insurance", "تأمين المركبات", 0.6),
    "5502": ("insurance", None, "Property Insurance", "تأمين الممتلكات", 0.4),

    # --- Administrative & Professional
    "5601": ("administrative_professional", None, "Bank Charges", "رسوم بنكية", 0.12),
    "5602": ("administrative_professional", None, "Legal & Accounting Fees", "أتعاب قانونية ومحاسبية", 0.30),
    "5603": ("administrative_professional", None, "Office Supplies", "قرطاسية ومطبوعات", 0.13),
    "5604": ("administrative_professional", None, "Telephone & Internet", "هاتف وإنترنت", 0.15),
    # new account appearing mid-period (2021+): a growing SME adopting
    # software tooling -- an independent "new account" example
    "5605": ("administrative_professional", None, "Software Subscriptions", "اشتراكات برمجية", 0.10),
    # "not present vs zero" demo account: recorded as an actual zero in
    # 2019, present with a real amount only in 2023, absent every other year
    "5606": ("administrative_professional", None, "Legal & Settlement Fees", "رسوم قانونية وتسويات", 0.20),

    # --- Marketing & Advertising
    "5701": ("marketing_advertising", None, "Advertising & Promotion", "الدعاية والإعلان", 1.0),

    # --- Operating Supplies & Materials
    "5801": ("operating_supplies", None, "Workshop Supplies", "مستلزمات الورشة", 0.40),
    "5802": ("operating_supplies", None, "Safety Equipment", "معدات السلامة", 0.12),
    "5803": ("operating_supplies", None, "Fuel & Lubricants", "وقود وزيوت", 0.28),
    "5804": ("operating_supplies", None, "Packaging Materials", "مواد تغليف", 0.10),
    "5805": ("operating_supplies", None, "Freight & Shipping", "نقل وشحن", 0.10),

    # --- Depreciation
    "5901": ("depreciation", None, "Depreciation - Equipment", "إهلاك المعدات", 0.5),
    "5902": ("depreciation", None, "Depreciation - Vehicles", "إهلاك المركبات", 0.3),
    "5903": ("depreciation", None, "Depreciation - Furniture", "إهلاك الأثاث", 0.2),

    # --- Cost of Goods Sold
    "6001": ("cogs", None, "Cost of Goods Sold", "تكلفة البضاعة المباعة", 1.0),

    # --- Fines & Penalties
    "6101": ("fines_penalties", None, "Fines & Penalties", "غرامات وجزاءات", 1.0),

    # --- Zakat
    "6201": ("zakat", None, "Zakat", "الزكاة", 1.0),

    # --- Other / Discounts
    "6301": ("other_discounts", None, "Miscellaneous Expenses", "مصروفات متنوعة", 0.6),
    "6302": ("other_discounts", None, "Discounts Allowed", "خصومات مسموح بها", 0.4),
}

# Accounts that do not exist (no row at all) for a given year -- the
# "Not Present" side of the missing-vs-zero distinction.
NOT_PRESENT = {
    "5112": {2017, 2018, 2019, 2020},          # Staff Training & Development
    "5605": {2017, 2018, 2019, 2020},          # Software Subscriptions
    "5606": {2017, 2018, 2020, 2021, 2022, 2024, 2025},  # Legal & Settlement Fees (present only 2019 [as 0] and 2023)
    # Data Quality page demo: this account was not tracked as its own line
    # in the dataset's first year -- a completeness caveat about 2017, not
    # a recorded zero. (occupancy_facilities has 3 other accounts, so its
    # 2017 weight redistributes among those automatically.)
    "5304": {2017},                            # Facility Maintenance
}
# Accounts recorded as a genuine zero (a real row, amount 0.0) for a given
# year -- the "recorded zero" side of the missing-vs-zero distinction.
RECORDED_ZERO = {
    "5606": {2019},  # Legal & Settlement Fees: recorded zero in 2019
}


def expense_rows_for_year(year, total_expenses):
    nudges = YEAR_GROUP_NUDGES.get(year, {})
    group_weights = {g: w * nudges.get(g, 1.0) for g, w in BASE_GROUP_WEIGHTS.items()}
    weight_sum = sum(group_weights.values())
    group_dollars = {g: total_expenses * (w / weight_sum) for g, w in group_weights.items()}

    rows_by_group = {g: [] for g in GROUPS}
    for code, (group, subgroup, name_en, name_ar, weight) in EXPENSE_ACCOUNTS.items():
        rows_by_group[group].append(code)

    all_rows = []
    for group, codes in rows_by_group.items():
        target = group_dollars[group]

        # Handle fixed-amount demo accounts first (their dollar value is
        # independent of the group weight split), then distribute the
        # remainder across the group's regular accounts by relative weight.
        fixed_amounts = {}
        if "5606" in codes:
            if year in RECORDED_ZERO.get("5606", set()):
                fixed_amounts["5606"] = 0.0
            elif year not in NOT_PRESENT.get("5606", set()):
                fixed_amounts["5606"] = 18_500.0

        regular_codes = [c for c in codes if c not in fixed_amounts and year not in NOT_PRESENT.get(c, set())]
        remainder = target - sum(fixed_amounts.values())
        weight_sum_group = sum(EXPENSE_ACCOUNTS[c][4] for c in regular_codes)

        for c in regular_codes:
            w = EXPENSE_ACCOUNTS[c][4]
            all_rows.append((c, round(remainder * (w / weight_sum_group), 2)))
        for c, amt in fixed_amounts.items():
            all_rows.append((c, round(amt, 2)))

    return all_rows


# --- Data-quality demo: a nonstandard Official P/L row label in one year ---
# (an independent, fictional bookkeeping-template quirk -- not tied to any
# real company's records)
STANDARD_PL_LABEL_EN = "Net Profit / Loss"
STANDARD_PL_LABEL_AR = "صافي الربح / الخسارة"
NONSTANDARD_PL_YEAR = 2018
NONSTANDARD_PL_LABEL_EN = "Result"
NONSTANDARD_PL_LABEL_AR = "النتيجة"


def main():
    detail_rows = []
    totals_rows = []

    for year in YEARS:
        target = YEAR_TOTALS[year]
        rev_rows = revenue_rows_for_year(year, target["revenue"])
        exp_rows = expense_rows_for_year(year, target["expenses"])

        for code, amount in rev_rows:
            meta = REVENUE_ACCOUNTS[code]
            detail_rows.append({
                "year": year, "account_code": code, "account_name_en": meta["name_en"],
                "account_name_ar": meta["name_ar"], "account_type": "Revenue",
                "management_group": "", "amount": amount,
            })

        actual_expense_sum = 0.0
        for code, amount in exp_rows:
            group, subgroup, name_en, name_ar, _w = EXPENSE_ACCOUNTS[code]
            detail_rows.append({
                "year": year, "account_code": code, "account_name_en": name_en,
                "account_name_ar": name_ar, "account_type": "Expense",
                "management_group": group, "amount": amount,
            })
            actual_expense_sum += amount

        total_revenue = round(sum(a for _, a in rev_rows), 2)
        official_total_expenses = round(actual_expense_sum, 2)
        official_pl = round(total_revenue - official_total_expenses, 2)

        if year == NONSTANDARD_PL_YEAR:
            label_en, label_ar = NONSTANDARD_PL_LABEL_EN, NONSTANDARD_PL_LABEL_AR
        else:
            label_en, label_ar = STANDARD_PL_LABEL_EN, STANDARD_PL_LABEL_AR

        totals_rows.append({
            "year": year,
            "official_total_expenses": official_total_expenses,
            "official_pl_amount": official_pl,
            "official_pl_label_en": label_en,
            "official_pl_label_ar": label_ar,
        })

    detail_path = DATA_DIR / "synthetic_workshop_financial_data.csv"
    with detail_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "year", "account_code", "account_name_en", "account_name_ar",
            "account_type", "management_group", "amount",
        ])
        writer.writeheader()
        writer.writerows(detail_rows)

    totals_path = DATA_DIR / "synthetic_official_totals.csv"
    with totals_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "year", "official_total_expenses", "official_pl_amount",
            "official_pl_label_en", "official_pl_label_ar",
        ])
        writer.writeheader()
        writer.writerows(totals_rows)

    print(f"Wrote {len(detail_rows)} account rows -> {detail_path}")
    print(f"Wrote {len(totals_rows)} year totals -> {totals_path}")
    for year in YEARS:
        t = YEAR_TOTALS[year]
        print(f"  {year}: revenue={t['revenue']:>10,} expenses={t['expenses']:>10,} pl={t['revenue']-t['expenses']:>10,}")


if __name__ == "__main__":
    main()
