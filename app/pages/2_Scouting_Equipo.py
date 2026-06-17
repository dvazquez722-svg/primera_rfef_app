import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Scouting Equipo",
    page_icon="📋",
    layout="wide"
)

# =====================================================
# STYLE - SCOUTING PRO
# =====================================================

st.markdown(
    """
<style>

/* =====================================================
   OCULTAR STREAMLIT
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* =====================================================
   CONTENEDOR PRINCIPAL
===================================================== */

.block-container {

    max-width: 1600px;

    padding-top: 1rem;

    padding-bottom: 2rem;

    padding-left: 2rem;

    padding-right: 2rem;
}

/* =====================================================
   TÍTULOS
===================================================== */

h1 {

    font-size: 2.6rem !important;

    font-weight: 800 !important;

    letter-spacing: -1px;

    margin-bottom: 0.3rem;
}

h2 {

    font-size: 1.8rem !important;

    font-weight: 700 !important;
}

h3 {

    font-size: 1.25rem !important;

    font-weight: 700 !important;
}

/* =====================================================
   KPIs
===================================================== */

div[data-testid="stMetric"] {

    background: linear-gradient(
        180deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 16px;

    padding: 20px;

    box-shadow:
        0 4px 20px rgba(0,0,0,0.25);

    transition: 0.2s;
}

div[data-testid="stMetric"]:hover {

    transform: translateY(-2px);

    border: 1px solid rgba(255,255,255,0.15);
}

div[data-testid="stMetricLabel"] {

    font-size: 1rem !important;

    font-weight: 700 !important;

    color: rgba(255,255,255,0.85) !important;

    text-transform: uppercase;

    letter-spacing: 0.8px;
}

div[data-testid="stMetricValue"] {

    font-size: 2rem !important;

    font-weight: 800 !important;

    color: white !important;
}

div[data-testid="stMetric"] label {

    color: white !important;
}

div[data-testid="stMetricDelta"] {

    font-size: 1rem !important;

    font-weight: 700 !important;

    color: #22c55e !important;
}

/* =====================================================
   ALERTAS INFO
===================================================== */

div[data-testid="stAlert"] {

    border-radius: 16px;

    border: 1px solid rgba(255,255,255,0.08);

    padding: 1rem;
}

/* =====================================================
   DATAFRAME
===================================================== */

div[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);
}

/* =====================================================
   SELECTBOX
===================================================== */

div[data-baseweb="select"] {

    border-radius: 12px;
}

/* =====================================================
   SCROLLBAR
===================================================== */

::-webkit-scrollbar {

    width: 8px;
}

::-webkit-scrollbar-track {

    background: transparent;
}

::-webkit-scrollbar-thumb {

    background: #475569;

    border-radius: 10px;
}

/* =====================================================
   SEPARADORES
===================================================== */

hr {

    margin-top: 2rem !important;

    margin-bottom: 2rem !important;

    border-color: rgba(255,255,255,0.08);
}

</style>
""",
    unsafe_allow_html=True
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/team_summary.csv"
)

master_df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

tactical = pd.read_csv(
    "data/processed/team_tactical_profile.csv"
)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
# 📋 Scouting de Equipo

Análisis táctico automatizado · Primera Federación
"""
)

team = st.selectbox(
    "Seleccionar equipo",
    sorted(df["Equipo"].unique())
)

# =====================================================
# TEAM DATA
# =====================================================

team_stats = (
    df[
        df["Equipo"] == team
    ]
    .iloc[0]
)

team_tactical = (
    tactical[
        tactical["Equipo"] == team
    ]
    .iloc[0]
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

team_matches = (
    team_matches
    .sort_values("Fecha")
)

# =====================================================
# VARIABLES TÁCTICAS
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

dom = team_tactical["Dominio"]
vert = team_tactical["Verticalidad"]
pre = team_tactical["Presion"]
sol = team_tactical["Solidez"]
agr = team_tactical["Agresividad"]
efe = team_tactical["Efectividad"]
efi = team_tactical["Eficiencia"]

# =====================================================
# SCORE TÁCTICO
# =====================================================

tactical_score = round(
    team_tactical[radar_metrics].mean(),
    1
)

if tactical_score >= 70:

    tactical_level = "⭐⭐⭐ Élite"

elif tactical_score >= 50:

    tactical_level = "⭐⭐ Competitivo"

elif tactical_score >= 30:

    tactical_level = "⭐ Intermedio"

else:

    tactical_level = "Desarrollo"

# =====================================================
# ARQUETIPO AVANZADO
# =====================================================

top3 = (
    team_tactical[radar_metrics]
    .sort_values(ascending=False)
    .head(3)
)

top_metrics = top3.index.tolist()

if (
    "Dominio" in top_metrics
    and "Solidez" in top_metrics
):

    archetype = "🧠🔒 Dominador Controlador"

elif (
    "Verticalidad" in top_metrics
    and "Agresividad" in top_metrics
):

    archetype = "⚡💣 Transición Vertical"

elif (
    "Presion" in top_metrics
    and "Solidez" in top_metrics
):

    archetype = "🔥🛡️ Muralla Presionante"

elif (
    "Dominio" in top_metrics
    and "Verticalidad" in top_metrics
):

    archetype = "🚀 Dominio Vertical"

elif (
    "Agresividad" in top_metrics
    and "Efectividad" in top_metrics
):

    archetype = "💣🎯 Ataque Élite"

elif (
    "Efectividad" in top_metrics
    and "Eficiencia" in top_metrics
):

    archetype = "🎯🏆 Competidor Clínico"

elif (
    "Solidez" in top_metrics
    and "Eficiencia" in top_metrics
):

    archetype = "🛡️🏆 Equipo Competitivo"

else:
    archetype = f"⚽ Perfil {top_metrics[0]}"

# =====================================================

# CLAVES DEL EQUIPO

# =====================================================

insight_dict = {
"Dominio": "Control del juego y gestión de posesión",
"Verticalidad": "Progresión rápida hacia campo rival",
"Presion": "Capacidad para recuperar arriba",
"Solidez": "Protección del área propia",
"Agresividad": "Volumen ofensivo elevado",
"Efectividad": "Conversión de ocasiones",
"Eficiencia": "Capacidad para transformar rendimiento en resultados"
}

# =====================================================

# RESUMEN EJECUTIVO

# =====================================================

summary = []

if dom >= 65:
    summary.append("controla fases prolongadas de posesión")

if vert >= 65:
    summary.append("progresa rápidamente hacia campo rival")

if pre >= 65:
    summary.append("presiona tras pérdida")

if sol >= 65:
    summary.append("concede pocas ocasiones")

if agr >= 65:
    summary.append("genera volumen ofensivo")

if len(summary) == 0:
    summary.append("presenta un perfil equilibrado")

summary_text = ", ".join(summary)

# =====================================================

# HERO SECTION

# =====================================================

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
border:1px solid rgba(255,255,255,0.08);
margin-bottom:20px;
">

<h1 style="
margin-bottom:0;
font-size:46px;
font-weight:800;
color:white;
">
{team}
</h1>

<h3 style="
margin-top:10px;
color:#38bdf8;
font-weight:700;
">
{archetype}
</h3>

</div>
""",
    unsafe_allow_html=True
)

# =====================================================
# HERO CARDS
# =====================================================

c1, c2, c3, c4, c5 = st.columns([2.2,2.2,2.2,1.2,1.2])

cards = [
    insight_dict[top_metrics[0]],
    insight_dict[top_metrics[1]],
    insight_dict[top_metrics[2]]
]

for col, text in zip(
    [c1,c2,c3],
    cards
):

    with col:

        st.markdown(
            f"""
<div style="
height:145px;
padding:20px;
background:linear-gradient(
135deg,
#071329,
#1e293b
);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
display:flex;
align-items:center;
justify-content:center;
text-align:center;
font-size:19px;
font-weight:700;
color:white;
">

{text}

</div>
""",
            unsafe_allow_html=True
        )

with c4:

    st.markdown(
        f"""
<div style="
height:145px;
padding:15px;
background:linear-gradient(
135deg,
#071329,
#1e293b
);
border-radius:18px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
overflow:hidden;
">

<div style="
font-size:13px;
font-weight:700;
color:#cbd5e1;
">
NIVEL
</div>

<div style="
font-size:32px;
margin-top:8px;
">
⭐
</div>

<div style="
font-size:22px;
font-weight:800;
color:#38bdf8;
margin-top:5px;
">
{tactical_level.replace('⭐','').strip()}
</div>

</div>
""",
        unsafe_allow_html=True
    )

with c5:

    st.markdown(
        f"""
<div style="
height:145px;
padding:20px;
background:linear-gradient(
135deg,
#071329,
#1e293b
);
border-radius:18px;
text-align:center;
">

<div style="
font-size:14px;
color:#cbd5e1;
font-weight:700;
margin-bottom:10px;
">
SCORE
</div>

<div style="
font-size:42px;
font-weight:800;
color:white;
">
{tactical_score}
</div>

</div>
""",
        unsafe_allow_html=True
    )

st.divider()

# =====================================================
# RESUMEN EJECUTIVO
# =====================================================

left, right = st.columns([4,1.4])

with left:

    st.markdown(
        f"""
<div style="
padding:30px;
background:linear-gradient(
135deg,
#071329,
#041026
);
border-radius:18px;
height:240px;
">

<h2 style="
color:white;
margin-top:0;
margin-bottom:20px;
">
📋 Resumen Ejecutivo
</h2>

<div style="
color:white;
font-size:16px;
line-height:1.9;
">

{team} presenta una identidad táctica marcada principalmente por
<b>{top_metrics[0].lower()}</b>,
<b>{top_metrics[1].lower()}</b> y
<b>{top_metrics[2].lower()}</b>.

<br><br>

El equipo alcanza un score táctico de
<b>{tactical_score:.1f}/100</b>
y muestra una tendencia orientada a la generación de ocasiones mediante ataques dinámicos.

<br><br>

Su rendimiento reciente refleja un perfil competitivo estable dentro de la categoría.

</div>

</div>
""",
        unsafe_allow_html=True
    )

with right:

    st.markdown(
        f"""
<div style="
height:240px;
padding:30px;
background:linear-gradient(
135deg,
#071329,
#041026
);
border-radius:18px;
text-align:center;
">

<div style="
font-size:60px;
margin-bottom:10px;
">
🛡️
</div>

<div style="
font-size:14px;
letter-spacing:1px;
color:#cbd5e1;
font-weight:700;
">
IDENTIDAD PRINCIPAL
</div>

<div style="
margin-top:15px;
font-size:28px;
font-weight:800;
color:#38bdf8;
">
{archetype}
</div>

</div>
""",
        unsafe_allow_html=True
    )

st.divider ()

# =====================================================
# KPIs COMPETITIVOS
# =====================================================

st.subheader("📊 KPIs Competitivos")

xg_rank = int(
    df["xG"]
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

ppda_rank = int(
    df["PPDA"]
    .rank(
        ascending=True,
        method="min"
    )
    .loc[df["Equipo"] == team]
    .iloc[0]
)

pos_rank = int(
    df["Posesión del balón, %"]
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

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "⚽ xG",
    round(
        team_stats["xG"],
        2
    ),
    f"#{xg_rank}"
)

c2.metric(
    "🥅 Goles",
    round(
        team_stats["Goles"],
        2
    ),
    f"#{goals_rank}"
)

c3.metric(
    "🧠 Posesión",
    f"{team_stats['Posesión del balón, %']:.1f}%",
    f"#{pos_rank}"
)

c4.metric(
    "🔥 PPDA",
    round(
        team_stats["PPDA"],
        2
    ),
    f"#{ppda_rank}"
)

c5.metric(
    "🛡️ Encajados",
    round(
        team_stats["Goles recibidos"],
        2
    ),
    f"#{def_rank}"
)

st.divider()

st.markdown("### 🌍 Posicionamiento en la Liga")

league_rank = round(
    (
        len(df) - xg_rank + 1
    ) / len(df) * 100
)

st.progress(
    league_rank / 100
)

st.caption(
    f"Producción ofensiva superior al {league_rank:.0f}% de los equipos"
)

# =====================================================
# PERFIL DE JUEGO
# =====================================================

if dom >= 75:
    construccion = "Elaborada"
elif dom >= 55:
    construccion = "Mixta"
else:
    construccion = "Directa"

if vert >= 75:
    progresion = "Vertical"
elif vert >= 55:
    progresion = "Mixta"
else:
    progresion = "Asociativa"

if pre >= 75:
    defensa = "Presión Alta"
elif pre >= 55:
    defensa = "Presión Media"
else:
    defensa = "Bloque Medio/Bajo"

if agr >= 75 and vert >= 70:
    ataque = "Transición"

elif dom >= 70:
    ataque = "Posicional"

else:
    ataque = "Mixto"

# =====================================================
# ADN TÁCTICO
# =====================================================

st.subheader("🕸️ ADN Táctico")

fig = go.Figure()

fig.add_trace(

        go.Scatterpolar(

            r=team_tactical[radar_metrics],

            theta=radar_metrics,

            fill="toself",

            name=team,

            line=dict(
                width=3
            )
        )
    )

fig.update_layout(

        polar=dict(

            radialaxis=dict(

                visible=True,

                range=[0,100]
            )
        ),

        showlegend=False,

        height=550,

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("### ⚔️ Identidad del Equipo")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"""
<div style="
padding:20px;
background:#0f172a;
border-radius:16px;
border-left:5px solid #22c55e;
height:240px;
">

<h4 style="
color:white;
margin-bottom:15px;
">
⚔️ Identidad Ofensiva
</h4>

<div style="
color:white;
font-size:16px;
line-height:1.9;
">

{team} presenta un perfil ofensivo basado principalmente en la
<b>{top_metrics[0].lower()}</b>.

<br><br>

Su comportamiento ofensivo combina niveles de
<b>{vert:.0f}/100</b> en verticalidad y
<b>{agr:.0f}/100</b> en agresividad.

<br><br>

Muestra una clara tendencia a acelerar ataques y alcanzar zonas de finalización con frecuencia.

</div>

</div>

</div>

"""
    ,
    unsafe_allow_html=True
)

with col2:

    st.markdown(
        f"""
<div style="
padding:20px;
background:#0f172a;
border-radius:16px;
border-left:5px solid #ef4444;
height:240px;
">

<h4 style="
color:white;
margin-bottom:15px;
">
🛡️ Identidad Defensiva
</h4>

<div style="
color:white;
font-size:16px;
line-height:1.9;
">

Defensivamente el equipo alcanza
<b>{sol:.0f}/100</b> en solidez y
<b>{pre:.0f}/100</b> en presión.

<br><br>

Su modelo defensivo se caracteriza por proteger el área propia y limitar ocasiones rivales.

<br><br>

Prioriza la estabilidad defensiva frente a una presión constante de alto riesgo.

</div>

</div>

"""
    ,
    unsafe_allow_html=True
)
    
# =====================================================
# FORTALEZAS Y DEBILIDADES
# =====================================================

strength_dict = {

    "Dominio":
    "Controla largos tramos de partido mediante la posesión y la gestión del ritmo de juego.",

    "Verticalidad":
    "Progresa rápidamente hacia zonas de finalización y busca acelerar ataques.",

    "Presion":
    "Presenta capacidad para recuperar el balón en zonas avanzadas del campo.",

    "Solidez":
    "Reduce la generación de ocasiones rivales y protege correctamente su área.",

    "Agresividad":
    "Genera un volumen ofensivo elevado y alcanza con frecuencia zonas de remate.",

    "Efectividad":
    "Convierte ocasiones por encima de la media cuando logra finalizar ataques.",

    "Eficiencia":
    "Obtiene un rendimiento competitivo superior al esperado según su producción."
}

weakness_dict = {

    "Dominio":
    "Presenta dificultades para controlar fases largas de posesión.",

    "Verticalidad":
    "Muestra problemas para progresar con velocidad hacia campo rival.",

    "Presion":
    "Tiene dificultades para recuperar arriba y sostener presión avanzada.",

    "Solidez":
    "Concede situaciones de peligro con frecuencia superior a la media.",

    "Agresividad":
    "Genera menos volumen ofensivo que otros equipos de la competición.",

    "Efectividad":
    "Necesita un número elevado de ocasiones para convertir gol.",

    "Eficiencia":
    "La producción estadística no siempre se traduce en resultados."
}

top3 = (
    team_tactical[radar_metrics]
    .sort_values(
        ascending=False
    )
    .head(3)
)

bottom3 = (
    team_tactical[radar_metrics]
    .sort_values(
        ascending=True
    )
    .head(3)
)

st.divider()

st.subheader(
    "📋 Informe de Scouting"
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "### 🟢 Fortalezas"
    )

    for metric, value in top3.items():

        insight = strength_dict.get(
            metric,
            metric
        )

        st.markdown(
            f"""
<div style="
padding:16px;
margin-bottom:12px;
background:#ecfdf5;
border-left:5px solid #22c55e;
border-radius:10px;
font-size:15px;
line-height:1.7;
">
✓ {insight}
</div>
""",
            unsafe_allow_html=True
        )

with col2:

    st.markdown(
        "### 🔴 Aspectos Mejorables"
    )

    for metric, value in bottom3.items():

        insight = weakness_dict.get(
            metric,
            metric
        )

        st.markdown(
            f"""
<div style="
padding:16px;
margin-bottom:12px;
background:#fef2f2;
border-left:5px solid #ef4444;
border-radius:10px;
font-size:15px;
line-height:1.7;
">
✗ {insight}
</div>
""",
            unsafe_allow_html=True
        )

        
# =====================================================
# FORMA RECIENTE
# =====================================================

st.divider()

st.subheader("📈 Forma Reciente")

last5 = team_matches.tail(5)

# =====================================================
# COMPARACIÓN VS TEMPORADA
# =====================================================

delta_xg = round(
    last5["xG"].mean()
    - team_matches["xG"].mean(),
    2
)

delta_goals = round(
    last5["Goles"].mean()
    - team_matches["Goles"].mean(),
    2
)

delta_conceded = round(
    last5["Goles recibidos"].mean()
    - team_matches["Goles recibidos"].mean(),
    2
)

delta_ppda = round(
    last5["PPDA"].mean()
    - team_matches["PPDA"].mean(),
    2
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "xG últimos 5",
    round(
        last5["xG"].mean(),
        2
    ),
    delta_xg
)

c2.metric(
    "Goles últimos 5",
    round(
        last5["Goles"].mean(),
        2
    ),
    delta_goals
)

c3.metric(
    "Encajados últimos 5",
    round(last5["Goles recibidos"].mean(), 2),
    delta_conceded,
    delta_color="inverse"
)

c4.metric(
    "PPDA últimos 5",
    round(last5["PPDA"].mean(), 2),
    delta_ppda,
    delta_color="inverse"
)

if delta_xg > 0.15:

    trend = "📈 Producción ofensiva en crecimiento"

elif delta_xg < -0.15:

    trend = "📉 Producción ofensiva en descenso"

else:

    trend = "➖ Producción ofensiva estable"

st.info(
    f"""
{trend}

Diferencia respecto a la media anual:
{delta_xg:+.2f} xG por partido.
"""
)

# =====================================================
# EVOLUCIÓN OFENSIVA
# =====================================================

st.subheader("⚽ Evolución Ofensiva")

fig_xg = px.line(
    team_matches,
    x="Fecha",
    y="xG",
    markers=True
)

fig_xg.add_hline(
    y=team_matches["xG"].mean(),
    line_dash="dash",
    line_color="orange",
    annotation_text="Media temporada",
    annotation_position="top left"
)

fig_xg.update_layout(
    height=400,
    xaxis_title="",
    yaxis_title="xG",
    hovermode="x unified"
)

st.plotly_chart(
    fig_xg,
    use_container_width=True
)

# =====================================================
# EVOLUCIÓN PRESIÓN
# =====================================================

st.subheader("🔥 Evolución de la Presión")

fig_ppda = px.line(
    team_matches,
    x="Fecha",
    y="PPDA",
    markers=True
)

fig_ppda.add_hline(
    y=team_matches["PPDA"].mean(),
    line_dash="dash",
    line_color="orange",
    annotation_text="Media temporada",
    annotation_position="top left"
)

fig_ppda.update_layout(
    height=400,
    xaxis_title="",
    yaxis_title="PPDA",
    hovermode="x unified"
)

st.plotly_chart(
    fig_ppda,
    use_container_width=True
)

# =====================================================
# ÚLTIMOS PARTIDOS
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

    goles_favor = row["Goles"]
    goles_contra = row["Goles recibidos"]

    if goles_favor > goles_contra:
        resultado = "🟢 Victoria"
    elif goles_favor == goles_contra:
        resultado = "🟡 Empate"
    else:
        resultado = "🔴 Derrota"

    partido = row.get(
        "Partido",
        "Partido"
    )

    fecha = row["Fecha"].strftime(
        "%d/%m/%Y"
    )

    st.markdown(
        f"""
<div style="
padding:18px;
margin-bottom:12px;
background:linear-gradient(135deg,#0f172a,#1e293b);
border-radius:14px;
border-left:5px solid #38bdf8;
">

<div style="
font-size:18px;
font-weight:700;
color:white;
margin-bottom:8px;
">
{resultado}
</div>

<div style="
font-size:16px;
font-weight:600;
color:white;
margin-bottom:10px;
">
{partido}
</div>

<div style="
display:flex;
gap:30px;
flex-wrap:wrap;
font-size:14px;
color:#cbd5e1;
">

<span>📅 {fecha}</span>

<span>⚽ {int(goles_favor)}-{int(goles_contra)}</span>

<span>📊 xG {row["xG"]:.2f}</span>

</div>

</div>
""",
        unsafe_allow_html=True
    )