import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# WIN CONDITIONS
# =====================================================

def show_report_win_conditions(

    team,

    matches

):
    st.subheader("🏆 Factores de éxito")

    st.caption(
        "Comparación entre victorias y derrotas para identificar qué variables tienen mayor influencia en el rendimiento del equipo."
    )

    numeric_columns = [

        col

        for col in matches.columns

        if pd.api.types.is_numeric_dtype(

            matches[col]

        )

    ]

    default_metrics = [

        c

        for c in [

            "Posesión del balón, %",
            "xG",
            "PPDA",
            "Pases progresivos conseguidos",
            "Balones recuperados último tercio"

        ]

        if c in numeric_columns

    ]

    selected_metrics = st.multiselect(

        "Variables",

        numeric_columns,

        default=default_metrics,

        key="report_win_conditions"

    )

    if len(selected_metrics) == 0:

        st.info(

            "Selecciona al menos una variable."

        )

        return

    matches = matches.copy()

    matches["Resultado"] = np.where(

        matches["Goles"]

        >

        matches["Goles recibidos"],

        "Victoria",

        np.where(

            matches["Goles"]

            <

            matches["Goles recibidos"],

            "Derrota",

            "Empate"

        )

    )

    wins = matches[

        matches["Resultado"] == "Victoria"

    ]

    losses = matches[

        matches["Resultado"] == "Derrota"

    ]

    rows = []

    for metric in selected_metrics:

        win_value = wins[metric].mean()

        loss_value = losses[metric].mean()

        delta = win_value - loss_value

        delta_pct = (

            delta

            / abs(loss_value)

            * 100

            if loss_value != 0

            else 0

        )

        rows.append(

            {

                "Variable": metric,

                "Victoria": round(

                    win_value,

                    2

                ),

                "Derrota": round(

                    loss_value,

                    2

                ),

                "Diferencia": round(

                    delta,

                    2

                ),

                "Delta_%": round(

                    delta_pct,

                    1

                )

            }

        )

    comparison_df = pd.DataFrame(

        rows

    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            y=comparison_df["Variable"],

            x=comparison_df["Derrota"],

            name="Derrota",

            orientation="h"

        )

    )

    fig.add_trace(

        go.Bar(

            y=comparison_df["Variable"],

            x=comparison_df["Victoria"],

            name="Victoria",

            orientation="h"

        )

    )

    fig.update_layout(

        barmode="group",

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

        xaxis_title="",

        yaxis_title="",

        legend_title="",

        legend=dict(

            font=dict(

                color="white"

            )
        ),

        font=dict(

            color="white"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    top_positive = (

        comparison_df

        .sort_values(

            "Delta_%",

            ascending=False

        )

        .iloc[0]

    )

    top_negative = (

        comparison_df

        .sort_values(

            "Delta_%"

        )

        .iloc[0]

    )

    mean_delta = comparison_df["Delta_%"].mean()

    with c1:

        st.metric(

            "Mayor mejora",

            top_positive["Variable"],

            f"+{top_positive['Delta_%']:.1f}%"

        )

    with c2:

        st.metric(

            "Mayor descenso",

            top_negative["Variable"],

            f"{top_negative['Delta_%']:.1f}%"

        )

    with c3:

        st.metric(

            "Cambio medio",

            f"{mean_delta:.1f}%"

        )

    st.dataframe(

        comparison_df,

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

        section="Condiciones de Victoria",

        chart="Win Conditions",

        variables=selected_metrics

    )