import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from math import cos, sin, radians

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Comparador de Equipos",
    page_icon="⚔️",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown(
    """
<style>

/* =====================================================
   STREAMLIT
===================================================== */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* =====================================================
   CONTENEDOR
===================================================== */

.block-container{

    max-width:1600px;

    padding-top:1rem;
    padding-bottom:2rem;

    padding-left:2rem;
    padding-right:2rem;
}

/* =====================================================
   TITULOS
===================================================== */

h1{

    font-size:2.6rem !important;

    font-weight:800 !important;

    color:#000000 !important;

    letter-spacing:-1px;
}

h2{

    font-weight:800 !important;

    color:#000000 !important;
}

h3{

    font-weight:800 !important;

    color:##000000 !important;

    opacity:1 !important;
}

/* =====================================================
   SELECTBOXES
===================================================== */

.stSelectbox label{

    color:#cbd5e1 !important;

    font-weight:600 !important;
}

/* =====================================================
   MÉTRICAS
===================================================== */

div[data-testid="stMetric"]{

    background:linear-gradient(
        135deg,
        rgba(15,23,42,0.98),
        rgba(30,41,59,0.95)
    );

    border:1px solid rgba(255,255,255,0.08);

    border-radius:18px;

    padding:18px;

    box-shadow:
        0 6px 25px rgba(0,0,0,0.25);
}

div[data-testid="stMetricLabel"]{

    color:#ffffff !important;

    font-weight:700 !important;

    opacity:1 !important;

    font-size:0.9rem !important;
}

div[data-testid="stMetricValue"]{

    color:#ffffff !important;

    font-weight:800 !important;

    font-size:2rem !important;
}

div[data-testid="stMetricDelta"]{

    font-weight:700 !important;
}

/* =====================================================
   MARKDOWN
===================================================== */

[data-testid="stMarkdownContainer"] p{

    color:#e2e8f0 !important;

    line-height:1.6 !important;
}


/* =====================================================
   DIVIDER
===================================================== */

hr{

    border-color:rgba(255,255,255,0.08);
}

/* =====================================================
   SCROLL
===================================================== */

::-webkit-scrollbar{

    width:8px;
}

::-webkit-scrollbar-thumb{

    background:#475569;

    border-radius:10px;
}

</style>
""",
    unsafe_allow_html=True
)

# =====================================================
# LOAD DATA
# =====================================================

tactical = pd.read_csv(
    "data/processed/team_tactical_profile.csv"
)

summary = pd.read_csv(
    "data/processed/team_summary.csv"
)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
# ⚔️ Comparador de Equipos

Comparación táctica y competitiva entre equipos de Primera Federación.
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

# =====================================================
# DATOS EQUIPOS
# =====================================================

teamA_tac = tactical[
    tactical["Equipo"] == team_a
].iloc[0]

teamB_tac = tactical[
    tactical["Equipo"] == team_b
].iloc[0]

teamA_sum = summary[
    summary["Equipo"] == team_a
].iloc[0]

teamB_sum = summary[
    summary["Equipo"] == team_b
].iloc[0]

# =====================================================
# MÉTRICAS TÁCTICAS
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

# =====================================================
# SCORES
# =====================================================

score_a = round(
    teamA_tac[metrics].mean(),
    1
)

score_b = round(
    teamB_tac[metrics].mean(),
    1
)

score_diff = round(
    abs(score_a - score_b),
    1
)

if score_a > score_b:

    favorite = team_a

elif score_b > score_a:

    favorite = team_b

else:

    favorite = "Igualados"

# =====================================================
# ARQUETIPOS
# =====================================================

def get_archetype(row):

    top3 = (
        row[metrics]
        .sort_values(
            ascending=False
        )
        .head(3)
        .index
        .tolist()
    )

    if (
        "Dominio" in top3
        and "Solidez" in top3
    ):

        return "🧠🔒 Dominador Controlador"

    elif (
        "Verticalidad" in top3
        and "Agresividad" in top3
    ):

        return "⚡💣 Transición Vertical"

    elif (
        "Presion" in top3
        and "Solidez" in top3
    ):

        return "🔥🛡️ Muralla Presionante"

    elif (
        "Dominio" in top3
        and "Verticalidad" in top3
    ):

        return "🚀 Dominio Vertical"

    elif (
        "Agresividad" in top3
        and "Efectividad" in top3
    ):

        return "💣🎯 Ataque Élite"

    else:

        return "⚽ Perfil Mixto"

archetype_a = get_archetype(
    teamA_tac
)

archetype_b = get_archetype(
    teamB_tac
)

# =====================================================
# HERO
# =====================================================

st.markdown(
f"""
<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(
135deg,
#071329,
#1e293b
);
border:1px solid rgba(255,255,255,0.08);
margin-bottom:25px;
">

<h1 style="
margin:0;
font-size:52px;
font-weight:800;
color:white;
text-align:center;
">

⚔️ {team_a} vs {team_b}

</h1>

<div style="
margin-top:10px;
text-align:center;
font-size:26px;
font-weight:700;
color:#38bdf8;
">

{archetype_a}

<br>

vs

<br>

{archetype_b}

</div>

</div>
""",
unsafe_allow_html=True
)

# =====================================================
# KPI HERO
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        team_a,
        score_a
    )

with c2:

    st.metric(
        team_b,
        score_b
    )

with c3:

    st.metric(
        "Ventaja Global",
        score_diff
    )

with c4:

    st.metric(
        "Favorito",
        favorite
    )

st.divider()

# =====================================================
# CARA A CARA TÁCTICO
# =====================================================

st.subheader("⚔️ Cara a Cara Táctico")

for metric in metrics:

    value_a = round(
        teamA_tac[metric],
        1
    )

    value_b = round(
        teamB_tac[metric],
        1
    )

    if value_a > value_b:

        winner = team_a
        color = "#22c55e"

    elif value_b > value_a:

        winner = team_b
        color = "#ef4444"

    else:

        winner = "Empate"
        color = "#94a3b8"

    diff = abs(
        round(value_a - value_b, 1)
    )

    st.markdown(
        f"""
<div style="
padding:20px;
margin-bottom:14px;
background:linear-gradient(
135deg,
#071329,
#1e293b
);
border-radius:18px;
border-left:6px solid {color};
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
">

<div style="
width:35%;
">

<div style="
font-size:14px;
color:#cbd5e1;
">
{team_a}
</div>

<div style="
font-size:34px;
font-weight:800;
color:white;
">
{value_a}
</div>

</div>

<div style="
width:30%;
text-align:center;
">

<div style="
font-size:20px;
font-weight:800;
color:white;
margin-bottom:5px;
">
{metric}
</div>

<div style="
font-size:14px;
color:{color};
font-weight:700;
">
Ventaja: {winner}
</div>

<div style="
margin-top:6px;
font-size:13px;
color:#94a3b8;
">
Diferencia: {diff}
</div>

</div>

<div style="
width:35%;
text-align:right;
">

<div style="
font-size:14px;
color:#cbd5e1;
">
{team_b}
</div>

<div style="
font-size:34px;
font-weight:800;
color:white;
">
{value_b}
</div>

</div>

</div>

</div>
""",
        unsafe_allow_html=True
    )

# =====================================================
# ADN COMPARATIVO PRO
# =====================================================

st.subheader("🕸️ ADN Comparativo Pro")

metrics = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Efectividad",
    "Eficiencia"
]

values_a = [float(teamA_tac[m]) for m in metrics]
values_b = [float(teamB_tac[m]) for m in metrics]

metrics_closed = metrics + [metrics[0]]
values_a_closed = values_a + [values_a[0]]
values_b_closed = values_b + [values_b[0]]

fig = go.Figure()

# =====================================================
# EQUIPO A
# =====================================================

fig.add_trace(

    go.Scatterpolar(

        r=values_a_closed,

        theta=metrics_closed,

        mode="lines+markers",

        line=dict(
            color="#00C2FF",
            width=6
        ),

        marker=dict(
            size=12,
            color="#00C2FF"
        ),

        fill="toself",

        fillcolor="rgba(0,194,255,0.25)",

        name=team_a

    )

)

# =====================================================
# EQUIPO B
# =====================================================

fig.add_trace(

    go.Scatterpolar(

        r=values_b_closed,

        theta=metrics_closed,

        mode="lines+markers",

        line=dict(
            color="#FF3B5C",
            width=6
        ),

        marker=dict(
            size=12,
            color="#FF3B5C"
        ),

        fill="toself",

        fillcolor="rgba(255,59,92,0.22)",

        name=team_b

    )

)

# =====================================================
# POSICIONES EXTERNAS
# =====================================================

positions = {

    "Dominio": (0.50, 0.97),

    "Verticalidad": (0.84, 0.80),

    "Presion": (0.95, 0.48),

    "Solidez": (0.78, 0.08),

    "Agresividad": (0.22, 0.08),

    "Efectividad": (0.05, 0.45),

    "Eficiencia": (0.16, 0.80)

}

annotations = []
shapes = []

for metric in metrics:

    a = float(teamA_tac[metric])
    b = float(teamB_tac[metric])

    if a >= b:

        value = int(round(a))
        color = "#00C2FF"

    else:

        value = int(round(b))
        color = "#FF3B5C"

    x, y = positions[metric]

    # línea

    shapes.append(

        dict(

            type="line",

            xref="paper",
            yref="paper",

            x0=0.50,
            y0=0.50,

            x1=x,
            y1=y,

            line=dict(
                color="rgba(255,255,255,0.18)",
                width=1
            )

        )

    )

    # etiqueta

    annotations.append(

        dict(

            x=x,
            y=y,

            xref="paper",
            yref="paper",

            showarrow=False,

            align="center",

            text=
            f"<b>{metric.upper()}</b>"
            f"<br><br>"
            f"<span style='font-size:42px'>{value}</span>",

            font=dict(
                size=20,
                color=color
            )

        )

    )

# =====================================================
# LAYOUT
# =====================================================

fig.update_layout(

    height=950,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    showlegend=True,

    legend=dict(

        orientation="h",

        x=0.5,

        y=1.06,

        xanchor="center",

        font=dict(
            size=16,
            color="white"
        )

    ),

    polar=dict(

        domain=dict(
            x=[0.28, 0.72],
            y=[0.22, 0.78]
        ),

        bgcolor="#071329",

        radialaxis=dict(

            range=[0,100],

            tickvals=[20,40,60,80,100],

            tickfont=dict(
                color="white",
                size=14
            ),

            gridcolor="rgba(255,255,255,0.18)",

            linecolor="rgba(255,255,255,0.18)"

        ),

        angularaxis=dict(

            showticklabels=False,

            gridcolor="rgba(255,255,255,0.15)",

            linecolor="rgba(255,255,255,0.15)",

            rotation=90,

            direction="clockwise"

        )

    ),

    annotations=annotations,

    shapes=shapes,

    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )

)

st.markdown(
"""
<div style="
background:linear-gradient(
135deg,
#071329,
#041026
);
padding:30px;
border-radius:24px;
border:1px solid rgba(255,255,255,0.08);
">
""",
unsafe_allow_html=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown(
"</div>",
unsafe_allow_html=True
)

# =====================================================
# RESUMEN RADAR
# =====================================================

st.markdown("### 📊 Lectura del ADN")

cols = st.columns(len(metrics))

for col, metric in zip(cols, metrics):

    a = round(teamA_tac[metric], 1)
    b = round(teamB_tac[metric], 1)

    if a > b:

        winner = team_a
        color = "#22c55e"

    elif b > a:

        winner = team_b
        color = "#ef4444"

    else:

        winner = "Empate"
        color = "#94a3b8"

    with col:

        st.markdown(
            f"""
<div style="
padding:12px;
border-radius:12px;
background:#071329;
text-align:center;
height:180px;
">

<div style="
font-size:13px;
font-weight:700;
color:white;
">
{metric}
</div>

<div style="
margin-top:10px;
font-size:24px;
font-weight:800;
color:#38bdf8;
">
{a}
</div>

<div style="
font-size:20px;
font-weight:700;
color:white;
">
vs
</div>

<div style="
font-size:24px;
font-weight:800;
color:#93c5fd;
">
{b}
</div>

<div style="
margin-top:8px;
font-size:12px;
font-weight:700;
color:{color};
">
{winner}
</div>

</div>
""",
            unsafe_allow_html=True
        )

st.divider()

# =====================================================
# ANALISIS DEL ENFRENTAMIENTO
# =====================================================

st.subheader(
    "⚔️ Análisis del Enfrentamiento"
)

diffs = []

for metric in metrics:

    diff = round(
        teamA_tac[metric]
        - teamB_tac[metric],
        1
    )

    diffs.append(
        (metric, diff)
    )

diffs = sorted(
    diffs,
    key=lambda x: abs(x[1]),
    reverse=True
)

top1 = diffs[0]
top2 = diffs[1]

analysis = f"""

{team_a} presenta una diferencia relevante en
{top1[0]} ({top1[1]:+.1f})
y en {top2[0]} ({top2[1]:+.1f}).

"""

st.markdown(
f"""
<div style="
padding:22px;
background:linear-gradient(
135deg,
#071329,
#041026
);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
">

<h3 style="color:white;">
⚔️ Claves Tácticas
</h3>

<div style="
color:white;
font-size:18px;
line-height:1.5;
">

{team_a} y {team_b}
presentan perfiles claramente diferenciados.

<br>

La mayor diferencia aparece en
<b>{top1[0]}</b>
({top1[1]:+.1f}).

<br>

La segunda dimensión más diferencial es
<b>{top2[0]}</b>
({top2[1]:+.1f}).

<br>

Estas variables probablemente
condicionarán el desarrollo competitivo
del enfrentamiento.

</div>

</div>
""",
unsafe_allow_html=True
)

st.divider()

# =====================================================
# KPIs COMPETITIVOS
# =====================================================

st.subheader(
    "📊 Rendimiento Competitivo"
)

kpi_cols = st.columns(5)

# xG

with kpi_cols[0]:

    delta = round(
        teamA_sum["xG"]
        - teamB_sum["xG"],
        2
    )

    st.metric(
        "⚽ xG",
        round(
            teamA_sum["xG"],
            2
        ),
        delta
    )

# GOLES

with kpi_cols[1]:

    delta = round(
        teamA_sum["Goles"]
        - teamB_sum["Goles"],
        2
    )

    st.metric(
        "🥅 Goles",
        round(
            teamA_sum["Goles"],
            2
        ),
        delta
    )

# POSESIÓN

with kpi_cols[2]:

    delta = round(
        teamA_sum["Posesión del balón, %"]
        - teamB_sum["Posesión del balón, %"],
        1
    )

    st.metric(
        "🧠 Posesión",
        f"{teamA_sum['Posesión del balón, %']:.1f}%",
        delta
    )

# PPDA

with kpi_cols[3]:

    delta = round(
        teamA_sum["PPDA"]
        - teamB_sum["PPDA"],
        2
    )

    st.metric(
        "🔥 PPDA",
        round(
            teamA_sum["PPDA"],
            2
        ),
        delta,
        delta_color="inverse"
    )

# GOLES RECIBIDOS

with kpi_cols[4]:

    delta = round(
        teamA_sum["Goles recibidos"]
        - teamB_sum["Goles recibidos"],
        2
    )

    st.metric(
        "🛡️ Encajados",
        round(
            teamA_sum["Goles recibidos"],
            2
        ),
        delta,
        delta_color="inverse"
    )

st.divider()

# =====================================================
# INFORME AUTOMATICO
# =====================================================

st.subheader(
    "📋 Informe Automático"
)

dominant_team = (
    team_a
    if teamA_tac["Dominio"] >
    teamB_tac["Dominio"]
    else team_b
)

vertical_team = (
    team_a
    if teamA_tac["Verticalidad"] >
    teamB_tac["Verticalidad"]
    else team_b
)

press_team = (
    team_a
    if teamA_tac["Presion"] >
    teamB_tac["Presion"]
    else team_b
)

solid_team = (
    team_a
    if teamA_tac["Solidez"] >
    teamB_tac["Solidez"]
    else team_b
)

st.markdown(
f"""
<div style="
padding:22px;
background:linear-gradient(
135deg,
#071329,
#041026
);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
">

<h3 style="color:white;">
🤖 Lectura del Partido
</h3>

<div style="
color:white;
font-size:18px;
line-height:1.5;
">

<b>Control del juego:</b>
{dominant_team}

<br>

<b>Mayor verticalidad:</b>
{vertical_team}

<br>

<b>Presión más agresiva:</b>
{press_team}

<br>

<b>Mayor solidez defensiva:</b>
{solid_team}

<br>

El enfrentamiento presenta perfiles
complementarios y diferencias tácticas
suficientes para generar comportamientos
competitivos claramente diferenciados.

</div>

</div>
""",
unsafe_allow_html=True
)

st.divider()

# =====================================================
# POSICIONAMIENTO TACTICO
# =====================================================

st.subheader(
    "🌍 Posicionamiento Táctico"
)

left, right = st.columns(
    [3,1]
)

with left:

    fig_map = px.scatter(

        tactical,

        x="Dominio",

        y="Verticalidad",

        size="Eficiencia",

        color="Presion",

        text="Equipo",

        color_continuous_scale="RdYlGn",

        height=450
    )

    fig_map.add_scatter(

        x=[teamA_tac["Dominio"]],

        y=[teamA_tac["Verticalidad"]],

        mode="markers+text",

        text=[team_a],

        textposition="top center",

        marker=dict(

            size=40,

            color="#38bdf8",

            line=dict(
                width=3,
                color="white"
            )
        ),

        name=team_a
    )

    fig_map.add_scatter(

        x=[teamB_tac["Dominio"]],

        y=[teamB_tac["Verticalidad"]],

        mode="markers+text",

        text=[team_b],

        textposition="bottom center",

        marker=dict(

            size=40,

            color="#ef4444",

            line=dict(
                width=3,
                color="white"
            )
        ),

        name=team_b
    )

    fig_map.add_vline(
        x=tactical["Dominio"].mean(),
        line_dash="dash",
        line_color="gray"
    )

    fig_map.add_hline(
        y=tactical["Verticalidad"].mean(),
        line_dash="dash",
        line_color="gray"
    )

    fig_map.update_layout(

        height=700,

        paper_bgcolor="#071329",
        plot_bgcolor="#071329",

        font=dict(
            color="white"
        ),

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        showlegend=False,

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        )
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

with right:

    st.markdown(
        f"""
<div style="
padding:25px;
background:linear-gradient(
135deg,
#020817,
#071329,
#0f172a
);
border-radius:18px;
min-height:420px;
">

<h3 style="color:white;">
📌 Lectura del Mapa
</h3>

<div style="
color:white;
font-size:17px;
line-height:1.5;
">

<b>{team_a}</b>

<br>

Dominio:
{teamA_tac["Dominio"]:.0f}

<br>

Verticalidad:
{teamA_tac["Verticalidad"]:.0f}

<br>

<b>{team_b}</b>

<br>

Dominio:
{teamB_tac["Dominio"]:.0f}

<br>

Verticalidad:
{teamB_tac["Verticalidad"]:.0f}

<br>

La distancia entre ambos equipos
permite visualizar rápidamente
el grado de similitud táctica
existente entre los modelos.

</div>

</div>
""",
        unsafe_allow_html=True
    )

st.divider()

# =====================================================
# EQUIPOS SIMILARES
# =====================================================

st.subheader(
    f"🔍 Equipos similares a {team_a}"
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

similar_df = (
    similar_df
    .sort_values(
        "Distancia"
    )
    .head(5)
)

cols = st.columns(5)

for col, (_, row) in zip(
    cols,
    similar_df.iterrows()
):

    similarity_score = max(
        0,
        100 - row["Distancia"]
    )

    with col:

        st.markdown(
            f"""
<div style="
height:220px;
padding:18px;
background:linear-gradient(
135deg,
#071329,
#041026
);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
text-align:center;
">

<div style="
font-size:40px;
margin-top:5px;
">
⚽
</div>

<div style="
margin-top:10px;
font-size:26px;
font-weight:700;
color:white;
">

{row["Equipo"]}

</div>

<div style="
margin-top:10px;
font-size:26px;
font-weight:800;
color:#38bdf8;
">

{similarity_score:.0f}%

</div>

<div style="
margin-top:8px;
font-size:12px;
color:#cbd5e1;
">

Similitud táctica

</div>

</div>
""",
            unsafe_allow_html=True
        )

st.caption(
    """
La similitud se calcula utilizando las siete dimensiones tácticas
del modelo: Dominio, Verticalidad, Presión, Solidez,
Agresividad, Efectividad y Eficiencia.
"""
)

st.divider()