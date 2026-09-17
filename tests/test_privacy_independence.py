# -*- coding: utf-8 -*-
"""
Privacy + independence guardrails for the public Portfolio project. These
tests encode the migration's hard requirements as regression tests, so a
future edit can't silently reintroduce a confidential reference:

- no reference to the real company name/brand anywhere in the source tree
- no hardcoded local/user path anywhere in the source tree
- no reference back to the internal project directory or the confidential
  workbook filename
- this suite runs, and the app's data model loads, using ONLY files inside
  this project directory
"""
import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
# Scans the shipped APPLICATION code only (src/ + app.py + conftest.py) --
# not tests/, since the guard tests below must legitimately name these
# forbidden terms as literal strings in order to check their absence
# elsewhere (e.g. "aljohani" appears in FORBIDDEN_CASE_INSENSITIVE itself).
SOURCE_DIRS = ["src"]
SOURCE_FILES = ["app.py", "conftest.py"]

FORBIDDEN_CASE_INSENSITIVE = [
    "aljohani",
    "الجهني",
    "قوائم الدخل للورشة",
]
FORBIDDEN_CASE_SENSITIVE = [
    "C:\\Users",
    "C:/Users",
    "workshop-financial-dashboard\\",  # the internal project's own folder name
    "workshop-financial-dashboard/src",
]


def _all_py_files():
    files = list(SOURCE_FILES)
    paths = [PROJECT_ROOT / f for f in files]
    for d in SOURCE_DIRS:
        paths.extend((PROJECT_ROOT / d).rglob("*.py"))
    return paths


ALL_PY_FILES = _all_py_files()


def test_scanned_at_least_the_expected_number_of_files():
    # Sanity check on the scanner: if this collapses to a tiny number, the
    # glob broke and every check below would be vacuous.
    assert len(ALL_PY_FILES) >= 20


@pytest.mark.parametrize("path", ALL_PY_FILES, ids=lambda p: str(p.relative_to(PROJECT_ROOT)))
def test_no_forbidden_identity_or_path_strings(path):
    text = path.read_text(encoding="utf-8")
    low = text.lower()
    for term in FORBIDDEN_CASE_INSENSITIVE:
        assert term not in low, f"Forbidden term {term!r} found in {path.relative_to(PROJECT_ROOT)}"
    for term in FORBIDDEN_CASE_SENSITIVE:
        assert term not in text, f"Forbidden path fragment {term!r} found in {path.relative_to(PROJECT_ROOT)}"


def test_no_py_file_imports_from_outside_this_project():
    # Every first-party import must resolve to this project's own src/ tree
    # (or a standard/third-party package) -- never a sys.path hack or a
    # relative "../workshop-financial-dashboard" reference.
    pattern = re.compile(r"^\s*(?:from|import)\s+([./\\A-Za-z0-9_]*(?:\.\.|internal)[./\\A-Za-z0-9_]*)", re.MULTILINE)
    for path in ALL_PY_FILES:
        text = path.read_text(encoding="utf-8")
        assert not pattern.search(text), f"Suspicious cross-project import in {path}"


def test_data_loader_reads_only_files_inside_project_root():
    from src.data_loader import ACCOUNTS_CSV_PATH, OFFICIAL_TOTALS_CSV_PATH, PROJECT_ROOT as DL_ROOT
    assert PROJECT_ROOT.resolve() == DL_ROOT.resolve()
    assert ACCOUNTS_CSV_PATH.resolve().is_relative_to(DL_ROOT.resolve())
    assert OFFICIAL_TOTALS_CSV_PATH.resolve().is_relative_to(DL_ROOT.resolve())


def test_no_real_internal_account_codes_in_synthetic_data():
    data_csv = PROJECT_ROOT / "data" / "synthetic_workshop_financial_data.csv"
    text = data_csv.read_text(encoding="utf-8")
    for real_code in ("31010101", "31010191", "31060002", "42030103", "41020101", "42030102"):
        assert real_code not in text, f"Real internal account code {real_code} found in synthetic data"


def test_official_totals_do_not_reuse_the_real_2019_nonstandard_label():
    # "الورشة" is legitimately used throughout this project as the generic
    # Arabic word for "workshop" (e.g. "ايرادات الورشة" / Workshop Revenue) --
    # that is not the confidential fact. The confidential fact was that the
    # real company's Official P/L ROW LABEL for 2019 was replaced with
    # exactly that bare word instead of "Net Profit / Loss". This dataset's
    # own nonstandard-label demo (2018) must use a different, unrelated
    # label ("Result" / "النتيجة"), never that one.
    totals_csv = PROJECT_ROOT / "data" / "synthetic_official_totals.csv"
    text = totals_csv.read_text(encoding="utf-8")
    assert ",الورشة," not in text
    assert ",2019,الورشة" not in text
