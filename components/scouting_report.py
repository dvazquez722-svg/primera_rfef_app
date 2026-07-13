import streamlit as st

from services.data_reports import (

    get_notes,

    report_statistics

)


# =====================================================
# SCOUTING REPORT
# =====================================================

def show_report(

    team

):

    st.subheader("📄 Borrador del Informe")

    notes = get_notes(team)

    stats = report_statistics(team)

    # =====================================================
    # ESTADO DEL INFORME
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Notas",

            stats["total_notes"]

        )

    with c2:

        st.metric(

            "Fortalezas",

            stats["Fortaleza"]

        )

    with c3:

        st.metric(

            "Debilidades",

            stats["Debilidad"]

        )

    with c4:

        st.metric(

            "Ideas",

            stats["Idea táctica"]

        )

    st.divider()

    # =====================================================
    # SIN NOTAS
    # =====================================================

    if not notes:

        st.info(

            "Todavía no se ha añadido ningún comentario al informe."

        )

        st.button(

            "📄 Generar informe",

            disabled=True,

            use_container_width=True

        )

        return

    # =====================================================
    # COMENTARIOS
    # =====================================================

    icons = {

        "Fortaleza": "🟢",

        "Debilidad": "🔴",

        "Idea táctica": "💡",

        "Dato relevante": "📊",

        "Observación": "📝"

    }

    current_chart = None

    for note in notes:

        chart = note.get(

            "chart",

            "General"

        )

        if chart != current_chart:

            current_chart = chart

            st.markdown(

                f"### {chart}"

            )

        icon = icons.get(

            note["type"],

            "📝"

        )

        with st.container(

            border=True

        ):

            st.markdown(

                f"**{icon} {note['type']}**"

            )

            if "variables" in note:

                variables = note["variables"]

                if isinstance(

                    variables,

                    list

                ):

                    variables = ", ".join(

                        variables

                    )

                st.caption(

                    f"Variables: {variables}"

                )

            st.write(

                note["text"]

            )

            st.caption(

                note["date"][:16]

            )

    st.divider()

    # =====================================================
    # GENERAR INFORME
    # =====================================================

    st.button(

        "📄 Generar informe",

        use_container_width=True,

        type="primary"

    )