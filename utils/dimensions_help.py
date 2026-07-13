import streamlit as st


# =====================================================
# DIMENSIONS HELP
# =====================================================

@st.dialog("📚 Metodología de las Dimensiones Tácticas", width="large")
def show_dimensions_help():

    st.markdown("""
Las dimensiones tácticas representan una síntesis del comportamiento del equipo.

Cada una de ellas se calcula a partir de un conjunto de variables normalizadas respecto al resto de equipos de la competición. El objetivo es facilitar la interpretación táctica sin depender de una única estadística.
""")

    st.divider()

    dimensions = [

        {
            "title":"🧠 Dominio",
            "variables":[
                "Posesión",
                "Pases",
                "Precisión de pase",
                "xG",
                "Territorio"
            ],
            "meaning":"Mide la capacidad del equipo para controlar el desarrollo del juego e imponer su modelo de partido."
        },

        {
            "title":"⬆️ Verticalidad",
            "variables":[
                "Pases progresivos",
                "Ataques rápidos",
                "Progresión",
                "Transiciones"
            ],
            "meaning":"Evalúa la velocidad e intención del equipo para progresar hacia la portería rival."
        },

        {
            "title":"🔥 Presión",
            "variables":[
                "PPDA",
                "Recuperaciones en campo rival",
                "Acciones defensivas altas"
            ],
            "meaning":"Representa la intensidad con la que el equipo intenta recuperar el balón tras pérdida."
        },

        {
            "title":"🛡️ Solidez",
            "variables":[
                "xGA",
                "Goles recibidos",
                "Tiros recibidos",
                "Ocasiones concedidas"
            ],
            "meaning":"Evalúa la capacidad para minimizar las ocasiones del rival."
        },

        {
            "title":"⚔️ Agresividad",
            "variables":[
                "Duelos",
                "Entradas",
                "Intercepciones",
                "Recuperaciones"
            ],
            "meaning":"Describe el comportamiento defensivo activo del equipo."
        },

        {
            "title":"🎯 Efectividad",
            "variables":[
                "Goles",
                "Conversión",
                "xG"
            ],
            "meaning":"Mide la capacidad para transformar ocasiones en goles."
        },

        {
            "title":"📈 Eficiencia",
            "variables":[
                "xG",
                "Posesión",
                "PPDA",
                "Goles",
                "Recuperaciones"
            ],
            "meaning":"Representa el rendimiento global del equipo teniendo en cuenta recursos ofensivos y defensivos."
        }

    ]

    for dimension in dimensions:

        with st.container(border=True):

            st.subheader(dimension["title"])

            st.markdown("**Variables utilizadas**")

            for variable in dimension["variables"]:

                st.write(f"• {variable}")

            st.markdown("**Interpretación**")

            st.info(dimension["meaning"])

    st.divider()

    st.caption(
        "Las dimensiones se calculan a partir de variables normalizadas respecto al resto de equipos de la competición. "
        "La metodología podrá evolucionar conforme se incorporen nuevas métricas al modelo."
    )

