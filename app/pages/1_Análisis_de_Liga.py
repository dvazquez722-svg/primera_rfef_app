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
# HERO LIGA
# =====================================================

num_teams = len(df)

best_xg = df.loc[df["xG"].idxmax()]
best_pos = df.loc[df["Posesión del balón, %"].idxmax()]
best_def = df.loc[df["Goles recibidos"].idxmin()]
best_press = df.loc[df["PPDA"].idxmin()]

st.markdown(
f"""
<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(
135deg,
#0f172a,
#1e293b
);
margin-bottom:25px;
">

<h1 style="
color:white;
margin-bottom:10px;
">
🏆 Primera Federación
</h1>

<div style="
font-size:18px;
color:#cbd5e1;
margin-bottom:25px;
">
{num_teams} equipos analizados
</div>

<div style="
color:white;
font-size:16px;
line-height:1.9;
">

La competición presenta un perfil equilibrado,
con diferencias significativas en producción ofensiva,
presión y control del juego.

<br><br>

⚽ Mejor ataque:
<b>{best_xg["Equipo"]}</b>

&nbsp;&nbsp;&nbsp;

🧠 Más posesión:
<b>{best_pos["Equipo"]}</b>

&nbsp;&nbsp;&nbsp;

🛡️ Mejor defensa:
<b>{best_def["Equipo"]}</b>

&nbsp;&nbsp;&nbsp;

🔥 Más presión:
<b>{best_press["Equipo"]}</b>

</div>

</div>
""",
unsafe_allow_html=True
)

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

    st.markdown("### 🌍 Mapa de Equipos")

    st.markdown("""
    <div style="
    padding:20px;
    background:linear-gradient(
        135deg,
        #071329,
        #1e293b
    );
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    ">
    """, unsafe_allow_html=True)

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
        height=550
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
        line_color="rgba(255,255,255,0.25)"
    )

    fig_scatter.add_hline(
        y=df[y_var].mean(),
        line_dash="dash",
        line_color="rgba(255,255,255,0.25)"
    )

    fig_scatter.update_layout(

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
            gridcolor="rgba(255,255,255,0.08)",
            color="#cbd5e1"
        ),

        yaxis=dict(
            title=y_var,
            gridcolor="rgba(255,255,255,0.08)",
            color="#cbd5e1"
        )
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# =====================================================
# INSIGHTS COMPETICIÓN
# =====================================================

df["Conversion"] = (
    df["Goles"] /
    df["Tiros a portería"]
)

best_conversion = df.loc[
    df["Conversion"].idxmax()
]

dominant_team = df.loc[
    (
        df["Posesión del balón, %"] +
        df["Pases intentados"]
    ).idxmax()
]

cross_team = df.loc[
    df["% centros rematados"].idxmax()
]

press_team = df.loc[
    df["PPDA"].idxmin()
]

high_xg = (
    df["xG"] >
    df["xG"].mean()
).sum()


st.markdown(
    f"""
<div style="
padding:25px;
margin-top:15px;
background:linear-gradient(
135deg,
#041026,
#071329
);
border-radius:18px;
">

<h3 style="
color:white;
margin-top:0;
margin-bottom:20px;
">
📌 Insights de la Competición
</h3>

<div style="
color:white;
font-size:15px;
line-height:2;
">

🎯 <b>{best_conversion['Equipo']}</b>
presenta la mayor eficiencia ofensiva de la competición,
convirtiendo una proporción superior de sus tiros a portería en gol.

<br><br>

🧠 <b>{dominant_team['Equipo']}</b>
destaca por su capacidad para controlar los partidos mediante
posesión y volumen de circulación.

<br><br>

📦 <b>{cross_team['Equipo']}</b>
es el equipo que mejor aprovecha los centros laterales,
registrando el mayor porcentaje de centros rematados.

<br><br>

🔥 <b>{press_team['Equipo']}</b>
presenta el modelo defensivo más agresivo de la competición,
permitiendo menos pases rivales antes de recuperar.

<br><br>

📈 <b>{high_xg} equipos</b>
superan actualmente la media de la categoría en generación de xG.

</div>

</div>
""",
    unsafe_allow_html=True
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
        color_continuous_scale=[
    "#38bdf8",
    "#60a5fa",
    "#93c5fd",
    "#cbd5e1"
]
    )

    fig_rank.update_layout(

    height=550,

    showlegend=False,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="#071329",

    font=dict(
        color="white",
        size=13
    ),

    yaxis=dict(
        autorange="reversed",
        color="#cbd5e1",
        gridcolor="rgba(255,255,255,0.08)"
    ),

    xaxis=dict(
        color="#cbd5e1",
        gridcolor="rgba(255,255,255,0.08)"
    ),

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

### RANKING ###


st.subheader("📊 Ranking de Equipos")

metric_tb = st.selectbox(
    "Métrica",
    numeric_cols
)

top5 = (
    df[["Equipo", metric_tb]]
    .sort_values(metric_tb, ascending=False)
    .head(5)
)

bottom5 = (
    df[["Equipo", metric_tb]]
    .sort_values(metric_tb)
    .head(5)
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🟢 Top 5")

    for _, row in top5.iterrows():

        st.success(
            f"{row['Equipo']} · {row[metric_tb]:.2f}"
        )

with col2:

    st.markdown("### 🔴 Bottom 5")

    for _, row in bottom5.iterrows():

        st.error(
            f"{row['Equipo']} · {row[metric_tb]:.2f}"
        )

st.divider()