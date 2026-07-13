"""
==========================================================
PAGE HEADER
==========================================================

Cabecera común para todas las páginas del dashboard.
"""

from datetime import date

import streamlit as st


# ==========================================================
# HEADER
# ==========================================================

def render_header(
    title: str,
    subtitle: str = "",
    icon: str = "",
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None
) -> None:

    col1, col2 = st.columns([5, 2])

    with col1:

        if icon:

            st.title(f"{icon} {title}")

        else:

            st.title(title)

        if subtitle:

            st.caption(subtitle)

    with col2:

        if fecha_inicio and fecha_fin:

            st.metric(

                label="Periodo",

                value=f"{fecha_inicio.strftime('%d/%m/%Y')} → {fecha_fin.strftime('%d/%m/%Y')}"

            )

        elif fecha_inicio:

            st.metric(

                label="Fecha",

                value=fecha_inicio.strftime("%d/%m/%Y")

            )

    st.divider()