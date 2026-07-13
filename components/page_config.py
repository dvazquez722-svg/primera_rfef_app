"""
==========================================================
PAGE CONFIGURATION
==========================================================

Configuración global de Streamlit.

Todas las páginas utilizarán este componente para evitar
duplicar la configuración.
"""

import streamlit as st

from config_v1.app_config import (
    APP_NAME,
    APP_ICON,
    PAGE_LAYOUT,
    SIDEBAR_STATE
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

def configure_page() -> None:
    """
    Configura la aplicación Streamlit.

    Debe llamarse una única vez al inicio
    del dashboard principal.
    """

    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE,
    )