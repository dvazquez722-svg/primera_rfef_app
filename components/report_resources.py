import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# RECURSOS OFENSIVOS
# =====================================================

def show_report_resources(

    summary,

    team,

    team_summary

):

    st.subheader("🎯 Recursos Ofensivos")

    st.caption(
        "Identifica cuáles son los principales mecanismos ofensivos del equipo respecto al resto de la competición."
    )

    default_metrics = [

        "Centros lanzados",
        "Contraataques finalizados",
        "Ataques posicionales finalizados",
        "Regates logrados",
        "Pases progresivos conseguidos"

    ]

    available_defaults = [

        metric

        for metric in default_metrics

        if metric in summary.columns

    ]

    numeric_columns = [

        col

        for col in summary.columns

        if pd.api.types.is_numeric_dtype(

            summary[col]

        )

    ]

    selected_metrics = st.multiselect(

        "Variables",

        numeric_columns,

        default=available_defaults,

        key="report_resources"

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

            .rank(pct=True)

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

    resources_df = pd.DataFrame(

        rows

    )

    fig = px.bar(

        resources_df.sort_values(

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

        xaxis=dict(

            range=[0,100],

            title="Percentil Liga"

        ),

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

    strongest = (

        resources_df

        .sort_values(

            "Percentil",

            ascending=False

        )

        .iloc[0]

    )

    weakest = (

        resources_df

        .sort_values(

            "Percentil"

        )

        .iloc[0]

    )

    average = resources_df["Percentil"].mean()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Principal recurso",

            strongest["Variable"],

            f"{strongest['Percentil']:.0f}"

        )

    with c2:

        st.metric(

            "Menor utilización",

            weakest["Variable"],

            f"{weakest['Percentil']:.0f}"

        )

    with c3:

        st.metric(

            "Percentil medio",

            f"{average:.1f}"

        )

    st.dataframe(

        resources_df,

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

        section="Recursos",

        chart="Recursos Ofensivos",

        variables=selected_metrics

    )