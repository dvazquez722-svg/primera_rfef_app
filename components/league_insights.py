import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# LEAGUE INSIGHTS
# =====================================================

def show_league_insights(

    df,

    selected_team,

    numeric_columns

):

    st.subheader("💡 Insights Competitivos")

    metric = st.selectbox(

        "Variable de análisis",

        numeric_columns,

        key="league_insight_metric"

    )

    ascending = metric in [

        "PPDA",

        "Goles recibidos"

    ]

    ranking = (

        df

        .sort_values(

            metric,

            ascending=ascending

        )

        .reset_index(drop=True)

    )

    position = (

        ranking[

            ranking["Equipo"] == selected_team

        ]

        .index[0]

        + 1

    )

    total = len(df)

    percentile = round(

        100 *

        (total - position)

        /

        (total - 1)

    )

    value = ranking.loc[

        ranking["Equipo"] == selected_team,

        metric

    ].iloc[0]

    mean = df[metric].mean()

    std = df[metric].std()

    if value >= mean + std:

        level = "Muy por encima de la media"

        color = "🟢"

    elif value >= mean:

        level = "Por encima de la media"

        color = "🟡"

    elif value >= mean - std:

        level = "Por debajo de la media"

        color = "🟠"

    else:

        level = "Muy por debajo de la media"

        color = "🔴"

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Posición",

            f"{position}º"

        )

    with c2:

        st.metric(

            "Percentil",

            percentile

        )

    with c3:

        st.metric(

            "Valor",

            round(value, 2)

        )

    with c4:

        st.metric(

            "Media Liga",

            round(mean, 2)

        )

    st.write("")

    st.info(

        f"{color} **Situación competitiva:** {level}"

    )

    st.write("")

    top5 = ranking.head(5)

    bottom5 = ranking.tail(5)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🟢 Top 5")

        st.dataframe(

            top5[

                [

                    "Equipo",

                    metric

                ]

            ],

            use_container_width=True,

            hide_index=True

        )

    with col2:

        st.markdown("### 🔴 Bottom 5")

        st.dataframe(

            bottom5[

                [

                    "Equipo",

                    metric

                ]
            ],

            use_container_width=True,

            hide_index=True

        )

    show_analysis_comment(

        team=selected_team,

        module="League",

        section="Insights",

        chart="Insights Competitivos",

        variables=[

            metric

        ]

    )

    st.divider()