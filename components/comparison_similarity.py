import pandas as pd
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# COMPARISON SIMILARITY
# =====================================================

def show_comparison_similarity(

    tactical_df,

    team_a,

    team_b

):

    st.subheader("🔍 Equipos Similares")

    metrics = [

        "Dominio",

        "Verticalidad",

        "Presion",

        "Solidez",

        "Agresividad",

        "Efectividad",

        "Eficiencia"

    ]

    c1, c2 = st.columns(2)

    with c1:

        reference_team = st.radio(

            "Equipo de referencia",

            [

                team_a,

                team_b

            ],

            horizontal=True

        )

    with c2:

        top_n = st.slider(

            "Número de equipos",

            3,

            10,

            5

        )

    target = (

        tactical_df[

            tactical_df["Equipo"] == reference_team

        ]

        .iloc[0]

    )

    similarities = []

    for _, row in tactical_df.iterrows():

        if row["Equipo"] == reference_team:

            continue

        distance = sum(

            (

                row[m]

                - target[m]

            ) ** 2

            for m in metrics

        ) ** 0.5

        similarity = max(

            0,

            100 - distance

        )

        similarities.append(

            {

                "Equipo": row["Equipo"],

                "Similitud": round(

                    similarity,

                    1

                ),

                "Distancia": round(

                    distance,

                    2

                )

            }

        )

    similarity_df = (

        pd.DataFrame(

            similarities

        )

        .sort_values(

            "Distancia"

        )

        .head(

            top_n

        )

    )

    cols = st.columns(

        top_n

    )

    for col, (_, row) in zip(

        cols,

        similarity_df.iterrows()

    ):

        with col:

            st.markdown(

                f"""
<div style="
height:200px;
padding:18px;
background:linear-gradient(135deg,#071329,#041026);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
text-align:center;
">

<div style="
font-size:42px;
margin-top:6px;
">
⚽
</div>

<div style="
margin-top:12px;
font-size:22px;
font-weight:700;
color:white;
">

{row["Equipo"]}

</div>

<div style="
margin-top:14px;
font-size:28px;
font-weight:800;
color:#38bdf8;
">

{row["Similitud"]:.0f}%

</div>

<div style="
margin-top:8px;
font-size:12px;
color:#cbd5e1;
">

Similitud táctica

</div>

</div>
""",

                unsafe_allow_html=True

            )

    st.write("")

    st.dataframe(

        similarity_df,

        use_container_width=True,

        hide_index=True

    )

    show_analysis_comment(

        team=reference_team,

        module="Comparison",

        section="Equipos Similares",

        chart="Similitud Táctica",

        variables=metrics

    )

    st.divider()