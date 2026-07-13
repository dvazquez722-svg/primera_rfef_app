"""
==========================================================
LAYOUT
==========================================================

Layout común para todas las páginas.
"""

import streamlit as st

from components.styles import load_css
from components.filters import render_filters


# ==========================================================
# MAIN LAYOUT
# ==========================================================

def render_layout():

    # -----------------------------
    # CSS
    # -----------------------------

    load_css()

    # -----------------------------
    # Sidebar
    # -----------------------------

    filters = render_filters()

    # -----------------------------
    # Página
    # -----------------------------

    page = st.session_state.get(

        "page",

        "Estado General"

    )

    return page, filters