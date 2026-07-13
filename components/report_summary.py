import pandas as pd
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def show_report_summary(

    summary,

    team,

    team_summary

):

    st.subheader("📋 Resumen Ejecutivo")

    st.caption(
        "Síntesis automática del perfil competitivo del equipo a partir de los principales indicadores."
    )

    numeric_columns = [

        c

        for c in summary.columns

        if pd.api.types.is_numeric_dtype(

            summary[c]

        )

    ]

    percentiles = {}

    for metric in numeric_columns:

        try:

            pct = (

                summary[metric]

                .rank(

                    pct=True

                )

                [

                    summary["Equipo"] == team

                ]

                .iloc[0]

                * 100

            )

            percentiles[metric] = pct

        except:

            pass

    ordered = sorted(

        percentiles.items(),

        key=lambda x: x[1],

        reverse=True

    )

    strengths = ordered[:5]

    weaknesses = ordered[-5:]

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(

            "### 🟢 Principales fortalezas"

        )

        for metric, pct in strengths:

            st.success(

                f"**{metric}** · Percentil {pct:.0f}"

            )

    with c2:

        st.markdown(

            "### 🔴 Aspectos mejorables"

        )

        for metric, pct in weaknesses:

            st.error(

                f"**{metric}** · Percentil {pct:.0f}"

            )

    st.write("")

    mean_percentile = (

        sum(

            percentiles.values()

        )

        /

        len(

            percentiles

        )

    )

    if mean_percentile >= 80:

        overall = "⭐⭐⭐ Rendimiento de élite"

    elif mean_percentile >= 60:

        overall = "⭐⭐ Equipo competitivo"

    elif mean_percentile >= 40:

        overall = "⭐ Rendimiento medio"

    else:

        overall = "Equipo en desarrollo"

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Percentil medio",

            f"{mean_percentile:.1f}"

        )

    with c2:

        st.metric(

            "Fortalezas",

            len(

                [

                    x

                    for x in percentiles.values()

                    if x >= 75

                ]

            )

        )

    with c3:

        st.metric(

            "Nivel global",

            overall

        )

    st.write("")

    st.markdown(

        "### 📌 Claves para preparar el partido"

    )

    recommendations = []

    for metric, pct in strengths[:3]:

        recommendations.append(

            f"Potenciar situaciones relacionadas con **{metric}**, uno de los principales puntos fuertes del equipo."

        )

    for metric, pct in weaknesses[:2]:

        recommendations.append(

            f"Explorar situaciones que obliguen al rival a defender acciones relacionadas con **{metric}**."

        )

    for rec in recommendations:

        st.info(

            rec

        )

    st.divider()

    # =====================================================
    # COMENTARIO DEL ANALISTA
    # =====================================================

    show_analysis_comment(

        team=team,

        module="Informe Automático",

        section="Resumen Ejecutivo",

        chart="Resumen Ejecutivo",

        variables=[

            metric

            for metric, _ in strengths[:3]

        ] + [

            metric

            for metric, _ in weaknesses[:2]

        ]

    )

    st.download_button(

        "📄 Exportar resumen (.csv)",

        data=pd.DataFrame(

            {

                "Fortalezas": [

                    x[0]

                    for x in strengths

                ],

                "Percentil": [

                    round(

                        x[1],

                        1

                    )

                    for x in strengths

                ]

            }

        ).to_csv(index=False),

        file_name=f"Resumen_{team}.csv",

        mime="text/csv",

        use_container_width=True

    )