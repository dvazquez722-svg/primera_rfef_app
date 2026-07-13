import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# FACE TO FACE
# =====================================================

def show_face_to_face(

    team_a,

    team_b,

    teamA_tactical,

    teamB_tactical

):

    st.subheader("⚔️ Cara a Cara")

    metrics = [

        "Dominio",

        "Verticalidad",

        "Presion",

        "Solidez",

        "Agresividad",

        "Efectividad",

        "Eficiencia"

    ]

    for metric in metrics:

        value_a = round(

            float(

                teamA_tactical[metric]

            ),

            1

        )

        value_b = round(

            float(

                teamB_tactical[metric]

            ),

            1

        )

        maximum = max(

            value_a,

            value_b,

            1

        )

        pct_a = value_a / maximum

        pct_b = value_b / maximum

        if value_a > value_b:

            winner = team_a

            color = "#22c55e"

        elif value_b > value_a:

            winner = team_b

            color = "#ef4444"

        else:

            winner = "Empate"

            color = "#94a3b8"

        c1, c2, c3 = st.columns(

            [

                3,

                2,

                3

            ]

        )

        with c1:

            st.markdown(

                f"**{team_a}**"

            )

            st.progress(

                pct_a

            )

            st.metric(

                "",

                value_a

            )

        with c2:

            st.markdown(

                f"### {metric}"

            )

            st.markdown(

                f"<p style='text-align:center;color:{color};font-weight:700;'>"

                f"{winner}"

                f"</p>",

                unsafe_allow_html=True

            )

            st.caption(

                f"Diferencia: {abs(value_a-value_b):.1f}"

            )

        with c3:

            st.markdown(

                f"**{team_b}**"

            )

            st.progress(

                pct_b

            )

            st.metric(

                "",

                value_b

            )

        st.divider()

    show_analysis_comment(

        team=team_a,

        module="Comparison",

        section="Cara a Cara",

        chart="Cara a Cara",

        variables=metrics

    )