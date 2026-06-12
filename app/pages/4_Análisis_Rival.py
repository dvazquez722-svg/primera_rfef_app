import pandas as pd
import streamlit as st
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Análisis Rival",
    page_icon="🕵️",
    layout="wide"
)

# =====================================================
# LOAD
# =====================================================

master = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

# =====================================================
# HEADER
# =====================================================

st.title("🕵️ Análisis de Rival")

st.markdown(
    """
    Análisis contextual del comportamiento competitivo
    de cada equipo de Primera RFEF.
    """
)

# =====================================================
# TEAM SELECTOR
# =====================================================

team = st.selectbox(
    "Seleccionar equipo",
    sorted(
        master["Equipo"].unique()
    )
)

team_df = (
    master[
        master["Equipo"] == team
    ]
    .copy()
)

# =====================================================
# KPI HEADER
# =====================================================

wins = (
    team_df["Resultado"]
    == "Victoria"
).sum()

draws = (
    team_df["Resultado"]
    == "Empate"
).sum()

losses = (
    team_df["Resultado"]
    == "Derrota"
).sum()

points = team_df["Puntos"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Victorias",
    wins
)

col2.metric(
    "Empates",
    draws
)

col3.metric(
    "Derrotas",
    losses
)

col4.metric(
    "Puntos",
    int(points)
)

st.divider()

# =====================================================
# RENDIMIENTO POR RESULTADO
# =====================================================

st.subheader(
    "📊 Rendimiento según resultado"
)

metrics = [
    "xG",
    "Posesión del balón, %",
    "PPDA",
    "GF",
    "GC"
]

result_summary = (

    team_df

    .groupby("Resultado")[metrics]

    .mean()

    .round(2)

    .reset_index()

)

metric_selected = st.selectbox(
    "Métrica",
    metrics
)

fig = px.bar(

    result_summary,

    x="Resultado",

    y=metric_selected,

    color="Resultado",

    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# LOCAL VS VISITANTE
# =====================================================

st.subheader(
    "🏠 Local vs Visitante"
)

location_metrics = [
    "xG",
    "GF",
    "GC",
    "PPDA",
    "Posesión del balón, %",
    "Puntos"
]

location_summary = (

    team_df

    .groupby("Condicion")[location_metrics]

    .mean()

    .round(2)

    .reset_index()
)

location_metric = st.selectbox(
    "Comparar local vs visitante",
    location_metrics
)

fig_location = px.bar(

    location_summary,

    x="Condicion",

    y=location_metric,

    color="Condicion",

    height=500
)

st.plotly_chart(
    fig_location,
    use_container_width=True
)

st.divider()

# =====================================================
# FACTORES DE LA VICTORIA
# =====================================================

st.subheader(
    "🟢 Factores asociados a la victoria"
)

wins_df = team_df[
    team_df["Resultado"] == "Victoria"
]

analysis_metrics = [

    "xG",

    "GF",

    "GC",

    "PPDA",

    "Posesión del balón, %",

    "Tiros totales",

    "Tiros a portería",

    "Pases progresivos conseguidos",

    "Contraataques",

    "Balones recuperados último tercio"
]

victory_factors = []

for metric in analysis_metrics:

    global_value = team_df[metric].mean()

    win_value = wins_df[metric].mean()

    diff = win_value - global_value

    victory_factors.append({

        "Métrica": metric,

        "Diferencia": round(diff, 2)

    })

victory_df = pd.DataFrame(
    victory_factors
)

victory_df = victory_df.sort_values(
    "Diferencia",
    ascending=False
)

fig_victory = px.bar(

    victory_df.head(10),

    x="Diferencia",

    y="Métrica",

    orientation="h",

    height=600,

    color="Diferencia",

    color_continuous_scale="Greens"
)

st.plotly_chart(
    fig_victory,
    use_container_width=True
)

st.caption(
    "Variables que más aumentan respecto a la media del equipo cuando consigue la victoria."
)

st.divider()

# =====================================================
# FACTORES DE LA DERROTA
# =====================================================

st.subheader(
    "🔴 Factores asociados a la derrota"
)

loss_df = team_df[
    team_df["Resultado"] == "Derrota"
]

analysis_metrics = [

    "xG",

    "GF",

    "GC",

    "PPDA",

    "Posesión del balón, %",

    "Tiros totales",

    "Tiros a portería",

    "Pases progresivos conseguidos",

    "Contraataques",

    "Balones recuperados último tercio"
]

loss_factors = []

for metric in analysis_metrics:

    global_value = team_df[metric].mean()

    loss_value = loss_df[metric].mean()

    diff = loss_value - global_value

    loss_factors.append({

        "Métrica": metric,

        "Diferencia": round(diff, 2)

    })

loss_df_chart = pd.DataFrame(
    loss_factors
)

loss_df_chart = loss_df_chart.sort_values(
    "Diferencia"
)

fig_loss = px.bar(

    loss_df_chart,

    x="Diferencia",

    y="Métrica",

    orientation="h",

    height=600,

    color="Diferencia",

    color_continuous_scale="Reds"
)

fig_loss.add_vline(
    x=0,
    line_dash="dash"
)

st.plotly_chart(
    fig_loss,
    use_container_width=True
)

st.caption(
    "Variables que más se deterioran respecto a la media del equipo cuando llega la derrota."
)

st.divider()

# =====================================================
# RENDIMIENTO CONTRA RIVALES
# =====================================================

st.subheader(
    "⚔️ Rendimiento contra cada rival"
)

rival_summary = (

    team_df

    .groupby("Rival")

    .agg({

        "Puntos": "mean",

        "GF": "mean",

        "GC": "mean",

        "xG": "mean"

    })

    .round(2)

    .reset_index()

)

metric_rival = st.selectbox(

    "Analizar rival según",

    [
        "Puntos",
        "GF",
        "GC",
        "xG"
    ]
)

fig_rival = px.bar(

    rival_summary

    .sort_values(
        metric_rival,
        ascending=False
    ),

    x="Rival",

    y=metric_rival,

    color=metric_rival,

    height=600
)

fig_rival.update_layout(

    xaxis_tickangle=-45
)

st.plotly_chart(
    fig_rival,
    use_container_width=True
)

st.divider()

# =====================================================
# RIVAL MÁS FAVORABLE Y MÁS DIFÍCIL
# =====================================================

st.subheader(
    "🎯 Rivales clave"
)

best_rival = (

    rival_summary

    .sort_values(
        "Puntos",
        ascending=False
    )

    .iloc[0]
)

worst_rival = (

    rival_summary

    .sort_values(
        "Puntos"
    )

    .iloc[0]
)

col1, col2 = st.columns(2)

with col1:

    st.success(

        f"""
Mejor rival:

{best_rival['Rival']}

Puntos medios:
{best_rival['Puntos']:.2f}
"""
    )

with col2:

    st.error(

        f"""
Rival más complicado:

{worst_rival['Rival']}

Puntos medios:
{worst_rival['Puntos']:.2f}
"""
    )

# =====================================================
# INFORME AUTOMÁTICO DE SCOUTING
# =====================================================

st.divider()

st.subheader(
    "🧠 Informe automático"
)

insights = []

# ==========================================
# VICTORIAS
# ==========================================

if len(wins_df):

    win_xg = wins_df["xG"].mean()
    season_xg = team_df["xG"].mean()

    if win_xg > season_xg:

        diff = (
            (win_xg - season_xg)
            / season_xg
        ) * 100

        insights.append(
            f"🟢 Cuando gana genera un {diff:.0f}% más de xG que su media anual."
        )

# ==========================================
# PRESIÓN
# ==========================================

if len(wins_df):

    win_ppda = wins_df["PPDA"].mean()
    season_ppda = team_df["PPDA"].mean()

    if win_ppda < season_ppda:

        insights.append(
            "🔥 Las victorias están asociadas a una presión más agresiva."
        )

# ==========================================
# LOCAL / VISITANTE
# ==========================================

home_points = (

    team_df[
        team_df["Condicion"] == "Local"
    ]["Puntos"]

    .mean()
)

away_points = (

    team_df[
        team_df["Condicion"] == "Visitante"
    ]["Puntos"]

    .mean()
)

if home_points > away_points + 0.3:

    insights.append(
        "🏠 El rendimiento competitivo aumenta significativamente como local."
    )

elif away_points > home_points + 0.3:

    insights.append(
        "✈️ El equipo mantiene un rendimiento especialmente fuerte como visitante."
    )

# ==========================================
# SOLIDEZ
# ==========================================

if len(loss_df):

    loss_gc = loss_df["GC"].mean()
    season_gc = team_df["GC"].mean()

    if loss_gc > season_gc:

        insights.append(
            f"🔴 En las derrotas recibe {loss_gc:.2f} goles por partido."
        )

# ==========================================
# RIVAL MÁS COMPLEJO
# ==========================================

insights.append(
    f"⚔️ El rival más problemático ha sido {worst_rival['Rival']}."
)

# ==========================================
# MEJOR ESCENARIO
# ==========================================

if len(wins_df):

    threshold = wins_df["xG"].mean()

    insights.append(
        f"🎯 Su mejor escenario competitivo aparece cuando supera {threshold:.2f} xG."
    )

# ==========================================
# DISPLAY
# ==========================================

for item in insights:

    st.info(item)

# =====================================================
# EXPLORADOR DE RENDIMIENTO
# =====================================================

st.subheader(
    "🗺️ Explorador de rendimiento"
)

scatter_col1, scatter_col2 = st.columns([4,1])

numeric_metrics = [

    "xG",
    "GF",
    "GC",
    "PPDA",
    "Posesión del balón, %",
    "Tiros totales",
    "Tiros a portería",
    "Pases progresivos conseguidos",
    "Contraataques",
    "Balones recuperados último tercio"
]

with scatter_col2:

    x_metric = st.selectbox(
        "Eje X",
        numeric_metrics,
        index=3
    )

    y_metric = st.selectbox(
        "Eje Y",
        numeric_metrics,
        index=0
    )

with scatter_col1:

    fig_map = px.scatter(

        team_df,

        x=x_metric,

        y=y_metric,

        color="Resultado",

        hover_name="Partido",

        size="GF",

        height=700
    )

    x_mean = team_df[x_metric].mean()
    y_mean = team_df[y_metric].mean()

    fig_map.add_vline(
        x=x_mean,
        line_dash="dash"
    )

    fig_map.add_hline(
        y=y_mean,
        line_dash="dash"
    )

    fig_map.update_traces(
        marker=dict(
            line=dict(
                width=1,
                color="white"
            )
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

st.divider()

# =====================================================
# CONCLUSIONES
# =====================================================

st.subheader(
    "🎯 Conclusiones"
)

avg_xg = team_df["xG"].mean()
win_xg = wins_df["xG"].mean() if len(wins_df) else 0

avg_ppda = team_df["PPDA"].mean()
win_ppda = wins_df["PPDA"].mean() if len(wins_df) else 0

home_points = (
    team_df[
        team_df["Condicion"] == "Local"
    ]["Puntos"]
    .mean()
)

away_points = (
    team_df[
        team_df["Condicion"] == "Visitante"
    ]["Puntos"]
    .mean()
)

if win_xg > avg_xg:

    st.success(
        f"🟢 Cuando gana genera +{win_xg-avg_xg:.2f} xG respecto a su media."
    )

if win_ppda < avg_ppda:

    st.success(
        "🟢 Sus victorias suelen estar asociadas a una presión más intensa."
    )

if home_points > away_points:

    st.info(
        "🏠 Obtiene más rendimiento jugando como local."
    )

else:

    st.info(
        "✈️ Mantiene un rendimiento similar fuera de casa."
    )

if len(loss_df):

    st.warning(
        f"🔴 En las derrotas recibe {loss_df['GC'].mean():.2f} goles por partido."
    )