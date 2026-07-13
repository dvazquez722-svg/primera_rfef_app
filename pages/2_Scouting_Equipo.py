import pandas as pd
import streamlit as st


from src.team_summary import (
    build_team_summary
)

from utils.team_selector import (
    show_team_selector,
    get_selected_team
)

from utils.dimensions_help import (
    show_dimensions_help
)

from components.scouting_header import (
    show_header
)

from components.scouting_kpis import (
    show_kpis
)

from components.scouting_radar import (
    show_radar
)

from components.scouting_recent_form import (
    show_recent_form
)

from components.scouting_matches import (
    show_recent_matches
)

from components.scouting_report import (
    show_report
)

from utils.load_dynamic_team import (
    load_dynamic_team
)


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Scouting Equipo",

    page_icon="📋",

    layout="wide"

)

# =====================================================
# USER
# =====================================================

if "user" not in st.session_state:

    st.error("Sesión no iniciada.")

    st.stop()

user = st.session_state.user

# =====================================================
# TEAM SELECTOR
# =====================================================

show_team_selector()

team = get_selected_team()

# =====================================================
# LOAD DATA
# =====================================================

master_df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

# =====================================================
# LEAGUE SUMMARY
# =====================================================

df = build_team_summary(

    master_df

)

# =====================================================
# DATE FILTER
# =====================================================

master_df["Fecha"] = pd.to_datetime(master_df["Fecha"])

min_date = master_df["Fecha"].min()

max_date = master_df["Fecha"].max()

col1, col2 = st.columns(2)

with col1:

    start_date = st.date_input(

        "Desde",

        value=min_date.date(),

        min_value=min_date.date(),

        max_value=max_date.date(),

        key="start_date"

    )

with col2:

    end_date = st.date_input(

        "Hasta",

        value=max_date.date(),

        min_value=min_date.date(),

        max_value=max_date.date(),

        key="end_date"

    )

st.divider()


# =====================================================
# TEAM DATA
# =====================================================

team_stats, team_tactical, team_matches = load_dynamic_team(

    master_df,

    team,

    start_date,

    end_date

)

team_matches = team_matches.sort_values(

    "Fecha",
    
    ascending=False

)

# =====================================================
# PAGE
# =====================================================

show_header(

    team=team,

    team_stats=team_stats,

    team_tactical=team_tactical

)

st.divider()

show_kpis(

    team=team,

    df=df,

    team_stats=team_stats

)

st.divider()

show_radar(

    team=team,

    team_tactical=team_tactical

)

st.divider()

show_recent_form(

    team=team,

    team_matches=team_matches,

    league_df=df

)

st.divider()

show_recent_matches(

    team=team,
    team_matches=team_matches

)

st.divider()

show_report(

    team=team

)

st.divider()
