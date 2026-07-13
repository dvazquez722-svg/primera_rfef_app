import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# SCOUTING MATCHES
# =====================================================

def show_recent_matches(

    team,

    team_matches

):

    st.subheader("⚽ Match Center")

    matches = (

        team_matches

        .sort_values(

            "Fecha",

            ascending=False

        )

        .copy()

    )

    numeric_columns = [

        col

        for col in matches.columns

        if matches[col].dtype != "object"
        and col != "Fecha"

    ]

    default_metrics = []

    for metric in [

        "xG",

        "Goles",

        "PPDA",

        "Posesión del balón %"

    ]:

        if metric in numeric_columns:

            default_metrics.append(metric)

    selected_metrics = st.multiselect(

        "Variables a mostrar",

        numeric_columns,

        default=default_metrics

    )

    number_matches = st.slider(

        "Partidos a mostrar",

        5,

        min(20, len(matches)),

        10

    )

    matches = matches.head(number_matches)

    for _, row in matches.iterrows():

        cols = st.columns(2 + len(selected_metrics))

        with cols[0]:

            st.markdown(

                f"**{row['Rival']}**"

            )

            fecha = row["Fecha"]

            if hasattr(

                fecha,

                "strftime"

            ):

                fecha = fecha.strftime("%d/%m/%Y")

            st.caption(fecha)

        with cols[1]:

            st.metric(

                "Resultado",

                row.get(

                    "Resultado",

                    "-"

                )

            )

        for i, metric in enumerate(selected_metrics):

            value = row[metric]

            if isinstance(

                value,

                float

            ):

                value = round(

                    value,

                    2

                )

            with cols[i + 2]:

                st.metric(

                    metric,

                    value

                )

        st.divider()

    show_analysis_comment(

        team=team,

        module="Scouting",

        section="Match Center",

        chart="Últimos partidos",

        variables=selected_metrics

    )