import streamlit as st
import plotly.graph_objects as go

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# COMPARISON RADAR
# =====================================================

def show_comparison_radar(

    team_a,

    team_b,

    teamA_tactical,

    teamB_tactical

):

    st.subheader("🕸️ ADN Comparativo")

    metrics = [

        "Dominio",

        "Verticalidad",

        "Presion",

        "Solidez",

        "Agresividad",

        "Efectividad",

        "Eficiencia"

    ]

    values_a = [

        float(teamA_tactical[m])

        for m in metrics

    ]

    values_b = [

        float(teamB_tactical[m])

        for m in metrics

    ]

    metrics_closed = metrics + [metrics[0]]

    values_a_closed = values_a + [values_a[0]]

    values_b_closed = values_b + [values_b[0]]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=values_a_closed,

            theta=metrics_closed,

            fill="toself",

            name=team_a,

            line=dict(

                color="#38bdf8",

                width=4

            ),

            fillcolor="rgba(56,189,248,0.25)"

        )

    )

    fig.add_trace(

        go.Scatterpolar(

            r=values_b_closed,

            theta=metrics_closed,

            fill="toself",

            name=team_b,

            line=dict(

                color="#ef4444",

                width=4

            ),

            fillcolor="rgba(239,68,68,0.20)"

        )

    )

    fig.update_layout(

        height=700,

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#071329",

        showlegend=True,

        legend=dict(

            orientation="h",

            x=0.5,

            xanchor="center",

            y=1.08

        ),

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        polar=dict(

            bgcolor="#071329",

            radialaxis=dict(

                range=[0,100],

                tickvals=[20,40,60,80,100],

                gridcolor="rgba(255,255,255,0.12)",

                linecolor="rgba(255,255,255,0.12)",

                tickfont=dict(

                    color="white"

                )

            ),

            angularaxis=dict(

                gridcolor="rgba(255,255,255,0.12)",

                linecolor="rgba(255,255,255,0.12)",

                tickfont=dict(

                    color="white",

                    size=13

                )

            )

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    c1, c2, c3 = st.columns(3)

    diff = {

        metric: abs(

            teamA_tactical[metric]

            - teamB_tactical[metric]

        )

        for metric in metrics

    }

    biggest = max(

        diff,

        key=diff.get

    )

    closest = min(

        diff,

        key=diff.get

    )

    mean_diff = round(

        sum(

            diff.values()

        )

        / len(diff),

        1

    )

    with c1:

        st.metric(

            "Mayor diferencia",

            biggest

        )

    with c2:

        st.metric(

            "Mayor similitud",

            closest

        )

    with c3:

        st.metric(

            "Diferencia media",

            mean_diff

        )

    show_analysis_comment(

        team=team_a,

        module="Comparison",

        section="Radar",

        chart="ADN Comparativo",

        variables=metrics

    )

    st.divider()