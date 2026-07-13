import streamlit as st
import plotly.express as px

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# LEAGUE SCATTER
# =====================================================

def show_league_scatter(

    df,

    selected_team,

    numeric_columns

):

    st.subheader("🌍 Posicionamiento Competitivo")

    c1, c2 = st.columns(2)

    with c1:

        x_var = st.selectbox(

            "Variable X",

            numeric_columns,

            index=(
                numeric_columns.index("Posesión del balón, %")
                if "Posesión del balón, %" in numeric_columns
                else 0
            )

        )

    with c2:

        y_var = st.selectbox(

            "Variable Y",

            numeric_columns,

            index=(
                numeric_columns.index("xG")
                if "xG" in numeric_columns
                else 1
            )

        )

    df_plot = df.copy()

    df_plot["Tamaño"] = 18

    df_plot.loc[

        df_plot["Equipo"] == selected_team,

        "Tamaño"

    ] = 35

    fig = px.scatter(

        df_plot,

        x=x_var,

        y=y_var,

        text="Equipo",

        hover_name="Equipo",

        size="Tamaño",

        color=y_var,

        color_continuous_scale="RdYlGn",

        height=650

    )

    fig.update_traces(

        textposition="top center",

        marker=dict(

            line=dict(

                width=2,

                color="white"

            ),

            opacity=0.9

        )

    )

    fig.add_vline(

        x=df[x_var].mean(),

        line_dash="dash",

        line_color="rgba(255,255,255,0.30)"

    )

    fig.add_hline(

        y=df[y_var].mean(),

        line_dash="dash",

        line_color="rgba(255,255,255,0.30)"

    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#071329",

        font=dict(

            color="white",

            size=13

        ),

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        showlegend=False,

        coloraxis_colorbar=dict(

            title=y_var

        ),

        xaxis=dict(

            title=x_var,

            color="#cbd5e1",

            gridcolor="rgba(255,255,255,0.08)"

        ),

        yaxis=dict(

            title=y_var,

            color="#cbd5e1",

            gridcolor="rgba(255,255,255,0.08)"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    show_analysis_comment(

        team=selected_team,

        module="League",

        section="Posicionamiento Competitivo",

        chart="Scatter Competitivo",

        variables=[

            x_var,

            y_var

        ]

    )

    st.divider()