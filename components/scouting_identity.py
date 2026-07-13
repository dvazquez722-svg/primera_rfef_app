import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)


# =====================================================
# SCOUTING IDENTITY
# =====================================================

def show_identity(

    team,

    team_tactical

):

    st.subheader("⚔️ Perfil de Juego")

    dom = team_tactical["Dominio"]
    vert = team_tactical["Verticalidad"]
    pre = team_tactical["Presion"]
    sol = team_tactical["Solidez"]
    agr = team_tactical["Agresividad"]

    # =====================================================
    # PERFIL
    # =====================================================

    if dom >= 70:
        construccion = "Elaborada"
    elif dom >= 50:
        construccion = "Mixta"
    else:
        construccion = "Directa"

    if vert >= 70:
        progresion = "Vertical"
    elif vert >= 50:
        progresion = "Mixta"
    else:
        progresion = "Asociativa"

    if pre >= 70:
        defensa = "Presión Alta"
    elif pre >= 50:
        defensa = "Presión Media"
    else:
        defensa = "Bloque Bajo"

    if agr >= 70:
        ataque = "Transiciones"
    elif dom >= 70:
        ataque = "Posicional"
    else:
        ataque = "Mixto"

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Construcción",

            construccion

        )

    with c2:

        st.metric(

            "Progresión",

            progresion

        )

    with c3:

        st.metric(

            "Defensa",

            defensa

        )

    with c4:

        st.metric(

            "Ataque",

            ataque

        )

    st.write("")

    st.markdown("#### 🧭 Identidad del Equipo")

    identity = [

        ("🧠 Control del juego", dom),

        ("⬆️ Verticalidad", vert),

        ("🔥 Presión", pre),

        ("🛡️ Solidez", sol),

        ("⚔️ Agresividad", agr)

    ]

    for title, value in identity:

        c1, c2 = st.columns([3, 7])

        with c1:

            st.write(title)

        with c2:

            st.progress(value / 100)

            st.caption(f"{value:.1f}/100")

    st.divider()

    show_analysis_comment(

        team=team,

        module="Scouting",

        section="Perfil de Juego",

        chart="Perfil de Juego",

        variables=[

            "Dominio",

            "Verticalidad",

            "Presion",

            "Solidez",

            "Agresividad"

        ]

    )