import streamlit as st
import pandas as pd

from utils.dimensions_help import (
    show_dimensions_help
)

# =====================================================
# LOAD TEAMS
# =====================================================

@st.cache_data
def load_teams():

    df = pd.read_csv(

        "data/processed/team_summary.csv"

    )

    return sorted(

        df["Equipo"].unique()

    )


# =====================================================
# TEAM SELECTOR
# =====================================================

def show_team_selector():

    teams = load_teams()

    if "selected_team" not in st.session_state:

        st.session_state.selected_team = teams[0]

    st.sidebar.markdown("---")

    st.sidebar.markdown(

        "## ⚽ Tactical Analysis"

    )

    st.session_state.selected_team = st.sidebar.selectbox(

        "Equipo",

        teams,

        index=teams.index(

            st.session_state.selected_team

        ),

        key="global_team_selector"

    )

    st.sidebar.caption(

        f"Equipo seleccionado: {st.session_state.selected_team}"

    )

    st.sidebar.markdown("---")

    if st.sidebar.button(

        "📚 Dimensiones tácticas",

        use_container_width=True,

        key="sidebar_dimensions"

    ):

        show_dimensions_help()


# =====================================================
# GET TEAM
# =====================================================

def get_selected_team():

    return st.session_state.selected_team