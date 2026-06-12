import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Análisis de Rival",
    page_icon="⚽",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/team_summary.csv"
)

numeric_cols = (
    df.select_dtypes(
        include="number"
    )
    .columns
    .tolist()
)

# =====================================================
# TEAM SELECTOR
# =====================================================

st.title("⚽ Análisis descriptivo de Rival")

team = st.selectbox(
    "Seleccionar equipo",
    sorted(df["Equipo"].unique())
)

team_row = df[
    df["Equipo"] == team
].iloc[0]

# =====================================================
# RANKINGS LIGA
# =====================================================

xg_rank = int(
    df["xG"]
    .rank(
        ascending=False,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

def_rank = int(
    df["Goles recibidos"]
    .rank(
        ascending=True,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

ppda_rank = int(
    df["PPDA"]
    .rank(
        ascending=True,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

possession_rank = int(
    df["Posesión del balón, %"]
    .rank(
        ascending=False,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

goals_rank = int(
    df["Goles"]
    .rank(
        ascending=False,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    f"""
# ⚽ {team}

### Perfil táctico y rendimiento competitivo
"""
)

# =====================================================
# KPI HEADER
# =====================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "⚽ xG",
    round(team_row["xG"], 2),
    f"#{xg_rank} liga"
)

col2.metric(
    "🥅 Goles",
    round(team_row["Goles"], 2),
    f"#{goals_rank} liga"
)

col3.metric(
    "🧠 Posesión",
    f"{team_row['Posesión del balón, %']:.1f}%",
    f"#{possession_rank} liga"
)

col4.metric(
    "🔥 PPDA",
    round(team_row["PPDA"], 2),
    f"#{ppda_rank} liga"
)

col5.metric(
    "🛡️ Encajados",
    round(team_row["Goles recibidos"], 2),
    f"#{def_rank} liga"
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.info(
    f"""
📊 {team} genera {team_row['xG']:.2f} xG por partido y marca {team_row['Goles']:.2f} goles de media.

🧠 Mantiene una posesión media del {team_row['Posesión del balón, %']:.1f}% y registra un PPDA de {team_row['PPDA']:.2f}.

🛡️ Defensivamente encaja {team_row['Goles recibidos']:.2f} goles por encuentro.

🏆 Ranking liga:
- Ataque: #{xg_rank}
- Defensa: #{def_rank}
- Presión: #{ppda_rank}
- Posesión: #{possession_rank}
"""
)

st.divider()

# =====================================================
# PERFIL TÁCTICO
# =====================================================

st.subheader("🎯 Perfil táctico")

radar_metrics = {
    "xG": "Producción ofensiva",
    "Posesión del balón, %": "Posesión",
    "PPDA": "Presión",
    "Pases progresivos conseguidos": "Progresión",
    "Duelos ganados": "Duelos",
    "Balones recuperados último tercio": "Recuperación alta"
}

# =====================================================
# PERCENTILES
# =====================================================

team_percentiles = []

for metric in radar_metrics.keys():

    pct = (
        df[metric]
        .rank(pct=True)
        .loc[df["Equipo"] == team]
        .iloc[0]
        * 100
    )

    team_percentiles.append(
        round(pct, 1)
    )

# cerrar radar

radar_labels = list(
    radar_metrics.values()
)

team_percentiles.append(
    team_percentiles[0]
)

radar_labels.append(
    radar_labels[0]
)

# =====================================================
# LAYOUT
# =====================================================

radar_col, text_col = st.columns(
    [2, 1]
)

# =====================================================
# RADAR
# =====================================================

with radar_col:

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=team_percentiles,
            theta=radar_labels,
            fill="toself",
            name=team,
            line=dict(width=4),
            opacity=0.8
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=650,
        margin=dict(
            l=30,
            r=30,
            t=40,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# SCOUTING SUMMARY
# =====================================================

with text_col:

    st.markdown("### 📋 Scouting")

    radar_df = pd.DataFrame({
        "Metric": list(radar_metrics.values()),
        "Pct": team_percentiles[:-1]
    })

    strengths = (
        radar_df
        .sort_values(
            "Pct",
            ascending=False
        )
        .head(3)
    )

    weaknesses = (
        radar_df
        .sort_values(
            "Pct",
            ascending=True
        )
        .head(3)
    )

    st.success("### 🟢 Fortalezas")

    for _, row in strengths.iterrows():

        st.write(
            f"**{row['Metric']}** · Percentil {row['Pct']:.0f}"
        )

    st.error("### 🔴 Debilidades")

    for _, row in weaknesses.iterrows():

        st.write(
            f"**{row['Metric']}** · Percentil {row['Pct']:.0f}"
        )

    st.info(
        f"""
Equipo situado en el percentil medio
{radar_df['Pct'].mean():.0f} de la competición.
"""
    )

st.divider()

# =====================================================
# IDENTIDAD DEL EQUIPO
# =====================================================

st.subheader("🧠 Identidad del equipo")

profile_col1, profile_col2 = st.columns([1, 1])

# =====================================================
# PERCENTILES
# =====================================================

metrics_profile = [
    "xG",
    "Posesión del balón, %",
    "PPDA",
    "Pases progresivos conseguidos",
    "Duelos ganados",
    "Balones recuperados último tercio",
]

profile_percentiles = {}

for metric in metrics_profile:

    pct = (
        df[metric]
        .rank(pct=True)
        .loc[df["Equipo"] == team]
        .iloc[0]
        * 100
    )

    profile_percentiles[metric] = round(pct)

# =====================================================
# PERFIL AUTOMÁTICO
# =====================================================

style_sentences = []

if profile_percentiles["Posesión del balón, %"] >= 70:
    style_sentences.append(
        "🧠 Equipo con clara vocación de control mediante posesión."
    )

if profile_percentiles["PPDA"] >= 70:
    style_sentences.append(
        "🔥 Perfil agresivo en presión y recuperación."
    )

if profile_percentiles["xG"] >= 70:
    style_sentences.append(
        "⚽ Alta capacidad de generación ofensiva."
    )

if profile_percentiles["Pases progresivos conseguidos"] >= 70:
    style_sentences.append(
        "➡️ Destaca en progresión y avance de balón."
    )

if profile_percentiles["Duelos ganados"] >= 70:
    style_sentences.append(
        "💪 Competitivo en situaciones de disputa."
    )

if profile_percentiles["Balones recuperados último tercio"] >= 70:
    style_sentences.append(
        "🎯 Recupera con frecuencia cerca del área rival."
    )

# =====================================================
# ALERTAS
# =====================================================

alerts = []

for metric, value in profile_percentiles.items():

    if value <= 30:

        alerts.append(
            f"⚠️ Percentil bajo en {metric}"
        )

# =====================================================
# DISPLAY
# =====================================================

with profile_col1:

    st.markdown("### 🎯 Perfil detectado")

    if len(style_sentences):

        for sentence in style_sentences:

            st.success(sentence)

    else:

        st.info(
            "Perfil equilibrado sin rasgos extremos."
        )

with profile_col2:

    st.markdown("### 🚨 Aspectos a vigilar")

    if len(alerts):

        for alert in alerts:

            st.warning(alert)

    else:

        st.success(
            "No aparecen debilidades estructurales relevantes."
        )

# =====================================================
# SCOUTING REPORT
# =====================================================

st.markdown("### 📋 Resumen ejecutivo")

summary = []

if profile_percentiles["xG"] >= 70:
    summary.append(
        "genera ocasiones por encima de la media"
    )

if profile_percentiles["Posesión del balón, %"] >= 70:
    summary.append(
        "domina fases largas de posesión"
    )

if profile_percentiles["PPDA"] >= 70:
    summary.append(
        "presiona con intensidad"
    )

if profile_percentiles["Balones recuperados último tercio"] >= 70:
    summary.append(
        "recupera arriba con frecuencia"
    )

if not summary:

    summary.append(
        "presenta un perfil equilibrado dentro de la competición"
    )

st.info(
    f"""
**{team}** destaca porque {', '.join(summary)}.

El rendimiento global del equipo se sitúa en el percentil medio
{round(sum(profile_percentiles.values()) / len(profile_percentiles), 0)}
de la competición.
"""
)

st.divider()

# =====================================================
# MAPA TÁCTICO DE LA COMPETICIÓN
# =====================================================

st.subheader("🗺️ Mapa táctico de la competición")

scatter_col1, scatter_col2 = st.columns([4, 1])

# =====================================================
# SCATTER
# =====================================================

with scatter_col1:

    x_var = st.selectbox(
        "Eje X",
        numeric_cols,
        index=numeric_cols.index("Posesión del balón, %")
    )

    y_var = st.selectbox(
        "Eje Y",
        numeric_cols,
        index=numeric_cols.index("xG")
    )

    selected = df[
        df["Equipo"] == team
    ]

    x_mean = df[x_var].mean()
    y_mean = df[y_var].mean()

    fig_scatter = px.scatter(
        df,
        x=x_var,
        y=y_var,
        text="Equipo",
        color=y_var,
        size=y_var,
        size_max=35,
        color_continuous_scale="RdYlGn",
        height=520
    )

    fig_scatter.update_traces(
        textposition="top center",
        marker=dict(
            line=dict(
                width=1,
                color="white"
            )
        )
    )

    # ==========================
    # CUADRANTES
    # ==========================

    fig_scatter.add_vrect(
        x0=df[x_var].min(),
        x1=x_mean,
        fillcolor="lightcoral",
        opacity=0.04,
        layer="below",
        line_width=0
    )

    fig_scatter.add_vrect(
        x0=x_mean,
        x1=df[x_var].max(),
        fillcolor="lightgreen",
        opacity=0.04,
        layer="below",
        line_width=0
    )

    fig_scatter.add_hrect(
        y0=y_mean,
        y1=df[y_var].max(),
        fillcolor="lightgreen",
        opacity=0.04,
        layer="below",
        line_width=0
    )

    fig_scatter.add_hrect(
        y0=df[y_var].min(),
        y1=y_mean,
        fillcolor="lightcoral",
        opacity=0.04,
        layer="below",
        line_width=0
    )

    fig_scatter.add_vline(
        x=x_mean,
        line_dash="dash",
        line_color="gray",
        line_width=2
    )

    fig_scatter.add_hline(
        y=y_mean,
        line_dash="dash",
        line_color="gray",
        line_width=2
    )

    # ==========================
    # EQUIPO SELECCIONADO
    # ==========================

    fig_scatter.add_scatter(
        x=selected[x_var],
        y=selected[y_var],
        mode="markers",
        marker=dict(
            size=55,
            color="rgba(255,0,0,0.15)"
        ),
        hoverinfo="skip",
        showlegend=False
    )

    fig_scatter.add_scatter(
        x=selected[x_var],
        y=selected[y_var],
        mode="markers+text",
        text=[f"⭐ {team}"],
        textposition="top center",
        marker=dict(
            size=28,
            color="#E63946",
            line=dict(
                width=3,
                color="white"
            )
        ),
        showlegend=False
    )

    # ==========================
    # ETIQUETAS
    # ==========================

    fig_scatter.add_annotation(
        x=df[x_var].max(),
        y=df[y_var].max(),
        text="<b>DOMINADORES</b>",
        showarrow=False
    )

    fig_scatter.add_annotation(
        x=df[x_var].min(),
        y=df[y_var].max(),
        text="<b>DIRECTOS</b>",
        showarrow=False
    )

    fig_scatter.add_annotation(
        x=df[x_var].max(),
        y=df[y_var].min(),
        text="<b>POSESIÓN ESTÉRIL</b>",
        showarrow=False
    )

    fig_scatter.add_annotation(
        x=df[x_var].min(),
        y=df[y_var].min(),
        text="<b>BAJO IMPACTO</b>",
        showarrow=False
    )

    fig_scatter.update_layout(
        title=f"{y_var} vs {x_var}",
        showlegend=False,
        margin=dict(l=10, r=10, t=60, b=10)
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# =====================================================
# PANEL DERECHO
# =====================================================

with scatter_col2:

    team_x = selected[x_var].iloc[0]
    team_y = selected[y_var].iloc[0]

    delta_x = team_x - x_mean
    delta_y = team_y - y_mean

    st.markdown("## 🎯 Perfil")

    if team_x >= x_mean and team_y >= y_mean:

        st.success("⭐ DOMINADOR")
        profile_text = "Por encima de la media en ambas dimensiones."

    elif team_x < x_mean and team_y >= y_mean:

        st.success("⚡ DIRECTO")
        profile_text = "Genera mucho con menos posesión."

    elif team_x >= x_mean and team_y < y_mean:

        st.warning("🧠 POSESIÓN ESTÉRIL")
        profile_text = "Controla más de lo que produce."

    else:

        st.error("📉 BAJO IMPACTO")
        profile_text = "Por debajo de la media en ambas dimensiones."

    st.write(profile_text)

    st.markdown("---")

    info1, info2 = st.columns(2)

    with info1:

        st.markdown("#### 📊")

        st.metric(
            x_var,
            round(team_x, 2),
            f"{delta_x:+.2f}"
        )

        st.metric(
            y_var,
            round(team_y, 2),
            f"{delta_y:+.2f}"
        )

    with info2:

        rank_x = int(
            df[x_var]
            .rank(ascending=False, method="min")
            .loc[df["Equipo"] == team]
            .iloc[0]
        )

        rank_y = int(
            df[y_var]
            .rank(ascending=False, method="min")
            .loc[df["Equipo"] == team]
            .iloc[0]
        )

        st.markdown("#### 🏆")

        st.progress((21-rank_x)/20)
        st.caption(f"{x_var}: #{rank_x}")

        st.progress((21-rank_y)/20)
        st.caption(f"{y_var}: #{rank_y}")

st.divider()

# =====================================================
# PERCENTILES SCOUTING
# =====================================================

st.subheader("📊 Perfil Percentil")

percentile_metrics = {
    "xG": "Producción ofensiva",
    "Posesión del balón, %": "Posesión",
    "PPDA": "Presión",
    "Pases progresivos conseguidos": "Progresión",
    "Duelos ganados": "Duelos"
}

percentiles = []

for metric, label in percentile_metrics.items():

    pct = (
        df[metric]
        .rank(pct=True)
        .loc[
            df["Equipo"] == team
        ]
        .iloc[0]
        * 100
    )

    percentiles.append(
        {
            "Métrica": label,
            "Percentil": round(pct)
        }
    )

percentiles_df = pd.DataFrame(
    percentiles
)

# =====================================================
# VISUAL SCOUTING
# =====================================================

for _, row in percentiles_df.iterrows():

    pct = row["Percentil"]

    if pct >= 80:
        color = "🟢"

    elif pct >= 60:
        color = "🔵"

    elif pct >= 40:
        color = "🟡"

    else:
        color = "🔴"

    st.markdown(
        f"""
### {row['Métrica']}

{color} **Percentil {pct}**

"""
    )

    st.progress(
        pct / 100
    )

# =====================================================
# RESUMEN
# =====================================================

mean_pct = round(
    percentiles_df["Percentil"].mean()
)

st.divider()

if mean_pct >= 80:

    st.success(
        f"⭐ Equipo de élite en la competición (P{mean_pct})."
    )

elif mean_pct >= 60:

    st.success(
        f"📈 Equipo claramente por encima de la media (P{mean_pct})."
    )

elif mean_pct >= 40:

    st.warning(
        f"⚖️ Equipo de perfil intermedio (P{mean_pct})."
    )

else:

    st.error(
        f"📉 Equipo por debajo de la media competitiva (P{mean_pct})."
    )

# =====================================================
# EVOLUCIÓN TEMPORAL
# =====================================================

st.divider()

st.subheader("📈 Forma y evolución")

master_df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

team_matches = (
    master_df[
        master_df["Equipo"] == team
    ]
    .copy()
)

team_matches["Fecha"] = pd.to_datetime(
    team_matches["Fecha"]
)

team_matches = team_matches.sort_values(
    "Fecha"
)

# =====================================================
# KPIs FORMA RECIENTE
# =====================================================

last5 = team_matches.tail(5)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⚽ xG últimos 5",
    round(last5["xG"].mean(), 2)
)

col2.metric(
    "🥅 Goles últimos 5",
    round(last5["Goles"].mean(), 2)
)

col3.metric(
    "🛡️ Encajados últimos 5",
    round(last5["Goles recibidos"].mean(), 2)
)

col4.metric(
    "🔥 PPDA últimos 5",
    round(last5["PPDA"].mean(), 2)
)

st.divider()

# =====================================================
# SELECTOR
# =====================================================

evolution_metric = st.selectbox(
    "Variable a analizar",
    [
        "xG",
        "Goles",
        "Goles recibidos",
        "PPDA",
        "Posesión del balón, %"
    ]
)

# =====================================================
# MEDIA MÓVIL
# =====================================================

team_matches["rolling"] = (
    team_matches[evolution_metric]
    .rolling(5)
    .mean()
)

league_mean = (
    master_df[evolution_metric]
    .mean()
)

# =====================================================
# EVOLUCIÓN
# =====================================================

fig = px.line(
    team_matches,
    x="Fecha",
    y=evolution_metric,
    markers=True,
    height=600
)

fig.add_scatter(
    x=team_matches["Fecha"],
    y=team_matches["rolling"],
    mode="lines",
    name="Media móvil 5 partidos",
    line=dict(width=4)
)

fig.add_hline(
    y=league_mean,
    line_dash="dash",
    annotation_text="Media liga"
)

fig.update_layout(
    title=f"Evolución de {evolution_metric}",
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TENDENCIA
# =====================================================

recent = (
    team_matches[evolution_metric]
    .tail(5)
    .mean()
)

season = (
    team_matches[evolution_metric]
    .mean()
)

delta = recent - season

if delta > 0:

    trend_text = (
        f"📈 Tendencia positiva (+{delta:.2f})"
    )

    st.success(
        trend_text
    )

else:

    trend_text = (
        f"📉 Tendencia negativa ({delta:.2f})"
    )

    st.error(
        trend_text
    )

# =====================================================
# ÚLTIMOS 5 PARTIDOS
# =====================================================

st.subheader("🗓️ Últimos 5 partidos")

recent_matches = (
    team_matches
    .sort_values(
        "Fecha",
        ascending=False
    )
    .head(5)
)

for _, row in recent_matches.iterrows():

    goals_for = row["Goles"]
    goals_against = row["Goles recibidos"]

    if goals_for > goals_against:

        icon = "🟢"

    elif goals_for == goals_against:

        icon = "🟡"

    else:

        icon = "🔴"

    st.markdown(
        f"""
{icon} **{row['Partido']}**

xG: {row['xG']:.2f}
|
Goles: {goals_for}
|
Encajados: {goals_against}
"""
    )

# =====================================================
# INFORME AUTOMÁTICO
# =====================================================

st.divider()

st.subheader("📋 Informe automático")

last5_xg = last5["xG"].mean()
season_xg = team_matches["xG"].mean()

last5_ga = last5["Goles recibidos"].mean()
season_ga = team_matches["Goles recibidos"].mean()

attack_trend = (
    "mejorando"
    if last5_xg > season_xg
    else "empeorando"
)

defense_trend = (
    "mejorando"
    if last5_ga < season_ga
    else "empeorando"
)

st.info(
    f"""
**{team}** presenta una tendencia ofensiva **{attack_trend}**
respecto a su media de temporada.

Defensivamente está **{defense_trend}**.

En los últimos cinco encuentros registra:

• xG medio: {last5_xg:.2f}

• Goles recibidos: {last5_ga:.2f}

• PPDA: {last5['PPDA'].mean():.2f}
"""
)