import streamlit as st


# =====================================================
# REPORT HEADER
# =====================================================

def show_report_header(

    team,

    team_summary,

    team_tactical,

    matches

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

    tactical_score = round(

        team_tactical[metrics].mean(),

        1

    )

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

    defeats = (

        matches["Goles"]

        <

        matches["Goles recibidos"]

    ).sum()

    games = len(matches)

    win_pct = (

        victories / games * 100

        if games > 0

        else 0

    )

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

    archetype = get_archetype(

        team_tactical

    )

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

🎯 Informe Automático

</h1>

<div style="
margin-top:8px;
text-align:center;
font-size:28px;
font-weight:700;
color:white;
">

{team}

</div>

<div style="
margin-top:8px;
margin-bottom:18px;
text-align:center;
font-size:20px;
font-weight:700;
color:#38bdf8;
">

{archetype}

</div>

</div>

""",

        unsafe_allow_html=True

    )

    st.write("")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(

            "Tactical Score",

            f"{tactical_score:.1f}"

        )

    with c2:

        st.metric(

            "Partidos",

            games

        )

    with c3:

        st.metric(

            "% Victorias",

            f"{win_pct:.0f}%"

        )

    with c4:

        st.metric(

            "GF",

            round(

                team_summary["Goles"],

                2

            )

        )

    with c5:

        st.metric(

            "GC",

            round(

                team_summary["Goles recibidos"],

                2

            )

        )

    st.caption(

        "El Tactical Score representa la media de las siete dimensiones tácticas del modelo de juego (escala 0-100)."

    )

    st.divider()