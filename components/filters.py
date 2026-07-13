"""
==========================================================
GLOBAL FILTERS
==========================================================

Filtros globales utilizados por toda la aplicación.

Este componente únicamente crea la interfaz y devuelve
los filtros seleccionados.

No filtra DataFrames.
No realiza cálculos.

Toda la lógica irá posteriormente en los services.
"""

from dataclasses import dataclass
from datetime import date

import streamlit as st


# ==========================================================
# FILTER MODEL
# ==========================================================

@dataclass
class Filters:

    fecha_inicio: date | None

    fecha_fin: date | None

    jugador: str

    equipo: str

    competicion: str

    microciclo: str

    partido: str

    tipo_sesion: str


# ==========================================================
# GLOBAL FILTERS
# ==========================================================

def render_filters() -> Filters:

    st.sidebar.title("Filtros")

    fecha_inicio = st.sidebar.date_input(
        "Fecha inicio",
        value=None
    )

    fecha_fin = st.sidebar.date_input(
        "Fecha fin",
        value=None
    )

    st.sidebar.divider()

    jugador = st.sidebar.selectbox(
        "Jugador",
        ["Todos"]
    )

    equipo = st.sidebar.selectbox(
        "Equipo",
        ["Todos"]
    )

    competicion = st.sidebar.selectbox(
        "Competición",
        ["Todas"]
    )

    microciclo = st.sidebar.selectbox(
        "Microciclo",
        ["Todos"]
    )

    partido = st.sidebar.selectbox(
        "Partido",
        ["Todos"]
    )

    tipo_sesion = st.sidebar.selectbox(
        "Tipo de sesión",
        ["Todas"]
    )

    return Filters(

        fecha_inicio=fecha_inicio,

        fecha_fin=fecha_fin,

        jugador=jugador,

        equipo=equipo,

        competicion=competicion,

        microciclo=microciclo,

        partido=partido,

        tipo_sesion=tipo_sesion

    )