import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# PROGRESIÓN
# =====================================================

def show_report_progression(

    summary,

    team,

    team_summary

):

    st.subheader("🔄 Progresión")

    st.caption(
        "Analiza cómo progresa el equipo comparando sus acciones con el resto de la competición."
    )

    default_metrics = [

        "Pases hacia adelante logrados",

        "Pases progresivos conseguidos",

        "Pases largos logrados",

        "Conducciones progresivas",

        "Carreras progresivas"

    ]

    available_metrics = [

        m

        for m in default_metrics

        if m in summary.columns

    ]

    all_numeric = [

        c

        for c in summary.columns

        if pd.api.types.is_numeric_dtype(

            summary[c]

        )

    ]

    selected_metrics = st.multiselect(

        "Variables",

        all_numeric,

        default=available_metrics,

        key="report_progression"

    )

    if len(selected_metrics) == 0:

        st.info(

            "Selecciona al menos una variable."

        )

        return

    rows = []

    for metric in selected_metrics:

        percentile = (

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

        rows.append(

            {

                "Variable": metric,

                "Valor": round(

                    float(

                        team_summary[metric]

                    ),

                    2

                ),

                "Percentil": round(

                    percentile,

                    1

                )

            }

        )

    progression_df = pd.DataFrame(

        rows

    )

    fig = px.bar(

        progression_df.sort_values(

            "Percentil"

        ),

        x="Percentil",

        y="Variable",

        orientation="h",

        text="Percentil"

    )

    fig.update_layout(

        template="plotly_dark",

        height=max(

            420,

            len(selected_metrics) * 55

        ),

        paper_bgcolor="#071329",

        plot_bgcolor="#071329",

        margin=dict(

            l=20,

            r=20,

            t=30,

            b=20

        ),

        xaxis_title="Percentil Liga",

        yaxis_title="",

        showlegend=False,

        font=dict(

            color="white"

        )

    )

    fig.update_traces(

        texttemplate="%{text:.0f}",

        textposition="outside"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.write("")

    top_metric = (

        progression_df

        .sort_values(

            "Percentil",

            ascending=False

        )

        .iloc[0]

    )

    bottom_metric = (

        progression_df

        .sort_values(

            "Percentil"

        )

        .iloc[0]

    )

    mean_pct = progression_df["Percentil"].mean()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Principal recurso",

            top_metric["Variable"],

            f"{top_metric['Percentil']:.0f}"

        )

    with c2:

        st.metric(

            "Menor utilización",

            bottom_metric["Variable"],

            f"{bottom_metric['Percentil']:.0f}"

        )

    with c3:

        st.metric(

            "Percentil medio",

            f"{mean_pct:.1f}"

        )

    st.dataframe(

        progression_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # =====================================================
    # COMENTARIO DEL ANALISTA
    # =====================================================

    show_analysis_comment(

        team=team,

        module="Informe Automático",

        section="Progresión",

        chart="Progresión",

        variables=selected_metrics

    )