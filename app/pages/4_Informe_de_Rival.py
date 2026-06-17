import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Informe de Rival",
    page_icon="🎯",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

summary = pd.read_csv(
    "data/processed/team_summary.csv"
)

master_df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

master_df["Fecha"] = pd.to_datetime(
    master_df["Fecha"]
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    max-width:1600px;
    padding-top:1rem;
}

.hero-card{

    padding:30px;

    border-radius:20px;

    background:linear-gradient(
        135deg,
        #071329,
        #1e293b
    );

    border:1px solid rgba(255,255,255,0.08);
}

.section-title{

    font-size:30px;

    font-weight:800;

    margin-top:20px;

    margin-bottom:20px;
}

</style>
""",
unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(
"""
# 🎯 Informe de Rival

Contexto previo al análisis de vídeo.
"""
)

# =====================================================
# SELECTOR
# =====================================================

team = st.selectbox(
    "Seleccionar rival",
    sorted(summary["Equipo"].unique())
)

# =====================================================
# TEAM DATA
# =====================================================

team_summary = (

    summary[
        summary["Equipo"] == team
    ]

    .iloc[0]

)

matches = (

    master_df[
        master_df["Equipo"] == team
    ]

    .copy()

)

# =====================================================
# HERO
# =====================================================

victories = (
    matches["Goles"]
    >
    matches["Goles recibidos"]
).sum()

draws = (
    matches["Goles"]
    ==
    matches["Goles recibidos"]
).sum()

losses = (
    matches["Goles"]
    <
    matches["Goles recibidos"]
).sum()

games = len(matches)

win_pct = (
    victories / games
) * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Partidos",
        games
    )

with col2:
    st.metric(
        "% Victorias",
        f"{win_pct:.0f}%"
    )

with col3:
    st.metric(
        "GF",
        round(
            team_summary["Goles"],
            2
        )
    )

with col4:
    st.metric(
        "GC",
        round(
            team_summary["Goles recibidos"],
            2
        )
    )

st.divider()

# =====================================================
# ¿QUÉ NECESITA PARA GANAR?
# =====================================================

st.markdown("## 🏆 ¿Qué necesita para ganar?")

# -----------------------------------------------------
# RESULTADO
# -----------------------------------------------------

matches = master_df[
    master_df["Equipo"] == team
].copy()

matches["Resultado"] = np.where(
    matches["Goles"] > matches["Goles recibidos"],
    "Victoria",
    np.where(
        matches["Goles"] < matches["Goles recibidos"],
        "Derrota",
        "Empate"
    )
)

wins = matches[
    matches["Resultado"] == "Victoria"
]

losses = matches[
    matches["Resultado"] == "Derrota"
]

# -----------------------------------------------------
# VARIABLES CLAVE
# -----------------------------------------------------

variables = {

    "Posesión":
    "Posesión del balón, %",

    "Pases progresivos":
    "Pases progresivos conseguidos",

    "Pases hacia delante":
    "Pases hacia adelante logrados",

    "Pases largos":
    "Pases largos logrados",

    "Recuperaciones altas":
    "Balones recuperados último tercio"

}

rows = []

for label, column in variables.items():

    win_value = wins[column].mean()

    loss_value = losses[column].mean()

    rows.append({

        "Variable": label,

        "Victoria": round(win_value, 2),

        "Derrota": round(loss_value, 2),

        "Diferencia": round(
            win_value - loss_value,
            2
        )

    })

comparison_df = pd.DataFrame(rows)

# -----------------------------------------------------
# VISUAL
# -----------------------------------------------------

fig = go.Figure()

fig.add_trace(

    go.Bar(

        y=comparison_df["Variable"],

        x=comparison_df["Victoria"],

        name="Victoria",

        orientation="h"
    )

)

fig.add_trace(

    go.Bar(

        y=comparison_df["Variable"],

        x=comparison_df["Derrota"],

        name="Derrota",

        orientation="h"
    )

)

fig.update_layout(

    barmode="group",

    height=500,

    title="Victoria vs Derrota",

    paper_bgcolor="#071329",

    plot_bgcolor="#071329",

    font=dict(
        color="#FFFFFF"
    ),

    legend=dict(
        font=dict(
            color="#FFFFFF",
            size=14
        )
    ),

    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# CONCLUSIONES AUTOMÁTICAS
# -----------------------------------------------------

comparison_df["Delta_%"] = (

    (
        comparison_df["Victoria"]
        -
        comparison_df["Derrota"]
    )

    /

    comparison_df["Derrota"]

) * 100

top3 = (

    comparison_df

    .sort_values(
        "Delta_%",
        ascending=False
    )

    .head(3)

)

st.markdown(
    "### 📌 Lo que más cambia cuando gana"
)

for _, row in top3.iterrows():

    st.info(

        f"""
        {row['Variable']}

        +{row['Delta_%']:.0f}% respecto a las derrotas
        """

    )

# =====================================================
# PRODUCCIÓN → RENDIMIENTO
# =====================================================

st.markdown(
    "## ⚽ Producción → Rendimiento"
)

# -----------------------------------------------------
# MÉTRICAS
# -----------------------------------------------------

xg = team_summary["xG"]

goals = team_summary["Goles"]

shots = team_summary["Tiros totales"]

shots_on_target = team_summary["Tiros a portería"]

# -----------------------------------------------------
# RATIOS
# -----------------------------------------------------

goal_per_xg = goals / xg if xg > 0 else 0

shot_accuracy = (
    shots_on_target / shots
    if shots > 0
    else 0
)

goal_per_shot_ot = (
    goals / shots_on_target
    if shots_on_target > 0
    else 0
)

# -----------------------------------------------------
# PERCENTILES LIGA
# -----------------------------------------------------

goal_per_xg_league = (
    summary["Goles"] /
    summary["xG"]
)

shot_accuracy_league = (
    summary["Tiros a portería"] /
    summary["Tiros totales"]
)

goal_per_shot_league = (
    summary["Goles"] /
    summary["Tiros a portería"]
)

pct_goal_xg = (
    goal_per_xg_league.rank(
        pct=True
    )[summary["Equipo"] == team]
    .iloc[0]
    * 100
)

pct_accuracy = (
    shot_accuracy_league.rank(
        pct=True
    )[summary["Equipo"] == team]
    .iloc[0]
    * 100
)

pct_conversion = (
    goal_per_shot_league.rank(
        pct=True
    )[summary["Equipo"] == team]
    .iloc[0]
    * 100
)

# -----------------------------------------------------
# KPIS
# -----------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Finalización",
        round(goal_per_xg, 2)
    )

with c2:

    st.metric(
        "Precisión",
        f"{shot_accuracy*100:.0f}%"
    )

with c3:

    st.metric(
        "Eficacia",
        round(goal_per_shot_ot, 2)
    )

# -----------------------------------------------------
# CONTEXTO
# -----------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.caption(
        f"Percentil Liga: {pct_goal_xg:.0f}"
    )

with c2:

    st.caption(
        f"Percentil Liga: {pct_accuracy:.0f}"
    )

with c3:

    st.caption(
        f"Percentil Liga: {pct_conversion:.0f}"
    )

# -----------------------------------------------------
# INTERPRETACIÓN
# -----------------------------------------------------

if goal_per_xg >= 1.05:

    finishing_text = (
        "Convierte por encima de lo esperado."
    )

elif goal_per_xg <= 0.95:

    finishing_text = (
        "Convierte por debajo de lo esperado."
    )

else:

    finishing_text = (
        "Su conversión está alineada con lo esperado."
    )

if shot_accuracy >= 0.35:

    accuracy_text = (
        "Genera un porcentaje elevado de remates entre palos."
    )

elif shot_accuracy <= 0.25:

    accuracy_text = (
        "Le cuesta convertir tiros en remates a portería."
    )

else:

    accuracy_text = (
        "Presenta una precisión media en el remate."
    )

if goal_per_shot_ot >= 0.40:

    efficiency_text = (
        "Necesita pocos remates a portería para marcar."
    )

elif goal_per_shot_ot <= 0.25:

    efficiency_text = (
        "Necesita un volumen elevado de remates a portería para convertir."
    )

else:

    efficiency_text = (
        "Presenta una eficacia media en la finalización."
    )
st.info(
    f"""
    🎯 {finishing_text}

    ⚽ {accuracy_text}x
    """
)


# =====================================================
# ¿CÓMO PROGRESA?
# =====================================================

st.markdown(
    "## 🔄 ¿Cómo progresa?"
)

# -----------------------------------------------------
# VARIABLES
# -----------------------------------------------------

progression_metrics = {

    "Pases hacia adelante intentados":
    "Pases hacia adelante logrados",

    "Pases laterales intentados":
    "Pases laterales logrados",

    "Pases hacia atrás intentados":
    "Pases hacia atrás logrados",

    "Pases progresivos intentados":
    "Pases progresivos conseguidos",

    "Pases largos intentados":
    "Pases largos logrados"

}

rows = []

for label, metric in progression_metrics.items():

    percentile = (

        summary[metric]

        .rank(pct=True)

        [summary["Equipo"] == team]

        .iloc[0]

        * 100

    )

    value = team_summary[metric]

    rows.append({

        "Acción": label,

        "Valor": value,

        "Percentil": round(percentile)

    })

progression_df = pd.DataFrame(rows)

# -----------------------------------------------------
# VISUAL
# -----------------------------------------------------

fig = px.bar(

    progression_df,

    x="Percentil",

    y="Acción",

    orientation="h",

    text="Percentil"

)

fig.update_layout(

    height=450,

    paper_bgcolor="#071329",

    plot_bgcolor="#071329",

    font=dict(
        color="#FFFFFF"
    ),

    xaxis_range=[0,100],
)


st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# LECTURA AUTOMÁTICA
# -----------------------------------------------------

top_metric = progression_df.sort_values(
    "Percentil",
    ascending=False
).iloc[0]["Acción"]

bottom_metric = progression_df.sort_values(
    "Percentil",
    ascending=True
).iloc[0]["Acción"]

c1, c2 = st.columns(2)

with c1:

    st.info(
        f"""
        Recurso principal de progresión:

        {top_metric}
        """
    )

with c2:

    st.info(
        f"""
        Recurso menos utilizado:

        {bottom_metric}
        """
    )

# =====================================================
# TERRITORIO
# =====================================================

st.markdown(
    "## 🌍 Territorio"
)

# -----------------------------------------------------
# PERCENTILES TERRITORIALES
# -----------------------------------------------------

rec_own_pct = (
    summary["Balones recuperados inicio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

rec_mid_pct = (
    summary["Balones recuperados medio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

rec_high_pct = (
    summary["Balones recuperados último tercio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

loss_own_pct = (
    summary["Balones perdidos inicio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

loss_mid_pct = (
    summary["Balones perdidos medio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

loss_high_pct = (
    summary["Balones perdidos último tercio"]
    .rank(pct=True)
    [summary["Equipo"] == team]
    .iloc[0] * 100
)

territory_df = pd.DataFrame({

    "Zona":[

        "Recupera Campo Propio",
        "Recupera Zona Media",
        "Recupera Campo Rival",

        "Pierde Campo Propio",
        "Pierde Zona Media",
        "Pierde Campo Rival"

    ],

    "Percentil":[

        round(rec_own_pct),
        round(rec_mid_pct),
        round(rec_high_pct),

        round(loss_own_pct),
        round(loss_mid_pct),
        round(loss_high_pct)

    ]

})

fig = px.bar(

    territory_df.sort_values(
        "Percentil"
    ),

    x="Percentil",

    y="Zona",

    orientation="h",

    text="Percentil"

)

fig.update_layout(

    height=500,

    paper_bgcolor="#071329",

    plot_bgcolor="#071329",

    font=dict(
        color="#FFFFFF"
    ),

    title=dict(
        text="Comparado con la Liga",
        font=dict(
            color="#FFFFFF",
            size=20
        )
    ),

    xaxis_range=[0,100]

)

st.plotly_chart(
    fig,
    use_container_width=True
)

best_zone = (

    territory_df

    .sort_values(
        "Percentil",
        ascending=False
    )

    .iloc[0]["Zona"]

)

best_pct = (

    territory_df

    .sort_values(
        "Percentil",
        ascending=False
    )

    .iloc[0]["Percentil"]

)

st.info(
    f"""
    Principal rasgo territorial:

    {best_zone}

    (Percentil {best_pct:.0f} de la competición)
    """
)


# =====================================================
# RECURSOS OFENSIVOS
# =====================================================

st.markdown(
    "## 🎯 ¿De dónde nace el peligro?"
)


# -----------------------------------------------------
# RECURSOS OFENSIVOS
# -----------------------------------------------------

exterior_pct = (

    summary["Centros lanzados"]

    .rank(pct=True)

    [summary["Equipo"] == team]

    .iloc[0]

    * 100

)

transition_pct = (

    summary["Contraataques finalizados"]

    .rank(pct=True)

    [summary["Equipo"] == team]

    .iloc[0]

    * 100

)

positional_pct = (

    summary["Ataques posicionales finalizados"]

    .rank(pct=True)

    [summary["Equipo"] == team]

    .iloc[0]

    * 100

)

resource_df = pd.DataFrame({

    "Mecanismo":[

        "Juego Exterior",
        "Transición",
        "Ataque Posicional"

    ],

    "Percentil":[

        round(exterior_pct),
        round(transition_pct),
        round(positional_pct)

    ]

})

fig = px.bar(

    resource_df.sort_values(
        "Percentil"
    ),

    x="Percentil",

    y="Mecanismo",

    orientation="h",

    text="Percentil"

)

fig.update_layout(

    height=400,

    paper_bgcolor="#071329",

    plot_bgcolor="#071329",

    font=dict(
        color="#FFFFFF"
    ),

    xaxis_title="Percentil Liga",

    yaxis_title=""

)

st.plotly_chart(
    fig,
    use_container_width=True
)

main_resource = (

    resource_df

    .sort_values(
        "Percentil",
        ascending=False
    )

    .iloc[0]["Mecanismo"]

)

main_pct = (

    resource_df

    .sort_values(
        "Percentil",
        ascending=False
    )

    .iloc[0]["Percentil"]

)


st.success(
    f"""
    Recurso ofensivo más característico:

    {main_resource}

    Percentil {main_pct:.0f} respecto a la liga.
    """
)

# =====================================================
# CLAVES DEL RIVAL
# =====================================================

st.markdown(
    "## 📌 Claves del Rival"
)

claves = []

top_factor = comparison_df.sort_values(
    "Diferencia",
    ascending=False
).iloc[0]["Variable"]

claves.append(
    f"Gana cuando incrementa su {top_factor.lower()}."
)

claves.append(
    f"Su principal mecanismo ofensivo es el {main_resource.lower()}."
)

top_progression = progression_df.sort_values(
    "Percentil",
    ascending=False
).iloc[0]["Acción"]

claves.append(
    f"Progresa principalmente mediante {top_progression.lower()}."
)

for clave in claves:

    st.info(clave)