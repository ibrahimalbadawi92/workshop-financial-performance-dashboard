# -*- coding: utf-8 -*-
"""
Management-group mapping for the synthetic dataset's expense accounts.

This mapping is ANALYTICAL ONLY. It never changes, merges, or overwrites the
original source accounts. Every management-group total must remain drillable
back to the original account codes and amounts. The account codes and
category names here are entirely invented for this Portfolio demo (see
scripts/generate_synthetic_data.py) -- they do not correspond to any real
company's chart of accounts.
"""

from dataclasses import dataclass

import pandas as pd

from src.data_loader import ACCOUNTS_CSV_PATH


@dataclass(frozen=True)
class ManagementGroup:
    key: str
    name_ar: str
    name_en: str


GROUPS = {
    "employee_costs": ManagementGroup("employee_costs", "تكاليف الموظفين", "Employee Costs"),
    "government_regulatory_fees": ManagementGroup(
        "government_regulatory_fees", "الرسوم الحكومية والتنظيمية", "Government & Regulatory Fees"
    ),
    "occupancy_facilities": ManagementGroup("occupancy_facilities", "الإشغال والمرافق", "Occupancy & Facilities"),
    "maintenance_repairs": ManagementGroup("maintenance_repairs", "الصيانة والإصلاحات", "Maintenance & Repairs"),
    "insurance": ManagementGroup("insurance", "التأمين", "Insurance (non-employee)"),
    "administrative_professional": ManagementGroup(
        "administrative_professional", "المصروفات الإدارية والمهنية", "Administrative & Professional"
    ),
    "marketing_advertising": ManagementGroup("marketing_advertising", "التسويق والإعلان", "Marketing & Advertising"),
    "operating_supplies": ManagementGroup(
        "operating_supplies", "المواد والمستلزمات التشغيلية", "Operating Supplies & Materials"
    ),
    "depreciation": ManagementGroup("depreciation", "الإهلاك", "Depreciation"),
    "cogs": ManagementGroup("cogs", "تكلفة البضاعة المباعة", "Cost of Goods Sold"),
    "fines_penalties": ManagementGroup("fines_penalties", "الغرامات والجزاءات", "Fines & Penalties"),
    "zakat": ManagementGroup("zakat", "الزكاة", "Zakat"),
    "other_discounts": ManagementGroup("other_discounts", "أخرى / خصومات", "Other / Discounts"),
}

# account_code -> group_key. Built directly from the dataset's own
# management_group column so it can never silently drift out of sync with
# the CSV (tests/test_expense_mapping.py enforces full coverage).
_accounts_df = pd.read_csv(ACCOUNTS_CSV_PATH, dtype={"account_code": str})
_expense_rows = _accounts_df[_accounts_df["account_type"] == "Expense"]
ACCOUNT_TO_GROUP = dict(zip(_expense_rows["account_code"], _expense_rows["management_group"]))


# --------------------------------------------------------------------------
# Employee Cost sub-components (Level 2 drill-down inside Employee Costs).
# --------------------------------------------------------------------------
EMPLOYEE_COST_SUBGROUPS = {
    "salaries_wages": {
        "name_ar": "الأجور والرواتب",
        "name_en": "Salaries & Wages",
        "accounts": ["5101"],
    },
    "allowances": {
        "name_ar": "بدلات السكن والإجازة",
        "name_en": "Housing & Vacation Allowances",
        "accounts": ["5102", "5103"],
    },
    "employee_insurance": {
        "name_ar": "تأمين الموظفين",
        "name_en": "Employee Insurance",
        "accounts": ["5104"],
    },
    "statutory_contributions": {
        "name_ar": "الاشتراكات النظامية (التأمينات الاجتماعية)",
        "name_en": "Statutory Contributions (GOSI)",
        "accounts": ["5105"],
    },
    "government_workforce_fees": {
        "name_ar": "رسوم العمالة الحكومية",
        "name_en": "Government Workforce Fees",
        "accounts": ["5106", "5107"],
    },
    "end_of_service": {
        "name_ar": "مخصص نهاية الخدمة",
        "name_en": "End-of-Service Provision",
        "accounts": ["5108"],
    },
    "travel": {
        "name_ar": "السفر والانتقالات",
        "name_en": "Travel & Transportation",
        "accounts": ["5109"],
    },
    "other_employee_related": {
        "name_ar": "تكاليف أخرى متعلقة بالموظفين",
        "name_en": "Other Employee-Related Costs",
        "accounts": ["5110", "5111", "5112"],
    },
}


def get_group_for_account(account_code_base: str) -> str:
    if account_code_base not in ACCOUNT_TO_GROUP:
        raise KeyError(
            f"Account code {account_code_base!r} has no management-group mapping. "
            "Every expense account must be explicitly mapped -- refusing to guess."
        )
    return ACCOUNT_TO_GROUP[account_code_base]


def get_employee_cost_subgroup_for_account(account_code_base: str):
    for key, sub in EMPLOYEE_COST_SUBGROUPS.items():
        if account_code_base in sub["accounts"]:
            return key
    return None
