# -*- coding: utf-8 -*-
"""Session-state helpers: language + global year selection, shared by every page."""
import streamlit as st

from src.data_loader import load_workbook_model

DEFAULT_LANG = "en"


@st.cache_resource(show_spinner="Loading dataset…")
def get_cached_workbook():
    """Streamlit-level cache: the synthetic dataset is read from disk once
    per app process, not on every widget interaction."""
    return load_workbook_model()


def init_session_state():
    loaded = get_cached_workbook()
    all_years = sorted(loaded.year_totals.keys())

    if "lang" not in st.session_state:
        st.session_state["lang"] = DEFAULT_LANG
    if "selected_years" not in st.session_state:
        st.session_state["selected_years"] = all_years[:]  # default: all years
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "nav.executive_overview"
    if "base_year" not in st.session_state:
        st.session_state["base_year"] = all_years[-2] if len(all_years) >= 2 else all_years[0]
    if "comparison_year" not in st.session_state:
        st.session_state["comparison_year"] = all_years[-1]

    return loaded, all_years


def get_lang() -> str:
    return st.session_state.get("lang", DEFAULT_LANG)


def get_selected_years() -> list:
    years = st.session_state.get("selected_years", [])
    return sorted(years)
