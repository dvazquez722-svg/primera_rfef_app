import pandas as pd
import streamlit as st

from utils.team_selector import (
    show_team_selector,
    get_selected_team
)

from utils.dimensions_help import (
    show_dimensions_help
)

from src.team_summary import (
    build_team_summary
)

from utils.load_dynamic_team import (
    load_dynamic_team
)

from components.comparison_header import (
    show_comparison_header
)

from components.comparison_face_to_face import (
    show_face_to_face
)

from components.comparison_radar import (
    show_comparison_radar
)

from components.comparison_kpis import (
    show_comparison_kpis
)

from components.comparison_scatter import (
    show_comparison_scatter
)

from components.comparison_similarity import (
    show_comparison_similarity
)

from components.comparison_report import (
    show_comparison_report
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Comparación de Equipos",

    page_icon="⚔️",

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

team_a = get_selected_team()

# =====================================================
# LOAD DATA
# =====================================================

master_df = pd.read_csv(

    "data/processed/master_team_stats.csv"

)

summary = build_team_summary(

    master_df

)

teams = sorted(

    summary["Equipo"].unique()

)

default_index = 1 if len(teams) > 1 else 0

team_b = st.selectbox(

    "Equipo a comparar",

    teams,

    index=default_index

)

if team_a == team_b:

    st.warning(

        "Selecciona dos equipos diferentes."

    )

    st.stop()

# =====================================================
# DATE FILTER
# =====================================================

master_df["Fecha"] = pd.to_datetime(

    master_df["Fecha"]

)

min_date = master_df["Fecha"].min()

max_date = master_df["Fecha"].max()

col1, col2 = st.columns(2)

with col1:

    start_date = st.date_input(

        "Desde",

        value=min_date.date(),

        min_value=min_date.date(),

        max_value=max_date.date(),

        key="comparison_start"

    )

with col2:

    end_date = st.date_input(

        "Hasta",

        value=max_date.date(),

        min_value=min_date.date(),

        max_value=max_date.date(),

        key="comparison_end"

    )

st.divider()

# =====================================================
# TEAM DATA
# =====================================================

teamA_summary, teamA_tactical, teamA_matches = load_dynamic_team(

    master_df,

    team_a,

    start_date,

    end_date

)

teamB_summary, teamB_tactical, teamB_matches = load_dynamic_team(

    master_df,

    team_b,

    start_date,

    end_date

)

# =====================================================
# LIGA DINÁMICA
# =====================================================

tactical_rows = []

for current_team in teams:

    _, tactical_row, _ = load_dynamic_team(

        master_df,

        current_team

    )

    tactical_rows.append(

        tactical_row

    )

tactical = pd.DataFrame(

    tactical_rows

)

numeric_columns = [

    col

    for col in summary.columns

    if pd.api.types.is_numeric_dtype(

        summary[col]

    )

]

tactical_numeric = [

    col

    for col in tactical.columns

    if pd.api.types.is_numeric_dtype(

        tactical[col]

    )

]

# =====================================================
# PAGE
# =====================================================

show_comparison_header(

    team_a=team_a,

    team_b=team_b,

    teamA_tactical=teamA_tactical,

    teamB_tactical=teamB_tactical

)

st.divider()

show_face_to_face(

    team_a=team_a,

    team_b=team_b,

    teamA_tactical=teamA_tactical,

    teamB_tactical=teamB_tactical

)

st.divider()

show_comparison_radar(

    team_a=team_a,

    team_b=team_b,

    teamA_tactical=teamA_tactical,

    teamB_tactical=teamB_tactical

)

st.divider()

show_comparison_kpis(

    team_a=team_a,

    team_b=team_b,

    teamA_summary=teamA_summary,

    teamB_summary=teamB_summary,

    numeric_columns=numeric_columns

)

st.divider()

show_comparison_scatter(

    tactical_df=tactical,

    team_a=team_a,

    team_b=team_b,

    numeric_columns=tactical_numeric

)

st.divider()

show_comparison_similarity(

    tactical_df=tactical,

    team_a=team_a,

    team_b=team_b

)

st.divider()

show_comparison_report(

    team=team_a

)

st.divider()