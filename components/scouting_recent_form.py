import streamlit as st
import pandas as pd

from utils.time_series_analysis import (
    show_time_series_analysis
)

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# RECENT FORM
# =====================================================

def show_recent_form(

    team,

    team_matches,

    league_df

):

    st.subheader("📈 Forma Reciente")

    st.write("")

    last5 = team_matches.tail(5)

    numeric_columns = [

        c

        for c in team_matches.columns

        if (

            team_matches[c].dtype != "object"

            and

            c not in [

                "ID",

                "Match_ID",

                "Jornada"

            ]

        )

    ]

    default_metrics = [

        "xG",

        "Goles",

        "Goles recibidos",

        "PPDA"

    ]

    cols = st.columns(4)

    for col, metric in zip(

        cols,

        default_metrics

    ):

        if metric in last5.columns:

            current = round(

                last5[metric].mean(),

                2

            )

            season = round(

                team_matches[metric].mean(),

                2

            )

            delta = round(

                current - season,

                2

            )

            inverse = metric in [

                "Goles recibidos",

                "PPDA"

            ]

            with col:

                st.metric(

                    metric,

                    current,

                    delta,

                    delta_color=(

                        "inverse"

                        if inverse

                        else "normal"

                    )

                )

    st.divider()

    # =====================================================
    # EVOLUCIÓN TEMPORAL
    # =====================================================

    show_time_series_analysis(

        team_matches=team_matches,

        league_df=league_df,

        team=team,

        module="Scouting",

        section="Forma Reciente",

        available_metrics = [

    col

    for col in team_matches.columns

    if pd.api.types.is_numeric_dtype(team_matches[col])

]

    )

    st.divider()

    # =====================================================
    # COMENTARIO DEL ANALISTA
    # =====================================================

    show_analysis_comment(

        team=team,

        module="Scouting",

        section="Forma Reciente",

        chart="Evolución Temporal",

        variables=numeric_columns

    )