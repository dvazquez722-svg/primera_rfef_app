import streamlit as st

from services.data_reports import (

    add_note,

    update_note,

    get_note_by_chart

)


# =====================================================
# ANALYSIS COMMENT
# =====================================================

def show_analysis_comment(

    team,

    module,

    section,

    chart,

    variables

):

    existing_note = get_note_by_chart(

        team,

        module,

        section,

        chart

    )

    editing_key = (

        f"editing_{module}_{section}_{chart}"

    )

    if editing_key not in st.session_state:

        st.session_state[editing_key] = False

    editing = st.session_state[editing_key]

    # =====================================================
    # COMMENT ALREADY EXISTS
    # =====================================================

    if existing_note and not editing:

        st.success(

            "✅ Comentario guardado"

        )

        if st.button(

            "✏ Editar comentario",

            key=f"edit_{module}_{section}_{chart}",

            use_container_width=True

        ):

            st.session_state[editing_key] = True

            st.rerun()

        return

    # =====================================================
    # COMMENT FORM
    # =====================================================

    with st.expander(

        "💬 Comentar visualización",

        expanded=editing

    ):
        
        note_types = [

            "Fortaleza",

            "Debilidad",

            "Idea táctica",

            "Dato relevante",

            "Observación"

        ]

        default_type = (

            existing_note["type"]

            if existing_note

            else "Observación"

        )

        default_text = (

            existing_note["text"]

            if existing_note

            else ""

        )

        note_type = st.selectbox(

            "Tipo de comentario",

            note_types,

            index=note_types.index(default_type),

            key=f"type_{module}_{section}_{chart}"

        )

        st.markdown(

            f"**📊 Gráfico:** {chart}"

        )

        if isinstance(

            variables,

            list

        ):

            variables_text = " · ".join(

                variables

            )

        else:

            variables_text = variables

        st.markdown(

            f"**📈 Variables analizadas:** {variables_text}"

        )

        text = st.text_area(

            "Comentario",

            value=default_text,

            height=140,

            placeholder="Escribe aquí tu análisis...",

            key=f"text_{module}_{section}_{chart}"

        )

        st.divider()

        if st.button(

            "📝 Guardar comentario",

            key=f"save_{module}_{section}_{chart}",

            use_container_width=True

        ):

            if not text.strip():

                st.warning(

                    "Escribe un comentario antes de guardarlo."

                )

            else:

                if existing_note:

                    update_note(

                        team,

                        existing_note["id"],

                        type=note_type,

                        text=text,

                        chart=chart,

                        variables=variables

                    )

                    st.toast(

                        "✅ Comentario actualizado"

                    )

                else:

                    add_note(

                        team=team,

                        module=module,

                        section=section,

                        note_type=note_type,

                        text=text,

                        chart=chart,

                        variables=variables

                    )

                    st.toast(

                        "✅ Comentario guardado"

                    )

                st.session_state[editing_key] = False

                st.rerun()

                if existing_note:

                    st.caption(

                    f"Última actualización: {existing_note['date'][:16]}"

            )