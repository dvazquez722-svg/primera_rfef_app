import pandas as pd
import streamlit as st

from utils.time_series_analysis import (
    show_time_series_analysis
)

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# LEAGUE TIME SERIES
# =====================================================

def show_league_time_series(

    master_df,

    selected_team

):

    st.subheader("📈 Evolución Temporal")

    team_matches = (

        master_df[
            master_df["Equipo"] == selected_team
        ]

        .copy()

    )

    if "Fecha" in team_matches.columns:

        team_matches["Fecha"] = pd.to_datetime(

            team_matches["Fecha"]

        )

        team_matches = (

            team_matches

            .sort_values(

                "Fecha"

            )

        )

    numeric_columns = [

        col

        for col in team_matches.columns

        if (

            pd.api.types.is_numeric_dtype(

                team_matches[col]

            )

            and

            col not in [

                "ID",

                "Match_ID",

                "Jornada"

            ]

        )

    ]

    show_time_series_analysis(

        team_matches=team_matches,

        league_df=master_df,

        team=selected_team,

        module="League",

        section="Evolución Temporal",

        available_metrics=numeric_columns

    )

    show_analysis_comment(

        team=selected_team,

        module="League",

        section="Evolución Temporal",

        chart="Evolución Temporal",

        variables=numeric_columns

    )

    st.divider()