# -*- coding: utf-8 -*-
"""
Workshop Financial Performance Dashboard -- Portfolio Case Study entry point.

This is a Portfolio demo built on a 100% synthetic dataset. See README.md
for the full Data Privacy Statement. Run with: streamlit run app.py
"""
import streamlit as st

from src.state import init_session_state, get_lang, get_selected_years
from src.translations import t
from src.ui_components import inject_global_styles, period_label_for_years

st.set_page_config(
    page_title="Workshop Financial Performance Dashboard | Portfolio Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

loaded, ALL_YEARS = init_session_state()
lang = get_lang()

inject_global_styles(lang)

NAV_ITEMS = [
    "nav.executive_overview",
    "nav.revenue_analysis",
    "nav.expense_analysis",
    "nav.pl_drivers",
    "nav.year_comparison",
    "nav.break_even",
    "nav.what_if",
    "nav.data_quality",
]


with st.sidebar:
    # No logo: a clean typographic header names this as a Portfolio case
    # study, not a real company's dashboard.
    st.markdown(
        """<div style="text-align:center;padding:10px 6px 16px 6px;">
        <div style="font-size:1.15rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.01em;">
        Workshop Financial<br/>Performance Dashboard</div>
        <div style="font-size:0.72rem;font-weight:600;color:#9FC7BC;text-transform:uppercase;
        letter-spacing:0.06em;margin-top:6px;">Portfolio Case Study</div>
        </div>""",
        unsafe_allow_html=True,
    )

    lang_choice = st.radio(
        t("language", lang), options=["en", "ar"],
        format_func=lambda x: "English" if x == "en" else "العربية",
        index=0 if lang == "en" else 1,
        horizontal=True, key="lang_radio",
    )
    if lang_choice != st.session_state["lang"]:
        st.session_state["lang"] = lang_choice
        st.rerun()

    st.markdown("---")

    nav_label = st.radio(
        t("nav.section", lang),
        options=NAV_ITEMS,
        format_func=lambda key: t(key, lang),
        index=NAV_ITEMS.index(st.session_state["nav_page"]) if st.session_state["nav_page"] in NAV_ITEMS else 0,
        key="nav_radio",
    )
    st.session_state["nav_page"] = nav_label

    st.markdown("---")
    st.markdown(f"**{t('filters.years', lang)}**")
    selected = st.multiselect(
        t("filters.select_years", lang), options=ALL_YEARS,
        default=st.session_state["selected_years"], key="year_multiselect",
        label_visibility="collapsed",
    )
    if not selected:
        selected = ALL_YEARS[:]
    st.session_state["selected_years"] = selected

    if st.button(t("filters.all_years", lang), use_container_width=True):
        st.session_state["selected_years"] = ALL_YEARS[:]
        st.rerun()

    if nav_label in ("nav.pl_drivers", "nav.year_comparison"):
        st.markdown("---")
        base_year = st.selectbox(
            t("filters.base_year", lang), options=ALL_YEARS,
            index=ALL_YEARS.index(st.session_state["base_year"]) if st.session_state["base_year"] in ALL_YEARS else 0,
            key="base_year_select",
        )
        comparison_year = st.selectbox(
            t("filters.comparison_year", lang), options=ALL_YEARS,
            index=ALL_YEARS.index(st.session_state["comparison_year"]) if st.session_state["comparison_year"] in ALL_YEARS else len(ALL_YEARS) - 1,
            key="comparison_year_select",
        )
        st.session_state["base_year"] = base_year
        st.session_state["comparison_year"] = comparison_year

    st.markdown("---")
    st.caption(
        "🔒 " + ("Synthetic data only -- see README" if lang == "en" else "بيانات اصطناعية بالكامل -- راجع README")
    )

selected_years = get_selected_years()
period_label = period_label_for_years(selected_years)

PAGE_DISPATCH = {
    "nav.executive_overview": "src.pages.executive_overview",
    "nav.revenue_analysis": "src.pages.revenue_analysis",
    "nav.expense_analysis": "src.pages.expense_analysis",
    "nav.pl_drivers": "src.pages.pl_drivers",
    "nav.year_comparison": "src.pages.yearly_comparison",
    "nav.break_even": "src.pages.break_even_analysis",
    "nav.what_if": "src.pages.what_if",
    "nav.data_quality": "src.pages.data_quality",
}

import importlib

module = importlib.import_module(PAGE_DISPATCH[st.session_state["nav_page"]])
module.render(loaded=loaded, lang=lang, selected_years=selected_years, period_label=period_label)
