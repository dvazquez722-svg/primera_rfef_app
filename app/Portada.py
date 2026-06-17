import streamlit as st

st.set_page_config(
page_title="Primera RFEF Intelligence",
page_icon="⚽",
layout="wide"
)

# =====================================================

# STYLE

# =====================================================

st.markdown("""

<style>

.hero{

    padding:55px;

    border-radius:25px;

    background:linear-gradient(
        135deg,
        #071329,
        #10284d
    );

    margin-bottom:35px;

    border:1px solid rgba(255,255,255,0.08);

}

.hero-title{

    font-size:56px;
    font-weight:800;
    color:white;

}

.hero-sub{

    font-size:20px;
    color:#b8c5d6;

    margin-top:15px;

}

.module-card{

    background:#071329;

    padding:30px;

    border-radius:20px;

    min-height:260px;

    border:1px solid rgba(255,255,255,0.08);

}

.module-title{

    font-size:28px;
    font-weight:700;
    color:white;

    margin-bottom:15px;

}

.module-text{

    color:#c9d4e3;
    font-size:16px;
    line-height:1.8;

}

.metric-card{

    background:#071329;

    padding:25px;

    border-radius:18px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.08);

}

.metric-number{

    font-size:42px;

    font-weight:800;

    color:white;

}

.metric-label{

    color:#b8c5d6;

    font-size:15px;

}

</style>

""",
unsafe_allow_html=True)

# =====================================================

# HERO

# =====================================================

st.markdown("""

<div class="hero">

<div class="hero-title">
⚽ Primera RFEF Intelligence
</div>

<div class="hero-sub">
Plataforma integral de análisis competitivo, scouting, vídeo y preparación de partido para fútbol profesional.
</div>

</div>
""",
unsafe_allow_html=True)

# =====================================================

# OVERVIEW

# =====================================================

st.markdown("## Ecosistema de Análisis")

c1,c2,c3 = st.columns(3)

with c1:


    st.markdown("""
<div class="metric-card">

<div class="metric-number">
6
</div>

<div class="metric-label">
Módulos Integrados
</div>

</div>
""",
unsafe_allow_html=True)


with c2:


    st.markdown("""
<div class="metric-card">

<div class="metric-number">
DATOS
</div>

<div class="metric-label">
Scouting y Rendimiento
</div>

</div>
""",
unsafe_allow_html=True)


with c3:


    st.markdown("""
<div class="metric-card">

<div class="metric-number">
VIDEO
</div>

<div class="metric-label">
Análisis Táctico Integrado
</div>

</div>
""",
unsafe_allow_html=True)


st.markdown("")

# =====================================================

# MODULOS

# =====================================================

c1,c2,c3 = st.columns(3)

with c1:


    st.markdown("""
<div class="module-card">

<div class="module-title">
📊 Análisis de Liga
</div>

<div class="module-text">

Contexto competitivo global.

Rankings.

Tendencias.

Comparación entre equipos.

</div>

</div>
""",
unsafe_allow_html=True)


with c2:


    st.markdown("""
<div class="module-card">

<div class="module-title">
🎯 Scouting Equipo
</div>

<div class="module-text">

Fortalezas.

Debilidades.

Indicadores clave.

Comparación competitiva.

</div>

</div>
""",
unsafe_allow_html=True)


with c3:


    st.markdown("""
<div class="module-card">

<div class="module-title">
🏟️ Perfil Táctico
</div>

<div class="module-text">

Construcción.

Progresión.

Finalización.

Comportamiento defensivo.

</div>

</div>
""",
unsafe_allow_html=True)


st.markdown("")

c4,c5,c6 = st.columns(3)

with c4:


    st.markdown("""
<div class="module-card">

<div class="module-title">
🕵️ Informe de Rival
</div>

<div class="module-text">

Qué necesita para ganar.

Recursos ofensivos.

Vulnerabilidades.

Tendencias competitivas.

</div>

</div>
""",
unsafe_allow_html=True)


with c5:


    st.markdown("""
<div class="module-card">

<div class="module-title">
🎥 Video Intelligence
</div>

<div class="module-text">

Biblioteca de clips.

Organización táctica.

Acceso rápido.

Preparación de reuniones.

</div>

</div>
""",
unsafe_allow_html=True)


with c6:


    st.markdown("""
<div class="module-card">

<div class="module-title">
👤 Scouting Individual
</div>

<div class="module-text">

KPIs específicos.

Jugadores clave.

Vídeo individual.

Integración datos-vídeo.

</div>

</div>
""",
unsafe_allow_html=True)
    

st.divider()

# =====================================================

# FILOSOFIA

# =====================================================

st.markdown("""
<div class="hero">

<h2 style="color:white;">
⚙️ Datos + Contexto + Vídeo
</h2>

<div style="
color:white;
font-size:19px;
line-height:2;
">

El objetivo no es únicamente describir lo que ocurre.<br><br>

La plataforma está diseñada para transformar datos y vídeo en información accionable para entrenadores, analistas y cuerpos técnicos.<br><br>

Desde el contexto competitivo de la liga hasta la preparación específica de un rival o un jugador concreto.

</div>

</div>
""",
unsafe_allow_html=True)