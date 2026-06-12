import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Comparador de Equipos",
    page_icon="⚔️",
    layout="wide"
)

# =====================================================
# LOAD
# =====================================================

tactical = pd.read_csv(
    "data/processed/team_tactical_profile.csv"
)

# =====================================================
# HEADER
# =====================================================

st.title("⚔️ Comparador de Equipos")

st.markdown(
    """
    Comparación táctica avanzada entre dos equipos.
    """
)

# =====================================================
# SELECTORES
# =====================================================

teams = sorted(
    tactical["Equipo"].unique()
)

col1, col2 = st.columns(2)

with col1:

    team_a = st.selectbox(
        "Equipo A",
        teams,
        index=0
    )

with col2:

    team_b = st.selectbox(
        "Equipo B",
        teams,
        index=1
    )

teamA = tactical[
    tactical["Equipo"] == team_a
].iloc[0]

teamB = tactical[
    tactical["Equipo"] == team_b
].iloc[0]

# =====================================================
# FUNCIÓN ARQUETIPO
# =====================================================

def get_archetype(row):

    dom = row["Dominio"]
    vert = row["Verticalidad"]
    pre = row["Presion"]
    sol = row["Solidez"]
    agr = row["Agresividad"]
    efe = row["Efectividad"]
    efi = row["Eficiencia"]

    if dom >= 80 and pre >= 75 and sol >= 75:
        return "⭐ Dominador Total"

    elif dom >= 80 and vert <= 50:
        return "🧠 Equipo de Control"

    elif vert >= 80 and agr >= 70:
        return "⚡ Transición Vertical"

    elif pre >= 80 and agr >= 70:
        return "🔥 Presión Agresiva"

    elif sol >= 85 and dom <= 60:
        return "🛡️ Bloque Bajo"

    elif agr >= 75 and efe >= 75:
        return "💣 Ataque Elite"

    elif efe >= 85 and agr <= 55:
        return "🏹 Francotirador"

    elif dom >= 70 and vert >= 70:
        return "🚀 Dominio Vertical"

    elif pre >= 70 and sol >= 80:
        return "🔒 Muralla Presionante"

    else:
        return "⚖️ Perfil Equilibrado"

# =====================================================
# KPI HEADER
# =====================================================

metrics = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Efectividad",
    "Eficiencia"
]

st.subheader(
    "📊 Resumen comparativo"
)

cols = st.columns(7)

for i, metric in enumerate(metrics):

    delta = round(
        teamA[metric] - teamB[metric],
        1
    )

    cols[i].metric(
        metric,
        round(teamA[metric],1),
        delta
    )

st.divider()

# =====================================================
# RADAR COMPARATIVO
# =====================================================

st.subheader(
    "🕸️ Radar comparativo"
)

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=teamA[metrics],

        theta=metrics,

        fill="toself",

        name=team_a
    )
)

fig.add_trace(

    go.Scatterpolar(

        r=teamB[metrics],

        theta=metrics,

        fill="toself",

        name=team_b
    )
)

fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True,

            range=[0,100]
        )
    ),

    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# =====================================================
# MAPA TÁCTICO DE LA LIGA
# =====================================================

st.divider()

st.subheader(
    "🗺️ Posicionamiento táctico en la competición"
)

fig_map = px.scatter(

    tactical,

    x="Dominio",

    y="Verticalidad",

    size="Eficiencia",

    color="Presion",

    text="Equipo",

    height=750
)

# Equipo A

fig_map.add_scatter(

    x=[teamA["Dominio"]],

    y=[teamA["Verticalidad"]],

    mode="markers+text",

    text=[team_a],

    textposition="top center",

    marker=dict(

        size=40,

        color="red",

        line=dict(
            width=3,
            color="white"
        )
    ),

    name=team_a
)

# Equipo B

fig_map.add_scatter(

    x=[teamB["Dominio"]],

    y=[teamB["Verticalidad"]],

    mode="markers+text",

    text=[team_b],

    textposition="bottom center",

    marker=dict(

        size=40,

        color="blue",

        line=dict(
            width=3,
            color="white"
        )
    ),

    name=team_b
)

# medias liga

x_mean = tactical["Dominio"].mean()
y_mean = tactical["Verticalidad"].mean()

fig_map.add_vline(
    x=x_mean,
    line_dash="dash"
)

fig_map.add_hline(
    y=y_mean,
    line_dash="dash"
)

fig_map.add_annotation(
    x=tactical["Dominio"].max(),
    y=tactical["Verticalidad"].max(),
    text="DOMINADORES",
    showarrow=False
)

fig_map.add_annotation(
    x=tactical["Dominio"].min(),
    y=tactical["Verticalidad"].max(),
    text="VERTICALES",
    showarrow=False
)

fig_map.add_annotation(
    x=tactical["Dominio"].max(),
    y=tactical["Verticalidad"].min(),
    text="CONTROL",
    showarrow=False
)

fig_map.add_annotation(
    x=tactical["Dominio"].min(),
    y=tactical["Verticalidad"].min(),
    text="REACTIVOS",
    showarrow=False
)

fig_map.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


# =====================================================
# DIFERENCIAS CLAVE
# =====================================================

st.subheader(
    "🧠 Diferencias tácticas"
)

differences = []

for metric in metrics:

    diff = abs(
        teamA[metric]
        - teamB[metric]
    )

    differences.append({

        "Métrica": metric,

        "Diferencia": diff
    })

diff_df = pd.DataFrame(
    differences
)

diff_df = diff_df.sort_values(
    "Diferencia",
    ascending=False
)

for _, row in diff_df.head(3).iterrows():

    metric = row["Métrica"]

    if teamA[metric] > teamB[metric]:

        st.info(
            f"{team_a} supera claramente a {team_b} en {metric} (+{row['Diferencia']:.1f})."
        )

    else:

        st.info(
            f"{team_b} supera claramente a {team_a} en {metric} (+{row['Diferencia']:.1f})."
        )

st.divider()

# =====================================================
# CLAVES DEL ENFRENTAMIENTO
# =====================================================

st.divider()

st.subheader(
    "⚔️ Claves del enfrentamiento"
)

advantages = []

for metric in metrics:

    diff = (
        teamA[metric]
        - teamB[metric]
    )

    if abs(diff) >= 15:

        if diff > 0:

            advantages.append(
                f"🟢 {team_a} tiene una ventaja importante en {metric} (+{diff:.1f})."
            )

        else:

            advantages.append(
                f"🔴 {team_b} tiene una ventaja importante en {metric} (+{abs(diff):.1f})."
            )

if len(advantages) == 0:

    st.info(
        "No aparecen ventajas tácticas claramente diferenciales."
    )

else:

    for item in advantages:

        st.write(item)

# =====================================================
# EQUIPOS MÁS PARECIDOS
# =====================================================

st.divider()

st.subheader(
    "🔍 Equipos tácticamente similares"
)

similarity_metrics = [

    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Efectividad",
    "Eficiencia"
]

target = (
    tactical[
        tactical["Equipo"] == team_a
    ]
    .iloc[0]
)

similarities = []

for _, row in tactical.iterrows():

    if row["Equipo"] == team_a:

        continue

    distance = 0

    for metric in similarity_metrics:

        distance += (

            row[metric]
            - target[metric]

        ) ** 2

    distance = distance ** 0.5

    similarities.append({

        "Equipo": row["Equipo"],

        "Distancia": distance
    })

similar_df = pd.DataFrame(
    similarities
)

similar_df = similar_df.sort_values(
    "Distancia"
)

top_similar = (
    similar_df
    .head(5)
)

for i, (_, row) in enumerate(
    top_similar.iterrows(),
    start=1
):

    similarity_score = max(
        0,
        100 - row["Distancia"]
    )

    st.success(
        f"{i}. {row['Equipo']} — Similitud {similarity_score:.0f}%"
    )

st.caption(
    """
La similitud se calcula utilizando las siete dimensiones tácticas
del modelo: Dominio, Verticalidad, Presión, Solidez,
Agresividad, Efectividad y Eficiencia. Las cuales aparecen definidas en el Glosario.
"""
)


# =====================================================
# INFORME AUTOMÁTICO
# =====================================================

st.divider()

st.subheader(
    "🤖 Informe scouting"
)

dominant_team = team_a if teamA["Dominio"] > teamB["Dominio"] else team_b
press_team = team_a if teamA["Presion"] > teamB["Presion"] else team_b
solid_team = team_a if teamA["Solidez"] > teamB["Solidez"] else team_b
effective_team = team_a if teamA["Efectividad"] > teamB["Efectividad"] else team_b

st.info(
    f"""
**Control del juego:** {dominant_team}

**Presión más intensa:** {press_team}

**Mayor solidez defensiva:** {solid_team}

**Mayor efectividad ofensiva:** {effective_team}
"""
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