# -*- coding: utf-8 -*-
"""
Display-only formatting helpers. Never round before calculating -- these
functions are for presentation of already-computed values only.
"""

from typing import Optional


def format_amount_compact(value: float, lang: str = "en") -> str:
    """K/M compact form for KPI cards. lang: 'en' or 'ar'."""
    if value is None:
        return "-"
    sign = "-" if value < 0 else ""
    v = abs(value)
    if lang == "ar":
        if v >= 1_000_000:
            return f"{sign}{v / 1_000_000:.2f} مليون"
        if v >= 1_000:
            return f"{sign}{v / 1_000:.1f} ألف"
        return f"{sign}{v:,.0f}"
    else:
        if v >= 1_000_000:
            return f"{sign}{v / 1_000_000:.2f}M"
        if v >= 1_000:
            return f"{sign}{v / 1_000:.1f}K"
        return f"{sign}{v:,.0f}"


def format_amount_full(value: float, lang: str = "en", parens_negative: bool = True) -> str:
    """Exact amount with currency, for tables/tooltips. Negative values shown
    in parentheses."""
    if value is None:
        return "-"
    currency = "ر.س" if lang == "ar" else "SAR"
    negative = value < 0
    v = abs(value)
    formatted = f"{v:,.2f}"
    if negative and parens_negative:
        body = f"({formatted} {currency})" if lang == "ar" else f"({currency} {formatted})"
    else:
        body = f"{formatted} {currency}" if lang == "ar" else f"{currency} {formatted}"
    return body


def format_pct(value: Optional[float], decimals: int = 1) -> str:
    if value is None:
        return "-"
    return f"{value * 100:.{decimals}f}%"


def format_reconciliation_value(value: float, zero_threshold: float = 0.005) -> str:
    """Plain (no-currency) 2-decimal formatting for the Data Quality
    reconciliation table. DISPLAY ONLY -- the raw float and the tolerance
    check that decides PASS/REVIEW (see src.data_loader / src.data_validation)
    are never touched by this function; it only decides how an
    already-validated number is printed. A value that is effectively zero
    at 2-decimal precision (e.g. floating-point noise like -0.0000000009)
    displays as a clean "0.00" instead of "-0.0000000009" or a stray
    "-0.00", so a PASS row never reads as if it carries a real difference.
    """
    if abs(value) < zero_threshold:
        return "0.00"
    return f"{value:,.2f}"


def bidi_isolate(s: str) -> str:
    """Wrap a numeric/Latin fragment (amount, percentage, year range, delta)
    in Unicode isolate marks (U+2066 LRI / U+2069 PDI) so it renders in its
    own left-to-right run wherever it lands -- inside an RTL Arabic
    sentence, a plain st.metric/st.caption in an RTL-styled page, anywhere.
    Plain Unicode characters, not HTML, so nothing can strip them (unlike
    <bdi>, which Streamlit's HTML sanitizer drops)."""
    return f"⁦{s}⁩"
