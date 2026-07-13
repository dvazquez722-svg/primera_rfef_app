import streamlit as st


# =====================================================
# COMPARISON HEADER
# =====================================================

def show_comparison_header(

    team_a,
    team_b,
    teamA_tactical,
    teamB_tactical

):

    metrics = [

        "Dominio",
        "Verticalidad",
        "Presion",
        "Solidez",
        "Agresividad",
        "Efectividad",
        "Eficiencia"

    ]

    score_a = round(teamA_tactical[metrics].mean(), 1)
    score_b = round(teamB_tactical[metrics].mean(), 1)

    diff = round(abs(score_a - score_b), 1)

    if score_a > score_b:
        favourite = team_a
    elif score_b > score_a:
        favourite = team_b
    else:
        favourite = "Igualados"

    # =====================================================
    # ARQUETIPO
    # =====================================================

    def get_archetype(row):

        top3 = (

            row[metrics]

            .sort_values(ascending=False)

            .head(3)

            .index

            .tolist()

        )

        if "Dominio" in top3 and "Solidez" in top3:
            return "🧠 Dominador Controlador"

        if "Verticalidad" in top3 and "Agresividad" in top3:
            return "⚡ Transición Vertical"

        if "Presion" in top3 and "Solidez" in top3:
            return "🔥 Muralla Presionante"

        if "Dominio" in top3 and "Verticalidad" in top3:
            return "🚀 Dominio Vertical"

        if "Agresividad" in top3 and "Efectividad" in top3:
            return "💣 Ataque Élite"

        if "Efectividad" in top3 and "Eficiencia" in top3:
            return "🎯 Competidor Clínico"

        if "Solidez" in top3 and "Eficiencia" in top3:
            return "🛡️ Equipo Competitivo"

        return "⚽ Perfil Mixto"

    archetype_a = get_archetype(teamA_tactical)
    archetype_b = get_archetype(teamB_tactical)

    # =====================================================
    # HERO
    # =====================================================

    st.markdown(

        f"""

<div style="
padding:20px;
border-radius:18px;
background:linear-gradient(135deg,#071329,#1e293b);
border:1px solid rgba(255,255,255,0.08);
">

<h1 style="
margin:0;
text-align:center;
font-size:42px;
font-weight:800;
color:white;
">

⚔️ {team_a} vs {team_b}

</h1>

<div style="
margin-top:6px;
margin-bottom:20px;
text-align:center;
font-size:22px;
font-weight:700;
color:#38bdf8;
">

Comparación táctica

</div>

<div style="
display:grid;
grid-template-columns:1fr 1fr;
gap:16px;
">

<div style="
padding:14px;
background:rgba(255,255,255,.04);
border-radius:14px;
text-align:center;
">

<div style="
font-size:22px;
font-weight:700;
color:white;
">

{team_a}

</div>

<div style="
margin-top:8px;
font-size:18px;
font-weight:700;
color:#38bdf8;
">

{archetype_a}

</div>

<div style="
margin-top:10px;
font-size:14px;
color:#cbd5e1;
">

Tactical Score

</div>

<div style="
font-size:34px;
font-weight:800;
color:white;
">

{score_a}

</div>

</div>

<div style="
padding:14px;
background:rgba(255,255,255,.04);
border-radius:14px;
text-align:center;
">

<div style="
font-size:22px;
font-weight:700;
color:white;
">

{team_b}

</div>

<div style="
margin-top:8px;
font-size:18px;
font-weight:700;
color:#38bdf8;
">

{archetype_b}

</div>

<div style="
margin-top:10px;
font-size:14px;
color:#cbd5e1;
">

Tactical Score

</div>

<div style="
font-size:34px;
font-weight:800;
color:white;
">

{score_b}

</div>

</div>

</div>

</div>

""",

        unsafe_allow_html=True

    )

    st.write()

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Diferencia de Tactical Score",

            f"{diff:.1f}"

        )

    with c2:

        st.metric(

            "Equipo con ventaja",

            favourite

        )

    st.caption(

        "El Tactical Score representa la media de las siete dimensiones tácticas del modelo de juego (escala 0-100)."

    )

    st.divider()