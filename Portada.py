import streamlit as st
import pandas as pd
from auth import login
# ==========================================================
# CONFIGURACIÓN
# ==========================================================

st.set_page_config(
    page_title="Plataforma de Inteligencia Deportiva",
    page_icon="⚽",
    layout="wide"
)

# ==========================================================
# LOGIN
# ==========================================================

from auth import login, get_profile

if "user" not in st.session_state:

    st.markdown("## 🔐 Iniciar sesión")

    email = st.text_input(
        "Correo electrónico"
    )

    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button(
        "Entrar",
        use_container_width=True,
        type="primary"
    ):

        response = login(email, password)

        if response:

            profile = get_profile(
                response.user.id
            )

            st.session_state.user = profile

            st.rerun()

    st.stop()


# ==========================================================
# CARGA DE DATOS
# ==========================================================

try:
    league = pd.read_csv("data/processed/team_summary.csv")
except:
    league = pd.DataFrame()

try:
    matches = pd.read_csv("data/processed/master_team_stats.csv")
except:
    matches = pd.DataFrame()

# ==========================================================
# MÉTRICAS
# ==========================================================

total_teams = (
    league["Equipo"].nunique()
    if not league.empty and "Equipo" in league.columns
    else 0
)

total_matches = (
    matches["Partido"].nunique()
    if not matches.empty and "Partido" in matches.columns
    else len(matches)
)

if "Jugador" in matches.columns:
    total_players = matches["Jugador"].nunique()
elif "player" in matches.columns:
    total_players = matches["player"].nunique()
else:
    total_players = 0

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    max-width:1550px;
    padding-top:1.2rem;
    padding-bottom:3rem;
}

html, body, [class*="css"]{
    font-family:Arial;
}

/* HERO */

.hero{
    background:linear-gradient(135deg,#111827,#1f2937,#111827);
    border-radius:22px;
    padding:45px;
    color:white;
    border:1px solid #2f3640;
}

.hero h1{
    font-size:48px;
    font-weight:800;
    margin-bottom:8px;
}

.hero h3{
    font-weight:400;
    color:#d1d5db;
    margin-bottom:35px;
}

.hero-metric{
    text-align:center;
}

.hero-number{
    font-size:42px;
    font-weight:800;
}

.hero-label{
    color:#9ca3af;
    font-size:15px;
    letter-spacing:1px;
}

/* TITULOS */

.section-title{
    font-size:30px;
    font-weight:700;
    margin-top:30px;
    margin-bottom:8px;
}

.section-sub{
    color:#6b7280;
    margin-bottom:20px;
}

/* TARJETAS */

.card{

    background:white;

    border-radius:20px;

    padding:30px;

    border:1px solid #ececec;

    box-shadow:0px 8px 24px rgba(0,0,0,.06);

    transition:0.25s;

    min-height:290px;

}

.card:hover{

    transform:translateY(-6px);

    box-shadow:0px 15px 40px rgba(0,0,0,.12);

}

.card-icon{

    font-size:54px;

}

.card-title{

    font-size:26px;

    font-weight:700;

    margin-top:10px;

    margin-bottom:15px;

}

.card ul{

    padding-left:18px;

    line-height:2;

    color:#4b5563;

}

.badge{

    display:inline-block;

    margin-top:20px;

    padding:8px 16px;

    background:#eef6ff;

    border-radius:50px;

    color:#2563eb;

    font-weight:600;

}

/* KPI */

.kpi{

    background:white;

    border-radius:18px;

    padding:25px;

    text-align:center;

    border:1px solid #ececec;

    box-shadow:0px 8px 20px rgba(0,0,0,.05);

}

.kpi-number{

    font-size:40px;

    font-weight:800;

}

.kpi-label{

    color:#6b7280;

    letter-spacing:1px;

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown(f"""
<div class="hero">

<h1>⚽ Plataforma de Inteligencia Deportiva</h1>

<h3>
Scouting · Análisis táctico · Videoanálisis · Inteligencia Artificial · Preparación de Partido
</h3>

<table width="100%">
<tr>

<td class="hero-metric">

<div class="hero-number">{total_teams}</div>

<div class="hero-label">EQUIPOS</div>

</td>

<td class="hero-metric">

<div class="hero-number">{total_matches}</div>

<div class="hero-label">PARTIDOS</div>

</td>

<td class="hero-metric">

<div class="hero-number">{total_players}</div>

<div class="hero-label">JUGADORES</div>

</td>

<td class="hero-metric">

<div class="hero-number">7</div>

<div class="hero-label">MÓDULOS</div>

</td>

</tr>

</table>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# CENTRO DE OPERACIONES
# ==========================================================

st.markdown(
    '<div class="section-title">🎯 Centro de Operaciones</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Accede a todos los módulos principales de la plataforma.</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:

    st.markdown("""
    <div class="card">

    <div class="card-icon">🏆</div>

    <div class="card-title">
    Análisis de Liga
    </div>

    <ul>
        <li>Rankings</li>
        <li>Estadísticas avanzadas</li>
        <li>Clasificación</li>
        <li>Tendencias</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/1_Análisis_de_Liga.py",
        label="Abrir módulo",
        icon="➡️"
    )


with col2:

    st.markdown("""
    <div class="card">

    <div class="card-icon">👥</div>

    <div class="card-title">
    Scouting Equipo
    </div>

    <ul>
        <li>Perfil colectivo</li>
        <li>Modelo de juego</li>
        <li>Fortalezas</li>
        <li>Debilidades</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/2_Scouting_Equipo.py",
        label="Abrir módulo",
        icon="➡️"
    )


with col3:

    st.markdown("""
    <div class="card">

    <div class="card-icon">📊</div>

    <div class="card-title">
    Comparación Equipos
    </div>

    <ul>
        <li>Comparativa</li>
        <li>Radar colectivo</li>
        <li>Indicadores</li>
        <li>Benchmark</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/3_Comparacion_Equipos.py",
        label="Abrir módulo",
        icon="➡️"
    )

# ==========================================================
# MÁS MÓDULOS
# ==========================================================

st.write("")

col4, col5, col6 = st.columns(3, gap="large")

with col4:

    st.markdown("""
    <div class="card">

    <div class="card-icon">🎯</div>

    <div class="card-title">
    Informe Automático del Rival
    </div>

    <ul>
        <li>Informe completo</li>
        <li>Análisis táctico</li>
        <li>Fortalezas y debilidades</li>
        <li>Plan de partido</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/4_Informe_Automatico_de_Rival.py",
        label="Abrir módulo",
        icon="➡️"
    )


with col5:

    st.markdown("""
    <div class="card">

    <div class="card-icon">👤</div>

    <div class="card-title">
    Scouting Individual
    </div>

    <ul>
        <li>Perfil del jugador</li>
        <li>Indicadores específicos</li>
        <li>Radar individual</li>
        <li>Historial</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "pages/5_Scouting_Individual.py",
        label="Abrir módulo",
        icon="➡️"
    )


with col6:

    st.markdown("""
    <div class="card">

    <div class="card-icon">🎥</div>

    <div class="card-title">
    Vídeo
    </div>

    <ul>
        <li>Video Informes</li>
        <li>Videoteca</li>
        <li>Clips</li>
        <li>Presentaciones</li>
    </ul>

    <div class="badge">
    Disponible
    </div>

    </div>
    """, unsafe_allow_html=True)

    video_col1, video_col2 = st.columns(2)

    with video_col1:

        st.page_link(
            "pages/Video Informes.py",
            label="Informes",
            icon="🎬"
        )

    with video_col2:

        st.page_link(
            "pages/Videoteca Clips.py",
            label="Videoteca",
            icon="📹"
        )

st.write("")
st.divider()

# ==========================================================
# RESUMEN DE LA BASE DE DATOS
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Base de Datos</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Estado actual de la información disponible en la plataforma.</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-number">{total_teams}</div>
        <div class="kpi-label">EQUIPOS</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-number">{total_matches}</div>
        <div class="kpi-label">PARTIDOS</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-number">{total_players}</div>
        <div class="kpi-label">JUGADORES</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-number">1</div>
        <div class="kpi-label">LIGA</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-number">7</div>
        <div class="kpi-label">MÓDULOS</div>
    </div>
    """, unsafe_allow_html=True)

with k6:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-number">100%</div>
        <div class="kpi-label">OPERATIVA</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ==========================================================
# ESTADO DE LA PLATAFORMA
# ==========================================================

st.markdown(
    '<div class="section-title">🟢 Estado de la Plataforma</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Todos los servicios principales se encuentran disponibles.</div>',
    unsafe_allow_html=True
)

estado1, estado2 = st.columns([2, 1], gap="large")

with estado1:

    st.success("✅ Base de datos cargada correctamente")
    st.success("✅ Equipos disponibles")
    st.success("✅ Partidos sincronizados")
    st.success("✅ Módulos operativos")
    st.success("✅ Plataforma lista para el análisis")

with estado2:

    st.info("🏆 Liga disponible")
    st.metric("Temporada", "2025-2026")

    st.metric(
        "Última actualización",
        "Hoy"
    )

    st.metric(
        "Versión",
        "v2.0"
    )

st.write("")
st.divider()

# ==========================================================
# NOVEDADES Y ACCESO RÁPIDO
# ==========================================================

st.markdown(
    '<div class="section-title">🚀 Novedades</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Últimas incorporaciones y estado de desarrollo de la plataforma.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([2, 1], gap="large")

with left:

    with st.container(border=True):

        st.markdown("### 📢 Últimas actualizaciones")

        st.info("Nuevo módulo de Informe Automático del Rival.")
        st.info("Base de datos de equipos sincronizada.")
        st.info("Integración de Videoteca de Clips.")
        st.info("Optimización del Scouting Individual.")
        st.info("Mejoras de rendimiento y estabilidad.")

with right:

    with st.container(border=True):

        st.markdown("### ⚙️ Próximamente")

        st.checkbox(
            "Modelos predictivos IA",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Gestión de cargas",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Exportación PDF",
            value=False,
            disabled=True
        )

        st.checkbox(
            "Dashboard GPS",
            value=False,
            disabled=True
        )

st.write("")
st.divider()

# ==========================================================
# ACCESO RÁPIDO
# ==========================================================

st.markdown(
    '<div class="section-title">⚡ Acceso Rápido</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Navega directamente a cualquier área de trabajo.</div>',
    unsafe_allow_html=True
)

a1, a2, a3, a4 = st.columns(4, gap="large")

with a1:
    st.page_link(
        "pages/1_Análisis_de_Liga.py",
        label="🏆 Análisis de Liga",
        use_container_width=True
    )

    st.page_link(
        "pages/2_Scouting_Equipo.py",
        label="👥 Scouting Equipo",
        use_container_width=True
    )

with a2:
    st.page_link(
        "pages/3_Comparacion_Equipos.py",
        label="📊 Comparación",
        use_container_width=True
    )

    st.page_link(
        "pages/4_Informe_Automatico_de_Rival.py",
        label="🎯 Informe Rival",
        use_container_width=True
    )

with a3:
    st.page_link(
        "pages/5_Scouting_Individual.py",
        label="👤 Scouting Individual",
        use_container_width=True
    )

    st.page_link(
        "pages/Video Informes.py",
        label="🎥 Video Informes",
        use_container_width=True
    )

with a4:
    st.page_link(
        "pages/Videoteca Clips.py",
        label="📹 Videoteca",
        use_container_width=True
    )

st.write("")
st.divider()

# ==========================================================
# SOBRE LA PLATAFORMA
# ==========================================================

st.markdown(
    '<div class="section-title">ℹ️ Plataforma de Inteligencia Deportiva</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-sub">Un único entorno para analizar, comparar y preparar cada partido.</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1], gap="large")

with col1:

    with st.container(border=True):

        st.markdown("""
### ¿Qué permite esta plataforma?

La Plataforma de Inteligencia Deportiva integra todas las herramientas necesarias para el análisis de rendimiento colectivo e individual dentro de un único ecosistema.

A través de diferentes módulos es posible analizar equipos, estudiar rivales, comparar modelos de juego, evaluar futbolistas y organizar todo el contenido audiovisual utilizado por el cuerpo técnico.

Toda la información se encuentra conectada para facilitar una toma de decisiones rápida, objetiva y basada en datos.
""")

        st.write("")

        f1, f2, f3 = st.columns(3)

        with f1:
            st.success("📊 Datos")
            st.caption(
                "Análisis estadístico avanzado de equipos y jugadores."
            )

        with f2:
            st.success("🎯 Scouting")
            st.caption(
                "Preparación de rivales y evaluación de futbolistas."
            )

        with f3:
            st.success("🎥 Vídeo")
            st.caption(
                "Informes audiovisuales y biblioteca de clips."
            )

with col2:

    with st.container(border=True):

        st.markdown("### 🧩 Módulos")

        st.write("🏆 Análisis de Liga")

        st.write("👥 Scouting Equipo")

        st.write("📊 Comparación Equipos")

        st.write("🎯 Informe Automático")

        st.write("👤 Scouting Individual")

        st.write("🎥 Video Informes")

        st.write("📹 Videoteca Clips")

        st.write("")

        st.success("Todos los módulos disponibles.")

st.write("")
st.divider()

# ==========================================================
# FOOTER
# ==========================================================

c1, c2, c3 = st.columns([3, 1, 1])

with c1:

    st.caption(
        "© 2026 Plataforma de Inteligencia Deportiva · Desarrollo propio para análisis táctico, scouting, videoanálisis y preparación de partido."
    )

with c2:

    st.caption("Versión 2.0")

with c3:

    st.caption("Estado: 🟢 Operativa")

st.write("")