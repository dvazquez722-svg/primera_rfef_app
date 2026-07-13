import streamlit as st
from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# SCOUTING KPIS
# =====================================================

def show_kpis(

    team,

    df,

    team_stats

):

    st.subheader("📊 KPIs Competitivos")

    st.write("")

    metrics = [

        "xG",

        "Goles",

        "Posesión del balón %",

        "PPDA",

        "Goles recibidos"

    ]

    selectors = st.columns(5)

    selected_metrics = []

    for i, col in enumerate(selectors):

        with col:

            metric = st.selectbox(

                f"Métrica {i+1}",

                df.columns,

                index=df.columns.get_loc(metrics[i])

                if metrics[i] in df.columns

                else 0,

                key=f"kpi_metric_{i}"

            )

            selected_metrics.append(metric)

    st.write("")

    cards = st.columns(5)

    for col, metric in zip(cards, selected_metrics):

        value = team_stats[metric]

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

                    (float, int)

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

    st.divider()

    show_analysis_comment(

        team=team,

        module="Scouting",

        section="KPIs Competitivos",

        chart="KPIs Competitivos",

        variables=selected_metrics

    )