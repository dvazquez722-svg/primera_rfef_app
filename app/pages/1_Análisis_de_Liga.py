import pandas as pd
import streamlit as st
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Análisis de Liga",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/team_summary.csv"
)

numeric_cols = (
    df.select_dtypes(include="number")
      .columns
      .tolist()
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
}

.kpi-card{
    background:white;
    padding:22px;
    border-radius:16px;
    border:1px solid #E5E7EB;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
    min-height:160px;
}

.kpi-title{
    font-size:14px;
    color:#6B7280;
    margin-bottom:10px;
    font-weight:600;
}

.kpi-team{
    font-size:32px;
    font-weight:800;
    color:#111827;
    line-height:1.1;
    margin-bottom:12px;
}

.kpi-value{
    font-size:24px;
    font-weight:700;
    color:#16A34A;
}

.section-title{
    font-size:22px;
    font-weight:700;
    margin-bottom:10px;
}

[data-testid="stMetric"]{
    background-color:white;
    border:1px solid #E5E7EB;
    padding:10px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Primera RFEF - Análisis de Liga")

st.markdown(
    """
    Comparativa visual del rendimiento de todos los equipos de la competición.
    """
)

st.divider()

# =====================================================
# KPI DATA
# =====================================================

best_xg = df.loc[df["xG"].idxmax()]
best_possession = df.loc[df["Posesión del balón, %"].idxmax()]
best_defense = df.loc[df["Goles recibidos"].idxmin()]
best_ppda = df.loc[df["PPDA"].idxmin()]

# =====================================================
# KPIs
# =====================================================

st.markdown("""
<style>

.kpi-card{
    background-color:white;
    padding:22px;
    border-radius:15px;
    border:1px solid #E5E7EB;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
    min-height:160px;
}

.kpi-title{
    font-size:14px;
    color:#6B7280;
    margin-bottom:10px;
}

.kpi-team{
    font-size:30px;
    font-weight:700;
    color:#111827;
    line-height:1.1;
    margin-bottom:12px;
}

.kpi-value{
    font-size:22px;
    font-weight:600;
    color:#16A34A;
}

</style>
""", unsafe_allow_html=True)

best_xg = df.loc[df["xG"].idxmax()]
best_possession = df.loc[df["Posesión del balón, %"].idxmax()]
best_defense = df.loc[df["Goles recibidos"].idxmin()]
best_ppda = df.loc[df["PPDA"].idxmin()]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            ⚽ Mejor ataque (xG)
        </div>
        <div class="kpi-team">
            {best_xg["Equipo"]}
        </div>
        <div class="kpi-value">
            xG {best_xg["xG"]:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            🧠 Más posesión
        </div>
        <div class="kpi-team">
            {best_possession["Equipo"]}
        </div>
        <div class="kpi-value">
            {best_possession["Posesión del balón, %"]:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            🛡️ Mejor defensa
        </div>
        <div class="kpi-team">
            {best_defense["Equipo"]}
        </div>
        <div class="kpi-value">
            {best_defense["Goles recibidos"]:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">
            🔥 Más presión
        </div>
        <div class="kpi-team">
            {best_ppda["Equipo"]}
        </div>
        <div class="kpi-value">
            PPDA {best_ppda["PPDA"]:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# FILTERS
# =====================================================

st.sidebar.header("Filtros")

highlight_team = st.sidebar.selectbox(
    "Destacar equipo",
    ["Ninguno"] + sorted(df["Equipo"].unique())
)

x_var = st.sidebar.selectbox(
    "Variable X",
    numeric_cols,
    index=numeric_cols.index("Posesión del balón, %")
    if "Posesión del balón, %" in numeric_cols
    else 0
)

y_var = st.sidebar.selectbox(
    "Variable Y",
    numeric_cols,
    index=numeric_cols.index("xG")
    if "xG" in numeric_cols
    else 1
)

ranking_metric = st.sidebar.selectbox(
    "Ranking",
    numeric_cols
)

selected_team = st.sidebar.selectbox(
    "Ficha de equipo",
    sorted(df["Equipo"].unique())
)

# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns([4, 1])

# =====================================================
# SCATTER
# =====================================================

with left:

    st.subheader("Mapa de Equipos")

    df_plot = df.copy()

    df_plot["Tamaño"] = 18

    if highlight_team != "Ninguno":

        df_plot.loc[
            df_plot["Equipo"] == highlight_team,
            "Tamaño"
        ] = 35

    fig_scatter = px.scatter(
        df_plot,
        x=x_var,
        y=y_var,
        text="Equipo",
        hover_name="Equipo",
        size="Tamaño",
        color=y_var,
        color_continuous_scale="RdYlGn",
        height=700
    )

    fig_scatter.update_traces(
        textposition="top center",
        marker=dict(
            line=dict(
                width=2,
                color="white"
            ),
            opacity=0.9
        )
    )
    fig_scatter.add_vline(
        x=df[x_var].mean(),
        line_dash="dash",
        line_color="gray",
        opacity=0.5
    )

    fig_scatter.add_hline(
        y=df[y_var].mean(),
        line_dash="dash",
        line_color="gray",
        opacity=0.5
    )

    fig_scatter.update_layout(
        title=f"{y_var} vs {x_var}",
        showlegend=False,
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    # =====================================================
# RANKING VISUAL
# =====================================================

with right:

    st.subheader("Top 10")

    ranking = (
        df[
            ["Equipo", ranking_metric]
        ]
        .sort_values(
            ranking_metric,
            ascending=False
        )
        .head(10)
    )

    fig_rank = px.bar(
        ranking,
        x=ranking_metric,
        y="Equipo",
        orientation="h",
        color=ranking_metric,
        color_continuous_scale="Blues"
    )

    fig_rank.update_layout(
        height=700,
        showlegend=False,
        yaxis=dict(
            autorange="reversed"
        ),
        template="plotly_white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )
st.markdown("---")

team_data = df[df["Equipo"] == selected_team].iloc[0]

st.subheader(f"📋 {selected_team}")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "xG",
    f"{team_data['xG']:.2f}"
)

c2.metric(
    "Posesión",
    f"{team_data['Posesión del balón, %']:.1f}%"
)

c3.metric(
    "PPDA",
    f"{team_data['PPDA']:.2f}"
)

c4.metric(
    "Goles recibidos",
    f"{team_data['Goles recibidos']:.2f}"
)

st.divider()

    # =====================================================
# TOP / BOTTOM
# =====================================================

st.subheader("Top y Bottom")

metric_tb = st.selectbox(
    "Selecciona métrica",
    numeric_cols,
    key="top_bottom"
)

top5 = (
    df[
        ["Equipo", metric_tb]
    ]
    .sort_values(
        metric_tb,
        ascending=False
    )
    .head(5)
)

top5["Grupo"] = "Top 5"

bottom5 = (
    df[
        ["Equipo", metric_tb]
    ]
    .sort_values(
        metric_tb,
        ascending=True
    )
    .head(5)
)

bottom5["Grupo"] = "Bottom 5"

tb = pd.concat(
    [top5, bottom5]
)

fig_tb = px.bar(
    tb,
    x=metric_tb,
    y="Equipo",
    color="Grupo",
    orientation="h",
    height=500,
    barmode="group"
)

fig_tb.update_layout(
    template="plotly_white",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),
    legend_title="",
    yaxis_title="",
    xaxis_title=metric_tb
)

st.plotly_chart(
    fig_tb,
    use_container_width=True
)

st.divider()