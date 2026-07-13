import plotly.graph_objects as go
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

from utils.dimensions_help import (
    show_dimensions_help
)


# =====================================================
# SCOUTING RADAR
# =====================================================

def show_radar(

    team,

    team_tactical

):

    st.subheader("🕸️ ADN Táctico")

    c1, c2 = st.columns([12, 1])

    with c2:

        if st.button(

            "ℹ️",

            key="radar_help",

            help="Metodología de las dimensiones"

        ):

            show_dimensions_help()

    radar_metrics = [

        "Dominio",

        "Verticalidad",

        "Presion",

        "Solidez",

        "Agresividad",

        "Efectividad",

        "Eficiencia"

    ]

    values = [

        team_tactical[m]

        for m in radar_metrics

    ]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=values + [values[0]],

            theta=radar_metrics + [radar_metrics[0]],

            fill="toself",

            name=team,

            line=dict(width=3)

        )

    )

    fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 100]

            )

        ),

        showlegend=False,

        height=550,

        margin=dict(

            l=40,

            r=40,

            t=30,

            b=30

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

        # =====================================================
    # TACTICAL SCORE
    # =====================================================

    tactical_score = round(

        sum(values) / len(values),

        1

    )

    percentile = round(

        tactical_score

    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "🎯 Tactical Score",

            f"{tactical_score:.1f}/100"

        )

    with c2:

        st.metric(

            "📈 Percentil Táctico",

            f"{percentile}"

        )

    st.progress(

        percentile / 100

    )

    st.caption(

        "El Tactical Score resume el comportamiento global del equipo a partir de las siete dimensiones tácticas."

    )


        # =====================================================
    # RANKING DE DIMENSIONES
    # =====================================================

    st.write("")

    st.subheader("🏆 Ranking de Dimensiones")

    ranking = sorted(

        zip(

            radar_metrics,

            values

        ),

        key=lambda x: x[1],

        reverse=True

    )

    medals = [

        "🥇",

        "🥈",

        "🥉",

        "4️⃣",

        "5️⃣",

        "6️⃣",

        "7️⃣"

    ]

    for medal, (metric, value) in zip(

        medals,

        ranking

    ):

        c1, c2, c3 = st.columns([3, 7, 1])

        with c1:

            st.write(

                f"{medal} {metric}"

            )

        with c2:

            st.progress(

                value / 100

            )

        with c3:

            st.write(

                f"**{value:.1f}**"

            )
            
    st.divider()

    # =====================================================
    # COMENTARIO DEL ANALISTA
    # =====================================================

    show_analysis_comment(

        team=team,

        module="Scouting",

        section="ADN Táctico",

        chart="Radar Táctico",

        variables=radar_metrics

    )