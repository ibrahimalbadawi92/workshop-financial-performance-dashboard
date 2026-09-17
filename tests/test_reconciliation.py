# -*- coding: utf-8 -*-
import pytest

from src.data_loader import get_loaded_workbook
from src.data_validation import run_full_validation, account_status, check_expense_mapping_coverage


@pytest.fixture(scope="module")
def loaded():
    return get_loaded_workbook()


@pytest.fixture(scope="module")
def report(loaded):
    return run_full_validation(loaded)


def test_all_years_reconcile(report):
    failing = report.reconciliation_by_year[report.reconciliation_by_year["status"] != "PASS"]
    assert failing.empty, f"Years failing reconciliation: {failing['year'].tolist()}"


def test_reconciliation_diff_within_tolerance(report):
    assert (report.reconciliation_by_year["reconciliation_diff"].abs() < 0.5).all()


def test_expenses_subtotal_matches_sum_of_rows(report):
    assert (report.reconciliation_by_year["expenses_subtotal_diff"].abs() < 0.5).all()


def test_no_duplicate_codes(report):
    assert report.duplicate_codes_by_year == {}


def test_full_expense_mapping_coverage(loaded):
    unmapped = check_expense_mapping_coverage(loaded.accounts_df)
    assert unmapped == [], f"Expense accounts missing from management mapping: {unmapped}"


def test_2018_label_issue_reported(report):
    # The synthetic dataset's one non-standard Official P/L label lives in
    # 2018 ("Result" instead of "Net Profit / Loss") -- a fictional
    # bookkeeping-template quirk, unrelated to any real company's records.
    assert any("2018" in msg for msg in report.label_issues)
    assert any("Result" in msg for msg in report.label_issues)
    assert len(report.label_issues) == 1


def test_missing_vs_zero_legal_settlement_fees():
    # Legal & Settlement Fees (5606): recorded zero in 2019, present with a
    # nonzero amount only in 2023, not present in every other year.
    loaded = get_loaded_workbook()
    status_2019 = account_status(loaded.accounts_df, 2019, "5606")
    assert status_2019["status"] == "present"
    assert status_2019["amount"] == 0.0

    status_2023 = account_status(loaded.accounts_df, 2023, "5606")
    assert status_2023["status"] == "present"
    assert status_2023["amount"] > 0

    status_2017 = account_status(loaded.accounts_df, 2017, "5606")
    assert status_2017["status"] == "not_present"
    assert status_2017["amount"] is None


def test_missing_vs_zero_facility_maintenance_2017():
    # Facility Maintenance (5304): the Data Quality page's completeness-note
    # demo account -- not present in 2017, present in every later year.
    loaded = get_loaded_workbook()
    status_2017 = account_status(loaded.accounts_df, 2017, "5304")
    assert status_2017["status"] == "not_present"

    status_2018 = account_status(loaded.accounts_df, 2018, "5304")
    assert status_2018["status"] == "present"
    assert status_2018["amount"] > 0


def test_new_account_appears_mid_period_software_subscriptions():
    loaded = get_loaded_workbook()
    for year in (2017, 2018, 2019, 2020):
        assert account_status(loaded.accounts_df, year, "5605")["status"] == "not_present"
    for year in (2021, 2022, 2023, 2024, 2025):
        status = account_status(loaded.accounts_df, year, "5605")
        assert status["status"] == "present"
        assert status["amount"] > 0
