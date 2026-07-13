
import pandas as pd
import streamlit as st

from utils.team_selector import (
    show_team_selector,
    get_selected_team
)

from utils.dimensions_help import (
    show_dimensions_help
)

from components.league_header import (
    show_league_header
)

from components.league_snapshot import (
    show_league_snapshot
)

from components.league_scatter import (
    show_league_scatter
)

from components.league_ranking import (
    show_league_ranking
)

from components.league_distribution import (
    show_league_distribution
)

from components.league_insights import (
    show_league_insights
)

from components.league_time_series import (
    show_league_time_series
)

from components.league_report import (
    show_league_report
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Análisis de Liga",

    page_icon="📊",

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

selected_team = get_selected_team()

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/team_summary.csv"
)

master_df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

numeric_columns = [

    col

    for col in df.columns

    if pd.api.types.is_numeric_dtype(

        df[col]

    )

]

# =====================================================
# PAGE
# =====================================================

show_league_header(

    df=df

)

show_league_snapshot(

    df=df,

    selected_team=selected_team,

    numeric_columns=numeric_columns

)

show_league_scatter(

    df=df,

    selected_team=selected_team,

    numeric_columns=numeric_columns

)

show_league_ranking(

    df=df,

    selected_team=selected_team,

    numeric_columns=numeric_columns

)

show_league_distribution(

    df=df,

    selected_team=selected_team,

    numeric_columns=numeric_columns

)

show_league_insights(

    df=df,

    selected_team=selected_team,

    numeric_columns=numeric_columns

)

show_league_time_series(

    master_df=master_df,

    selected_team=selected_team

)

show_league_report(

    team=selected_team

)
