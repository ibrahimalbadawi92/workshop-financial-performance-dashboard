# -*- coding: utf-8 -*-
"""
Reusable Streamlit UI building blocks for the executive dashboard. Keeps
every page visually consistent and keeps HTML/CSS out of the page modules.
"""
from pathlib import Path
from typing import Optional, Sequence

import streamlit as st

from src.translations import t, STRINGS
from src.formatting import format_amount_compact, format_amount_full, format_pct, bidi_isolate
from src import design_tokens as tokens

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def inject_global_styles(lang: str):
    """Injects the app's CSS. RTL is handled per-element, not via a <script>
    tag: HTML inserted through .innerHTML (which is how st.markdown's
    unsafe_allow_html renders) never executes embedded <script> tags, in
    every browser, by web-platform design. Every element this app marks
    with dir="{lang}" in its own markup (see page_header,
    executive_summary_box, note_box, etc.) is correctly mirrored by the
    browser's native handling of the dir HTML attribute -- no script
    involved -- and plain-Arabic text elsewhere right-aligns on its own via
    ordinary per-paragraph bidi auto-detection. Mixed Arabic+number
    fragments (a year range, a "(26.7%)") are the one case that needs help,
    and that's handled separately with literal Unicode isolate marks (see
    src.formatting.bidi_isolate), which need no script either."""
    css_path = ASSETS_DIR / "styles.css"
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_header(lang: str, title_key: str, subtitle: str, period_label: str):
    dir_attr = "rtl" if lang == "ar" else "ltr"
    st.markdown(
        f"""
        <div class="exec-header" dir="{dir_attr}">
          <div class="titles">
            <h1>{t(title_key, lang)}</h1>
            <p>{subtitle}</p>
          </div>
          <div class="period-badge">{t('selected_period', lang)}: {bidi_isolate(period_label)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


_HELP_SECTIONS = [
    ("definition", "help.section.definition"),
    ("calculation", "help.section.calculation"),
    ("how_to_read", "help.section.how_to_read"),
    ("notes", "help.section.notes"),
]


def _has_help_content(help_key: Optional[str]) -> bool:
    if not help_key:
        return False
    return any(f"{help_key}.{suffix}" in STRINGS for suffix, _ in _HELP_SECTIONS)


def info_popover(help_key: str, lang: str, key: str):
    """The reusable click-to-reveal help control: a small circular 'i'
    button that opens a native Streamlit popover panel (real click
    interaction with built-in dismiss-on-click-away -- not a browser hover
    tooltip). Renders only the Definition/Calculation/How to Read/Notes
    sections that actually have content for help_key; every section header
    and body string comes from the translation system (src.translations /
    src.help_translations), so language follows the app automatically."""
    with st.popover("i", key=key, width="content"):
        rendered_any = False
        for suffix, header_key in _HELP_SECTIONS:
            content_key = f"{help_key}.{suffix}"
            if content_key in STRINGS:
                content = t(content_key, lang).replace("\n", "  \n")
                st.markdown(f"**{t(header_key, lang)}**")
                st.markdown(content)
                rendered_any = True
        if not rendered_any:
            st.caption(t("common.na", lang))


def title_with_info(text: str, lang: str, key: str, help_key: Optional[str] = None):
    """A section/chart/table title with an inline info icon beside it --
    drop-in replacement for a bare section_title() call. Falls back to a
    plain section_title() when help_key has no registered content, so it's
    always safe to call."""
    if not _has_help_content(help_key):
        section_title(text)
        return
    with st.container(key=f"titleinfo_{key}", horizontal=True, gap="small", vertical_alignment="center"):
        section_title(text)
        info_popover(help_key, lang, key=f"pop_titleinfo_{key}")


def _delta_class(value: Optional[float], positive_is_good: bool = True) -> str:
    if value is None or value == 0:
        return "neutral"
    is_up = value > 0
    good = is_up if positive_is_good else not is_up
    return "good" if good else "critical"


def directional_amount_str(value: Optional[float], lang: str, compact: bool = True) -> str:
    """Amount with a directional arrow -- but a genuine zero gets NO arrow
    (neutral), never a misleading up/down glyph. Use alongside _delta_class()
    (or your own good/critical/neutral choice) for the color."""
    if value is None:
        return t("common.na", lang)
    if value == 0:
        return fmt_amount(0, lang, compact=compact)
    arrow = "▲" if value > 0 else "▼"
    return f"{arrow} {fmt_amount(value, lang, compact=compact)}"


def kpi_card(
    label: str,
    value_str: str,
    lang: str,
    key: str,
    delta_str: Optional[str] = None,
    delta_class: str = "neutral",
    help_key: Optional[str] = None,
    negative_value: bool = False,
    secondary: bool = False,
):
    """key must be unique among the KPI cards rendered on the same page --
    it names the Streamlit container (and so the CSS hook that makes it
    look like a card) and the info-popover beside its label.

    Note: value_str/delta_str are expected to already carry their own
    bidi_isolate() around any "(X%)"-style fragment (see pct_paren() and
    narrative.py) -- isolating the WHOLE mixed Arabic+number string would
    backfire: once the isolate's first strong character is Arabic, the
    isolate itself resolves RTL and the percent/parens inside it get
    reordered again. Only the pure-numeric sub-fragment should be isolated.
    """
    value_class = "kpi-value negative" if negative_value else "kpi-value"
    prefix = "kpis" if secondary else "kpip"
    with st.container(key=f"{prefix}_{key}", border=False, gap=None):
        if _has_help_content(help_key):
            with st.container(horizontal=True, gap="small", vertical_alignment="center"):
                st.markdown(f'<div class="kpi-label">{label}</div>', unsafe_allow_html=True)
                info_popover(help_key, lang, key=f"pop_{prefix}_{key}")
        else:
            st.markdown(f'<div class="kpi-label">{label}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{value_class}">{value_str}</div>', unsafe_allow_html=True)
        if delta_str:
            st.markdown(f'<div class="kpi-sub {delta_class}">{delta_str}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="kpi-sub-spacer">&nbsp;</div>', unsafe_allow_html=True)


def kpi_row(cards: Sequence[dict], n_cols: int = 4):
    cols = st.columns(n_cols)
    for i, card in enumerate(cards):
        with cols[i % n_cols]:
            kpi_card(**card)


def note_box(text: str, icon: str = "ℹ️", lang: Optional[str] = None):
    """lang is optional -- when given, the box gets a real dir="rtl"/"ltr"
    attribute on itself, which is what actually drives its RTL styling (see
    the .note-box[dir="rtl"] CSS rule); the plain Arabic text inside reads
    correctly either way via ordinary per-paragraph bidi auto-detection,
    dir= only affects the box's own padding/line-height treatment."""
    dir_attr = f' dir="{"rtl" if lang == "ar" else "ltr"}"' if lang else ""
    st.markdown(
        f'<div class="note-box"{dir_attr}><span class="icon">{icon}</span><span>{text}</span></div>',
        unsafe_allow_html=True,
    )


def method_note(text: str, lang: Optional[str] = None):
    dir_attr = f' dir="{"rtl" if lang == "ar" else "ltr"}"' if lang else ""
    st.markdown(f'<div class="method-note"{dir_attr}>{text}</div>', unsafe_allow_html=True)


def executive_summary_box(text: str, lang: Optional[str] = None):
    dir_attr = f' dir="{"rtl" if lang == "ar" else "ltr"}"' if lang else ""
    st.markdown(f'<div class="exec-summary"{dir_attr}>{text}</div>', unsafe_allow_html=True)


def analysis_year_badge(year: int, lang: str):
    """Break-Even and What-If both calculate from a single year chosen on
    the page itself, independent of the global multi-year Years filter.
    The page header's period badge still shows the *global* selection,
    which could otherwise read as if it drove these calculations -- this
    badge makes the actual basis explicit."""
    st.markdown(
        f'<div class="period-badge">{t("analysis_year", lang)}: {bidi_isolate(str(year))}</div>',
        unsafe_allow_html=True,
    )


def note_2025_if_relevant(years, lang: str):
    """Name kept for continuity with the underlying check (still keyed to a
    specific dataset year -- see src.data_validation); the banner text
    itself describes this synthetic dataset's own data-completeness note,
    not any particular calendar year's real-world meaning."""
    from src.data_validation import requires_completeness_caution_note
    if requires_completeness_caution_note(years):
        note_box(t("note.latest_body", lang), icon="⚠️", lang=lang)


def not_present_tag(lang: str) -> str:
    return f'<span class="not-present-tag">{t("compare.status_not_present", lang)}</span>'


def comparison_status_label(status: str, absolute_change: Optional[float], lang: str) -> str:
    """Bilingual-safe label for an account-level comparison status (see
    src.expense_analysis STATUS_*). "Normal" -- an account present in both
    years, the common case in these tables -- is never rendered blank: it
    is derived as Increased/Decreased from the sign of the change itself,
    so a table dominated by ordinary movers still shows a meaningful
    Status value in every row."""
    from src.expense_analysis import STATUS_NOT_PRESENT, STATUS_NEW, STATUS_ZERO_BASE
    if status == STATUS_NOT_PRESENT:
        return t("compare.status_not_present", lang)
    if status == STATUS_NEW:
        return t("compare.status_new", lang)
    if status == STATUS_ZERO_BASE:
        return t("compare.status_zero_base", lang)
    if absolute_change is not None and absolute_change > 0:
        return t("compare.status_increased", lang)
    if absolute_change is not None and absolute_change < 0:
        return t("compare.status_decreased", lang)
    return ""


def ratio_kpi_label(base_key: str, multi: bool, lang: str) -> str:
    """Label for a ratio KPI that is an aggregated-numerator/aggregated-
    denominator calculation over the selected period. The calculation never
    changes; for a multi-year selection the label switches to an explicit
    "cumulative ... of the period" variant so it reads as a period ratio,
    not an average of annual percentages. Falls back to the normal label if
    no "_cumulative" variant exists for base_key."""
    if multi:
        cumulative_key = f"{base_key}_cumulative"
        if cumulative_key in STRINGS:
            return t(cumulative_key, lang)
    return t(base_key, lang)


def fmt_amount(value, lang, compact=False):
    if value is None:
        return t("common.na", lang)
    if compact:
        return format_amount_compact(value, lang=lang) + (" ر.س" if lang == "ar" else " SAR")
    return format_amount_full(value, lang=lang)


def fmt_pct(value, decimals=1):
    return format_pct(value, decimals=decimals)


def pct_paren(value, decimals=1, na_text: str = "-") -> str:
    """'(26.7%)' as its own bidi-isolated fragment -- safe to concatenate
    after Arabic text without the '%' and parens reordering (see
    src.formatting.bidi_isolate)."""
    inner = format_pct(value, decimals=decimals) if value is not None else na_text
    return bidi_isolate(f"({inner})")


def period_label_for_years(years: Sequence[int]) -> str:
    years = sorted(years)
    if not years:
        return "-"
    if len(years) == 1:
        return str(years[0])
    if years == list(range(years[0], years[-1] + 1)) and len(years) > 2:
        return f"{years[0]}–{years[-1]}"
    return ", ".join(str(y) for y in years)
