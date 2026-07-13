import streamlit as st


# =====================================================
# SCOUTING HEADER
# =====================================================

def show_header(

    team,

    team_stats,

    team_tactical

):

    radar_metrics = [

        "Dominio",

        "Verticalidad",

        "Presion",

        "Solidez",

        "Agresividad",

        "Efectividad",

        "Eficiencia"

    ]

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

    top3 = (

        team_tactical[radar_metrics]

        .sort_values(

            ascending=False

        )

        .head(3)

    )

    top_metrics = top3.index.tolist()

    if (

        "Dominio" in top_metrics

        and

        "Solidez" in top_metrics

    ):

        archetype = "🧠🔒 Dominador Controlador"

    elif (

        "Verticalidad" in top_metrics

        and

        "Agresividad" in top_metrics

    ):

        archetype = "⚡💣 Transición Vertical"

    elif (

        "Presion" in top_metrics

        and

        "Solidez" in top_metrics

    ):

        archetype = "🔥🛡️ Muralla Presionante"

    elif (

        "Dominio" in top_metrics

        and

        "Verticalidad" in top_metrics

    ):

        archetype = "🚀 Dominio Vertical"

    elif (

        "Agresividad" in top_metrics

        and

        "Efectividad" in top_metrics

    ):

        archetype = "💣🎯 Ataque Élite"

    elif (

        "Efectividad" in top_metrics

        and

        "Eficiencia" in top_metrics

    ):

        archetype = "🎯🏆 Competidor Clínico"

    elif (

        "Solidez" in top_metrics

        and

        "Eficiencia" in top_metrics

    ):

        archetype = "🛡️🏆 Equipo Competitivo"

    else:

        archetype = f"⚽ Perfil {top_metrics[0]}"

    insight_dict = {

        "Dominio": "Control del juego",

        "Verticalidad": "Progresión vertical",

        "Presion": "Presión tras pérdida",

        "Solidez": "Seguridad defensiva",

        "Agresividad": "Volumen ofensivo",

        "Efectividad": "Finalización",

        "Eficiencia": "Rendimiento global"

    }

    st.markdown(

        f"""

<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(135deg,#0f172a,#1e293b);
border:1px solid rgba(255,255,255,0.08);
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

    st.write("")

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 1.2, 1.2])

    cards = [

        insight_dict[top_metrics[0]],

        insight_dict[top_metrics[1]],

        insight_dict[top_metrics[2]]

    ]

    for col, text in zip(

        [c1, c2, c3],

        cards

    ):

        with col:

            st.markdown(

                f"""

<div style="
height:140px;
padding:20px;
background:linear-gradient(135deg,#071329,#1e293b);
border-radius:18px;
border:1px solid rgba(255,255,255,0.08);
display:flex;
align-items:center;
justify-content:center;
text-align:center;
font-size:18px;
font-weight:700;
color:white;
">

{text}

</div>

""",

                unsafe_allow_html=True

            )

    with c4:

        st.metric(

            "Nivel",

            tactical_level.replace(

                "⭐",

                ""

            ).strip()

        )

    with c5:

        st.metric(

            "Tactical Score",

            f"{tactical_score:.1f}"

        )

    st.divider()

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    c1, c2 = st.columns([4, 1.4])

    with c1:

        st.subheader("📋 Resumen Ejecutivo")

        st.write(

            f"**{team}** presenta un perfil táctico marcado principalmente por "

            f"**{top_metrics[0].lower()}**, "

            f"**{top_metrics[1].lower()}** y "

            f"**{top_metrics[2].lower()}**."

        )

        st.info(

            f"Tactical Score: **{tactical_score:.1f}/100** · "

            f"Nivel: **{tactical_level.replace('⭐','').strip()}**"

        )

    with c2:

        st.subheader("🏷️ Identidad")

        st.metric(

            "Arquetipo",

            archetype.split(

                " ",

                1

            )[1] if " " in archetype else archetype

        )

    st.divider()