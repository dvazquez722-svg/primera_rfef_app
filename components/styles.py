"""
==========================================================
GLOBAL STYLES
==========================================================

Carga los estilos CSS globales de la aplicación.
"""

from pathlib import Path

import streamlit as st


# ==========================================================
# PATH
# ==========================================================

CSS_FILE = (
    Path(__file__)
    .parent.parent
    / "assets"
    / "css"
    / "style.css"
)


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css() -> None:
    """
    Carga la hoja de estilos global.
    """

    if not CSS_FILE.exists():

        return

    with open(
        CSS_FILE,
        encoding="utf-8"
    ) as file:

        css = file.read()

    st.markdown(

        f"<style>{css}</style>",

        unsafe_allow_html=True

    )