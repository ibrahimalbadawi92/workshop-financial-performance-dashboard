# -*- coding: utf-8 -*-
import re

from src.translations import STRINGS, t
from src import expense_mapping


def test_every_string_has_both_languages():
    missing = []
    for key, entry in STRINGS.items():
        if not entry.get("ar") or not entry.get("en"):
            missing.append(key)
    assert missing == [], f"Keys missing an ar/en translation: {missing}"


def test_t_returns_correct_language():
    assert t("nav.executive_overview", "en") == "Executive Overview"
    assert t("nav.executive_overview", "ar") == "نظرة تنفيذية"


def test_t_unknown_key_does_not_crash():
    assert t("this.key.does.not.exist", "en") == "this.key.does.not.exist"


def test_all_nav_pages_have_labels():
    nav_keys = [
        "nav.executive_overview", "nav.revenue_analysis", "nav.expense_analysis",
        "nav.pl_drivers", "nav.year_comparison", "nav.break_even", "nav.what_if", "nav.data_quality",
    ]
    for key in nav_keys:
        assert t(key, "en") != key
        assert t(key, "ar") != key


def test_management_group_names_bilingual():
    for group in expense_mapping.GROUPS.values():
        assert group.name_ar
        assert group.name_en


def test_no_company_identity_strings_anywhere_in_translations():
    forbidden = ["aljohani", "الجهني"]
    for key, entry in STRINGS.items():
        for lang, text in entry.items():
            low = str(text).lower()
            for term in forbidden:
                assert term not in low, f"Forbidden identity term {term!r} found in STRINGS[{key!r}][{lang!r}]"


def test_no_management_approved_phrasing_in_translations():
    # Per the privacy audit: the internal project's help/revenue text cited
    # "management's approved classification" / "management's instruction" as
    # the reason Earned Discount is revenue -- implying a real company's
    # internal policy. The public copy must describe this as this
    # dashboard's own accounting-treatment choice instead.
    forbidden_en = ["management's approved", "management's instruction", "management instruction"]
    for key, entry in STRINGS.items():
        text_en = str(entry.get("en", "")).lower()
        for phrase in forbidden_en:
            assert phrase not in text_en, f"Forbidden phrase {phrase!r} found in STRINGS[{key!r}]['en']"


def test_app_subtitle_discloses_synthetic_data():
    assert "synthetic" in t("app_subtitle", "en").lower()
    assert "اصطناعية" in t("app_subtitle", "ar")


def test_no_real_2025_provision_fact_in_translations():
    # The internal dashboard's real, company-specific fact was that 2025
    # excludes the end-of-service provision and depreciation. That exact
    # claim must not appear anywhere in the public copy.
    for key, entry in STRINGS.items():
        text_en = str(entry.get("en", ""))
        assert not re.search(r"end-of-service provision and depreciation", text_en, re.IGNORECASE), key
