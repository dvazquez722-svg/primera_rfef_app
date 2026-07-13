import streamlit as st

from utils.team_snapshot import (
    show_team_snapshot
)


# =====================================================
# LEAGUE SNAPSHOT
# =====================================================

def show_league_snapshot(

    df,

    selected_team,

    numeric_columns

):

    st.subheader("⚽ Snapshot del Equipo")

    st.caption(

        "Selecciona las métricas más relevantes para comparar el equipo con el resto de la competición."

    )

    show_team_snapshot(

        df=df,

        team=selected_team,

        mode="league",

        metrics=numeric_columns,

        columns=4

    )

    st.divider()