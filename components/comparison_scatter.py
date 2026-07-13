import streamlit as st
import plotly.express as px

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# COMPARISON SCATTER
# =====================================================

def show_comparison_scatter(

    tactical_df,

    team_a,

    team_b,

    numeric_columns

):

    st.subheader("🌍 Posicionamiento Competitivo")

    c1, c2 = st.columns(2)

    with c1:

        x_var = st.selectbox(

            "Variable X",

            numeric_columns,

            index=0,

            key="comparison_scatter_x"

        )

    with c2:

        y_var = st.selectbox(

            "Variable Y",

            numeric_columns,

            index=1,

            key="comparison_scatter_y"

        )

    plot_df = tactical_df.copy()

    plot_df["Grupo"] = "Liga"

    plot_df.loc[
        plot_df["Equipo"] == team_a,
        "Grupo"
    ] = team_a

    plot_df.loc[
        plot_df["Equipo"] == team_b,
        "Grupo"
    ] = team_b

    plot_df["Tamaño"] = 18

    plot_df.loc[
        plot_df["Equipo"].isin(
            [team_a, team_b]
        ),
        "Tamaño"
    ] = 36

    fig = px.scatter(

        plot_df,

        x=x_var,

        y=y_var,

        text="Equipo",

        size="Tamaño",

        color="Grupo",

        hover_name="Equipo",

        color_discrete_map={

            "Liga": "#64748b",

            team_a: "#38bdf8",

            team_b: "#ef4444"

        },

        height=700

    )

    fig.update_traces(

        textposition="top center",

        marker=dict(

            line=dict(

                color="white",

                width=1.5

            )

        )

    )

    fig.add_vline(

        x=plot_df[x_var].mean(),

        line_dash="dash",

        line_color="rgba(255,255,255,0.30)"

    )

    fig.add_hline(

        y=plot_df[y_var].mean(),

        line_dash="dash",

        line_color="rgba(255,255,255,0.30)"

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#071329",

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        showlegend=True,

        font=dict(

            color="white"

        ),

        xaxis=dict(

            title=x_var,

            gridcolor="rgba(255,255,255,0.08)"

        ),

        yaxis=dict(

            title=y_var,

            gridcolor="rgba(255,255,255,0.08)"

        )

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    c1, c2 = st.columns(2)

    row_a = plot_df[
        plot_df["Equipo"] == team_a
    ].iloc[0]

    row_b = plot_df[
        plot_df["Equipo"] == team_b
    ].iloc[0]

    with c1:

        st.metric(

            team_a,

            f"{row_a[x_var]:.1f} | {row_a[y_var]:.1f}"

        )

    with c2:

        st.metric(

            team_b,

            f"{row_b[x_var]:.1f} | {row_b[y_var]:.1f}"

        )

    show_analysis_comment(

        team=team_a,

        module="Comparison",

        section="Scatter",

        chart="Posicionamiento Competitivo",

        variables=[

            x_var,

            y_var

        ]

    )

    st.divider()