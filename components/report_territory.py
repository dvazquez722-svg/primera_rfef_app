import pandas as pd
import plotly.express as px
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# TERRITORIO
# =====================================================

def show_report_territory(

    summary,

    team,

    team_summary

):

    st.subheader("🌍 Territorio")

    st.caption(
        "Analiza dónde desarrolla el juego el equipo comparándolo con el resto de la competición."
    )

    suggested_metrics = [

        "Balones recuperados inicio",
        "Balones recuperados medio",
        "Balones recuperados último tercio",
        "Balones perdidos inicio",
        "Balones perdidos medio",
        "Balones perdidos último tercio"

    ]

    available_defaults = [

        metric

        for metric in suggested_metrics

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

        key="report_territory"

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

    territory_df = pd.DataFrame(

        rows

    )

    fig = px.bar(

        territory_df.sort_values(

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

    highest = (

        territory_df

        .sort_values(

            "Percentil",

            ascending=False

        )

        .iloc[0]

    )

    lowest = (

        territory_df

        .sort_values(

            "Percentil"

        )

        .iloc[0]

    )

    average = territory_df["Percentil"].mean()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Principal fortaleza",

            highest["Variable"],

            f"{highest['Percentil']:.0f}"

        )

    with c2:

        st.metric(

            "Menor presencia",

            lowest["Variable"],

            f"{lowest['Percentil']:.0f}"

        )

    with c3:

        st.metric(

            "Percentil medio",

            f"{average:.1f}"

        )

    st.dataframe(

        territory_df,

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

        section="Territorio",

        chart="Territorio",

        variables=selected_metrics

    )