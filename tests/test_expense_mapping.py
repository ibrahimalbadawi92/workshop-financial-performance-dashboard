# -*- coding: utf-8 -*-
from src import expense_mapping
from src.data_loader import get_loaded_workbook


def test_management_group_names_bilingual():
    for group in expense_mapping.GROUPS.values():
        assert group.name_ar
        assert group.name_en


def test_employee_subgroup_names_bilingual():
    for sub in expense_mapping.EMPLOYEE_COST_SUBGROUPS.values():
        assert sub["name_ar"]
        assert sub["name_en"]


def test_every_expense_account_in_dataset_is_mapped():
    loaded = get_loaded_workbook()
    expense_codes = set(loaded.accounts_df.loc[loaded.accounts_df.account_type == "Expense", "account_code_base"])
    mapped_codes = set(expense_mapping.ACCOUNT_TO_GROUP.keys())
    assert expense_codes <= mapped_codes


def test_no_real_internal_account_codes_reused():
    # These are the internal (confidential) project's actual chart-of-accounts
    # codes, discovered during the privacy audit -- they must never appear
    # in this public project's synthetic mapping.
    real_internal_codes = {"31010101", "31010191", "31060002", "42030103"}
    public_codes = set(expense_mapping.ACCOUNT_TO_GROUP.keys())
    assert public_codes.isdisjoint(real_internal_codes)


def test_employee_cost_subgroup_lookup():
    assert expense_mapping.get_employee_cost_subgroup_for_account("5101") == "salaries_wages"
    assert expense_mapping.get_employee_cost_subgroup_for_account("9999") is None
