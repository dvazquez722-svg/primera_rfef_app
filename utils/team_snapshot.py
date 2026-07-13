import streamlit as st


# =====================================================
# TEAM SNAPSHOT
# =====================================================

def show_team_snapshot(

    df,

    team,

    mode="league" ,

    metrics=None,

    columns=4

):
    
    if mode == "league":

        if metrics is None:

            metrics = [

                "xG",

                "PPDA",

                "Posesión del balón, %",

                "Goles"

            ]

        selectable = True

    elif mode == "scouting":

        metrics = [

            "Goles",

            "Goles recibidos",

            "xG",

            "PPDA"

        ]

        selectable = False

    elif mode == "comparison":

        metrics = [

            "xG",

            "PPDA",

            "Posesión del balón, %",

            "Goles"

        ]

        selectable = False

    else:

        selectable = False

    st.subheader(f"⚽ {team}")

    if selectable:

        selected_metrics = []

        cols = st.columns(columns)

        for i in range(columns):

            with cols[i]:

                metric = st.selectbox(

                    f"Métrica {i+1}",

                    metrics,

                    key=f"snapshot_metric_{i}"

                )

                selected_metrics.append(metric)

    else:

        selected_metrics = metrics

    st.write("")

    cards = st.columns(columns)

    team_row = (

        df[
            df["Equipo"] == team
        ]

        .iloc[0]

    )

    for col, metric in zip(cards, selected_metrics):

        value = team_row[metric]

        ranking = (

            df

            .sort_values(

                metric,

                ascending=False

            )

            .reset_index(drop=True)

        )

        position = (

            ranking[
                ranking["Equipo"] == team
            ]

            .index[0]

            + 1

        )

        percentile = round(

            100 *

            (len(df) - position)

            /

            (len(df) - 1)

        )

        with col:

            st.metric(

                metric,

                round(value, 2)

                if isinstance(

                    value,

                    float

                )

                else value,

                f"{position}º"

            )

            st.progress(

                percentile / 100

            )

            st.caption(

                f"Percentil {percentile}"
            )