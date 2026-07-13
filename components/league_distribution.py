import streamlit as st
import plotly.express as px

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# LEAGUE DISTRIBUTION
# =====================================================

def show_league_distribution(

    df,

    selected_team,

    numeric_columns

):

    st.subheader("📦 Distribución de la Competición")

    c1, c2 = st.columns(2)

    with c1:

        metric = st.selectbox(

            "Variable",

            numeric_columns,

            key="distribution_metric"

        )

    with c2:

        chart = st.selectbox(

            "Visualización",

            [

                "Histograma",

                "Boxplot",

                "Violín"

            ],

            key="distribution_chart"

        )

    if chart == "Histograma":

        fig = px.histogram(

            df,

            x=metric,

            nbins=12

        )

        team_value = df.loc[

            df["Equipo"] == selected_team,

            metric

        ].iloc[0]

        fig.add_vline(

            x=team_value,

            line_color="#38bdf8",

            line_width=3,

            annotation_text=selected_team

        )

    elif chart == "Boxplot":

        fig = px.box(

            df,

            y=metric,

            points="all"

        )

    else:

        fig = px.violin(

            df,

            y=metric,

            box=True,

            points="all"

        )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#071329",

        font=dict(

            color="white"

        ),

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        showlegend=False,

        height=550

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    value = df.loc[

        df["Equipo"] == selected_team,

        metric

    ].iloc[0]

    percentile = round(

        (

            df[metric] < value

        ).mean()

        * 100

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Valor",

            round(

                value,

                2

            )

        )

    with c2:

        st.metric(

            "Media Liga",

            round(

                df[metric].mean(),

                2

            )

        )

    with c3:

        st.metric(

            "Percentil",

            percentile

        )

    show_analysis_comment(

        team=selected_team,

        module="League",

        section="Distribución",

        chart="Distribución Competitiva",

        variables=[

            metric

        ]

    )

    st.divider()