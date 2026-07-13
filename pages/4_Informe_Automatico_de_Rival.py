import pandas as pd
import streamlit as st

from utils.team_selector import (
    show_team_selector,
    get_selected_team
)

from src.team_summary import (
    build_team_summary
)

from utils.load_dynamic_team import (
    load_dynamic_team
)

from utils.dimensions_help import (
    show_dimensions_help
)

from components.report_header import (
    show_report_header
)

from components.report_win_conditions import (
    show_report_win_conditions
)

from components.report_production import (
    show_report_production
)

from components.report_progression import (
    show_report_progression
)

from components.report_territory import (
    show_report_territory
)

from components.report_resources import (
    show_report_resources
)

from components.report_summary import (
    show_report_summary
)

from utils.report_generator import (
    generate_report
)

from services.data_reports import (
    get_notes
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(

    page_title="Informe Automático",

    page_icon="🎯",

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

summary = build_team_summary(

    master_df

)

master_df["Fecha"] = pd.to_datetime(

    master_df["Fecha"]

)

# =====================================================
# FILTRO TEMPORAL
# =====================================================

st.subheader("📅 Periodo de análisis")

mode = st.radio(

    "",

    [

        "Toda la temporada",

        "Últimos 5 partidos",

        "Últimos 10 partidos",

        "Últimos 15 partidos",

        "Rango personalizado"

    ],

    horizontal=True

)

start_date = None
end_date = None

if mode == "Rango personalizado":

    c1, c2 = st.columns(2)

    with c1:

        start_date = st.date_input(

            "Desde",

            master_df["Fecha"].min().date()

        )

    with c2:

        end_date = st.date_input(

            "Hasta",

            master_df["Fecha"].max().date()

        )

st.divider()

# =====================================================
# TEAM DATA
# =====================================================

matches_limit = None

if mode == "Últimos 5 partidos":

    matches_limit = 5

elif mode == "Últimos 10 partidos":

    matches_limit = 10

elif mode == "Últimos 15 partidos":

    matches_limit = 15

team_summary, team_tactical, team_matches = load_dynamic_team(

    master_df,

    team,

    start_date=start_date,

    end_date=end_date,

    matches_limit=matches_limit

)

filtered_summary = team_summary

# =====================================================
# PAGE
# =====================================================

show_report_header(

    team=team,

    team_summary=team_summary,

    team_tactical=team_tactical,

    matches=team_matches

)

st.divider()

show_report_win_conditions(

    team=team,

    matches=team_matches

)

st.divider()

show_report_production(

    summary=summary,

    team=team,

    team_summary=filtered_summary

)

st.divider()

show_report_progression(

    summary=summary,

    team=team,

    team_summary=filtered_summary

)

st.divider()

show_report_territory(

    summary=summary,

    team=team,

    team_summary=filtered_summary

)

st.divider()

show_report_resources(

    summary=summary,

    team=team,

    team_summary=filtered_summary

)

st.divider()

show_report_summary(

    summary=summary,

    team=team,

    team_summary=filtered_summary

)

st.divider()

st.subheader("📄 Informe Técnico")

if st.button(

    "Generar Informe Word",

    type="primary",

    use_container_width=True

):

    notes = get_notes(

        team

    )

    report = generate_report(

        team,

        notes

    )

    st.success(

        "Informe generado correctamente."

    )

    st.info(

        report["file"]

    )

show_dimensions_help()

