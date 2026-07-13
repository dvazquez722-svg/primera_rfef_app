import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# COMPARISON KPIs
# =====================================================

def show_comparison_kpis(

    team_a,

    team_b,

    teamA_summary,

    teamB_summary,

    numeric_columns

):

    st.subheader("📊 KPIs Comparativos")

    selected_metrics = st.multiselect(

        "Variables a comparar",

        numeric_columns,

        default=[

            m for m in [

                "xG",

                "Goles",

                "Posesión del balón, %",

                "PPDA",

                "Goles recibidos"

            ]

            if m in numeric_columns

        ]

    )

    if not selected_metrics:

        st.info(

            "Selecciona al menos una variable."

        )

        return

    cols = st.columns(

        len(selected_metrics)

    )

    inverse_metrics = [

        "PPDA",

        "Goles recibidos"

    ]

    for col, metric in zip(

        cols,

        selected_metrics

    ):

        value_a = float(

            teamA_summary[metric]

        )

        value_b = float(

            teamB_summary[metric]

        )

        delta = round(

            value_a - value_b,

            2

        )

        if metric in inverse_metrics:

            delta_color = "inverse"

        else:

            delta_color = "normal"

        with col:

            st.metric(

                metric,

                round(

                    value_a,

                    2

                ),

                delta,

                delta_color=delta_color

            )

    st.write("")

    comparison_df = []

    for metric in selected_metrics:

        comparison_df.append(

            {

                "Variable": metric,

                team_a: round(

                    float(

                        teamA_summary[metric]

                    ),

                    2

                ),

                team_b: round(

                    float(

                        teamB_summary[metric]

                    ),

                    2

                ),

                "Diferencia": round(

                    float(

                        teamA_summary[metric]

                    )

                    -

                    float(

                        teamB_summary[metric]

                    ),

                    2

                )

            }

        )

    st.dataframe(

        comparison_df,

        use_container_width=True,

        hide_index=True

    )

    show_analysis_comment(

        team=team_a,

        module="Comparison",

        section="KPIs",

        chart="KPIs Comparativos",

        variables=selected_metrics

    )

    st.divider()