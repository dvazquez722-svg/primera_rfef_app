import streamlit as st
import plotly.express as px

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# LEAGUE RANKING
# =====================================================

def show_league_ranking(

    df,

    selected_team,

    numeric_columns

):

    st.subheader("🏆 Ranking de la Competición")

    c1, c2 = st.columns([2, 1])

    with c1:

        metric = st.selectbox(

            "Métrica",

            numeric_columns,

            key="league_ranking_metric"

        )

    with c2:

        top_n = st.selectbox(

            "Equipos",

            [

                5,

                10,

                15,

                len(df)

            ],

            index=1,

            key="league_ranking_top"

        )

    ascending = metric in [

        "PPDA",

        "Goles recibidos"

    ]

    ranking = (

        df[

            [

                "Equipo",

                metric

            ]

        ]

        .sort_values(

            metric,

            ascending=ascending

        )

        .head(top_n)

        .copy()

    )

    ranking["Color"] = ranking["Equipo"].apply(

        lambda x:

        "Equipo seleccionado"

        if x == selected_team

        else

        "Resto"

    )

    fig = px.bar(

        ranking,

        x=metric,

        y="Equipo",

        orientation="h",

        color="Color",

        color_discrete_map={

            "Equipo seleccionado": "#38bdf8",

            "Resto": "#64748b"

        },

        text=metric,

        height=600

    )

    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside"

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#071329",

        font=dict(

            color="white",

            size=13

        ),

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        showlegend=False,

        yaxis=dict(

            autorange="reversed",

            title=""

        ),

        xaxis=dict(

            title=metric

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    position = (

        df

        .sort_values(

            metric,

            ascending=ascending

        )

        .reset_index(drop=True)

    )

    position = (

        position[

            position["Equipo"] == selected_team

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

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Posición",

            f"{position}º"

        )

    with c2:

        st.metric(

            "Percentil",

            percentile

        )

    with c3:

        st.metric(

            metric,

            round(

                df.loc[

                    df["Equipo"] == selected_team,

                    metric

                ].iloc[0],

                2

            )

        )

    show_analysis_comment(

        team=selected_team,

        module="League",

        section="Ranking",

        chart="Ranking Competitivo",

        variables=[

            metric

        ]

    )

    st.divider()