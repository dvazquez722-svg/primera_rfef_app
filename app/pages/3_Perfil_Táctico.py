import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Perfil Táctico",
    page_icon="🎯",
    layout="wide"
)

tactical = pd.read_csv(
    "data/processed/team_tactical_profile.csv"
)

st.title("🎯 Perfil Táctico")

team = st.selectbox(
    "Seleccionar equipo",
    sorted(
        tactical["Equipo"].unique()
    )
)

team_row = tactical[
    tactical["Equipo"] == team
].iloc[0]

# =====================================================
# VARIABLES
# =====================================================

radar_metrics = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Efectividad",
    "Eficiencia"
]

dom = team_row["Dominio"]
vert = team_row["Verticalidad"]
pre = team_row["Presion"]
sol = team_row["Solidez"]
agr = team_row["Agresividad"]
efe = team_row["Efectividad"]
efi = team_row["Eficiencia"]

# =====================================================
# ARQUETIPO
# =====================================================

if dom >= 80 and pre >= 75 and sol >= 75:

    archetype = "⭐ Dominador Total"

    description = """
Controla el juego, presiona alto y además concede muy poco.
Es uno de los perfiles más completos de la competición.
"""

elif dom >= 80 and vert <= 50:

    archetype = "🧠 Equipo de Control"

    description = """
Busca gobernar los partidos desde la posesión y el control territorial.
"""

elif vert >= 80 and agr >= 70:

    archetype = "⚡ Transición Vertical"

    description = """
Equipo orientado a atacar espacios y progresar rápidamente.
"""

elif pre >= 80 and agr >= 70:

    archetype = "🔥 Presión Agresiva"

    description = """
Busca recuperar arriba y atacar inmediatamente tras robo.
"""

elif sol >= 85 and dom <= 60:

    archetype = "🛡️ Bloque Bajo"

    description = """
Prioriza proteger su portería y competir desde la organización defensiva.
"""

elif agr >= 75 and efe >= 75:

    archetype = "💣 Ataque Elite"

    description = """
Genera mucho volumen ofensivo y además convierte con eficacia.
"""

elif efe >= 85 and agr <= 55:

    archetype = "🏹 Francotirador"

    description = """
Genera menos que otros equipos pero aprovecha muy bien sus ocasiones.
"""

elif dom >= 70 and vert >= 70:

    archetype = "🚀 Dominio Vertical"

    description = """
Combina control del balón con progresión rápida.
"""

elif pre >= 70 and sol >= 80:

    archetype = "🔒 Muralla Presionante"

    description = """
Defiende bien, presiona bien y concede muy poco.
"""

else:

    archetype = "⚖️ Perfil Equilibrado"

    description = """
No presenta una especialización extrema.
Mantiene un comportamiento relativamente equilibrado.
"""

# =====================================================
# KPI TÁCTICOS
# =====================================================

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Dominio",
    round(dom, 1)
)

k2.metric(
    "Presión",
    round(pre, 1)
)

k3.metric(
    "Solidez",
    round(sol, 1)
)

k4.metric(
    "Efectividad",
    round(efe, 1)
)

st.divider()

# =====================================================
# RADAR + ADN + ARQUETIPO
# =====================================================

left, right = st.columns([2, 1])

# =====================================================
# RADAR
# =====================================================

with left:

    st.subheader("🕸️ Radar táctico")

    fig_radar = go.Figure()

    fig_radar.add_trace(

        go.Scatterpolar(

            r=team_row[radar_metrics],

            theta=radar_metrics,

            fill="toself",

            name=team,

            line=dict(
                width=3
            )
        )
    )

    fig_radar.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0, 100]
            )
        ),

        showlegend=False,

        height=600
    )

    st.plotly_chart(
        fig_radar,
        use_container_width=True
    )

# =====================================================
# ADN + ARQUETIPO
# =====================================================

with right:

    st.subheader("🧬 ADN táctico")

    top3 = (

        team_row[radar_metrics]

        .sort_values(
            ascending=False
        )

        .head(3)
    )

    for metric, value in top3.items():

        st.metric(
            metric,
            round(value, 1)
        )

    st.divider()

    st.subheader("🎭 Arquetipo")

    st.success(
        archetype
    )

    st.info(
        description
    )

    st.divider()

    st.subheader(
        "📈 Nivel táctico"
    )

    tactical_score = round(

        team_row[
            radar_metrics
        ].mean(),

        1
    )

    st.metric(
        "Score Global",
        tactical_score
    )

    if tactical_score >= 80:

        st.success(
            "Perfil élite"
        )

    elif tactical_score >= 65:

        st.info(
            "Perfil competitivo"
        )

    else:

        st.warning(
            "Perfil mejorable"
        )

# =====================================================
# RANKING TÁCTICO
# =====================================================

st.divider()

st.subheader("🏆 Ranking por dimensiones")

rank_left, rank_right = st.columns(2)

for i, metric in enumerate(radar_metrics):

    rank = int(
        tactical[metric]
        .rank(
            ascending=False,
            method="min"
        )
        .loc[
            tactical["Equipo"] == team
        ]
        .iloc[0]
    )

    container = (
        rank_left
        if i < 4
        else rank_right
    )

    with container:

        st.markdown(
            f"**{metric}**"
        )

        st.progress(
            (21 - rank) / 20
        )

        st.caption(
            f"#{rank} de 20 equipos"
        )

# =====================================================
# MAPA DE ESTILOS
# =====================================================

st.divider()

st.subheader(
    "🗺️ Mapa de estilos"
)

fig_style = px.scatter(

    tactical,

    x="Dominio",

    y="Verticalidad",

    size="Eficiencia",

    color="Presion",

    text="Equipo",

    height=700
)

selected = tactical[
    tactical["Equipo"] == team
]

fig_style.add_scatter(

    x=selected["Dominio"],

    y=selected["Verticalidad"],

    mode="markers+text",

    text=[team],

    textposition="top center",

    marker=dict(

        size=45,

        color="red",

        line=dict(
            width=3,
            color="white"
        )
    ),

    name=team
)

fig_style.add_vline(
    x=tactical["Dominio"].mean(),
    line_dash="dash"
)

fig_style.add_hline(
    y=tactical["Verticalidad"].mean(),
    line_dash="dash"
)

fig_style.add_annotation(
    x=tactical["Dominio"].max(),
    y=tactical["Verticalidad"].max(),
    text="DOMINADORES",
    showarrow=False
)

fig_style.add_annotation(
    x=tactical["Dominio"].min(),
    y=tactical["Verticalidad"].max(),
    text="VERTICALES",
    showarrow=False
)

fig_style.add_annotation(
    x=tactical["Dominio"].max(),
    y=tactical["Verticalidad"].min(),
    text="CONTROL",
    showarrow=False
)

fig_style.add_annotation(
    x=tactical["Dominio"].min(),
    y=tactical["Verticalidad"].min(),
    text="REACTIVOS",
    showarrow=False
)

fig_style.update_traces(
    textposition="top center"
)

fig_style.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig_style,
    use_container_width=True
)

# =====================================================
# RESUMEN SCOUTING
# =====================================================

st.divider()

st.subheader(
    "📋 Resumen de scouting"
)

top3 = (
    team_row[radar_metrics]
    .sort_values(
        ascending=False
    )
    .head(3)
)

bottom3 = (
    team_row[radar_metrics]
    .sort_values(
        ascending=True
    )
    .head(3)
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "### 🟢 Fortalezas"
    )

    for metric, value in top3.items():

        st.success(
            f"{metric}: {value:.1f}"
        )

with col2:

    st.markdown(
        "### 🔴 Aspectos mejorables"
    )

    for metric, value in bottom3.items():

        st.warning(
            f"{metric}: {value:.1f}"
        )

# =====================================================
# GLOSARIO TÁCTICO
# =====================================================

st.divider()

with st.expander(
    "📚 Diccionario de dimensiones tácticas"
):

    st.markdown("""

### 🧠 Dominio

Capacidad de controlar el partido mediante posesión,
circulación de balón, progresión y generación de juego.

Variables utilizadas:

- Posesión
- Precisión de pase
- Pases progresivos
- Pases en último tercio
- Ataques posicionales
- xG generado

---

### ⚡ Verticalidad

Capacidad para progresar rápidamente hacia portería rival.

Variables utilizadas:

- Contraataques
- Contraataques finalizados
- Pases progresivos
- Pases hacia delante
- Intensidad de paso
- Pases por posesión

Valores altos indican ataques directos y rápidos.

---

### 🔥 Presión

Capacidad para recuperar el balón y dificultar la salida rival.

Variables utilizadas:

- PPDA
- Recuperaciones en último tercio
- Interceptaciones
- Duelos defensivos
- Entradas exitosas

Valores altos indican presión agresiva.

---

### 🛡️ Solidez

Capacidad para proteger la portería propia.

Variables utilizadas:

- Goles recibidos
- Tiros concedidos
- Calidad de tiros concedidos
- Duelos defensivos
- Interceptaciones
- Despejes

Valores altos indican equipos difíciles de superar.

---

### ⚔️ Agresividad

Volumen ofensivo generado independientemente de la eficacia.

Variables utilizadas:

- xG
- Tiros
- Ataques finalizados
- Contraataques finalizados
- Duelos ofensivos
- Centros rematados

Valores altos indican equipos muy activos en ataque.

---

### 🎯 Efectividad

Capacidad para transformar acciones ofensivas en ocasiones y goles.

Variables utilizadas:

- Goles por tiro
- Goles por tiro a puerta
- xG por tiro
- Precisión de tiro
- Finalización de ataques
- Centros rematados

Valores altos indican gran calidad de finalización.

---

### 🏆 Eficiencia

Capacidad para convertir rendimiento en resultados.

Variables utilizadas:

- Conversión goles/xG
- Puntos en casa
- Puntos fuera
- Producción en victorias
- Solidez en victorias

Valores altos indican equipos especialmente competitivos.

---

### 📈 Interpretación

Las dimensiones se expresan en percentiles (0-100).

- 90+ → élite de la competición
- 75-90 → muy alto
- 60-75 → alto
- 40-60 → promedio
- 25-40 → bajo
- <25 → muy bajo

""")