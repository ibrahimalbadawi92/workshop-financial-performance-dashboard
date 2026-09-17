# -*- coding: utf-8 -*-
"""
Loader tests. These run entirely against the bundled synthetic CSVs in
data/ -- no external or confidential file is read anywhere in this suite.
"""
from pathlib import Path

import pytest

from src.data_loader import (
    ACCOUNTS_CSV_PATH, OFFICIAL_TOTALS_CSV_PATH, PROJECT_ROOT, get_loaded_workbook,
)


def test_data_files_exist_inside_project():
    assert ACCOUNTS_CSV_PATH.exists(), f"Synthetic data file missing at {ACCOUNTS_CSV_PATH}"
    assert OFFICIAL_TOTALS_CSV_PATH.exists(), f"Synthetic totals file missing at {OFFICIAL_TOTALS_CSV_PATH}"


def test_data_paths_are_project_relative_not_hardcoded():
    # The whole point of the public rewrite: no hardcoded Windows
    # user-profile path, no reference to any file outside this project
    # directory. PROJECT_ROOT is fine to live under a user's Desktop on a
    # dev machine -- what must never happen is a LITERAL path baked into
    # the source, which is what this checks (structurally, via the source
    # text, not by asserting anything about the current machine's path).
    import inspect
    import src.data_loader as dl
    src_code = inspect.getsource(dl)
    assert "C:\\Users" not in src_code
    assert "C:/Users" not in src_code
    assert "Desktop" not in src_code
    for p in (ACCOUNTS_CSV_PATH, OFFICIAL_TOTALS_CSV_PATH):
        assert str(PROJECT_ROOT) in str(p)


def test_loaded_workbook_has_nine_years():
    loaded = get_loaded_workbook(force_reload=True)
    assert sorted(loaded.year_totals.keys()) == list(range(2017, 2026))


def test_accounts_df_has_expected_columns():
    loaded = get_loaded_workbook()
    for col in ("year", "account_code", "account_code_base", "account_name_ar", "account_name_clean",
                "account_type", "amount"):
        assert col in loaded.accounts_df.columns


def test_revenue_and_expense_types_present():
    loaded = get_loaded_workbook()
    types = set(loaded.accounts_df["account_type"].unique())
    assert types == {"Revenue", "Expense"}
