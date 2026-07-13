import streamlit as st

from services.data_reports import (

    add_note,

    get_notes_by_section,

    delete_note,

    update_note,

    report_statistics

)


# =====================================================
# REFLECTION BOX
# =====================================================

def show_reflection_box(

    team,

    module,

    section,

    show_notes=False

):

    if "editing_note" not in st.session_state:

        st.session_state.editing_note = None

    stats = report_statistics(team)

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

    st.markdown(

        "### 📝 Reflexión del analista"

    )

    note_type = st.selectbox(

        "Tipo",

        [

            "Fortaleza",

            "Debilidad",

            "Idea táctica",

            "Dato relevante",

            "Observación"

        ],

        key=f"type_{module}_{section}"

    )

    text = st.text_area(

        "Reflexión",

        height=140,

        key=f"text_{module}_{section}"

    )

    if st.button(

        "💾 Añadir al informe",

        key=f"save_{module}_{section}",

        use_container_width=True

    ):

        if text.strip():

            add_note(

                team,

                module,

                section,

                note_type,

                text

            )

            st.success(

                "Reflexión añadida al informe."

            )

            st.rerun()

            if not show_notes:

                return
            
    # =====================================================
    # SAVED NOTES
    # =====================================================

    notes = get_notes_by_section(

        team,

        module,

        section

    )
    
    grouped_notes = {

        "Fortaleza": [],

        "Debilidad": [],

        "Idea táctica": [],

        "Dato relevante": [],

        "Observación": []

    }

    for note in notes:

        grouped_notes[note["type"]].append(note)

    if not notes:

        return

    st.divider()

    st.markdown(

        "### 📋 Reflexiones guardadas"

    )

    icons = {

        "Fortaleza": "🟢",

        "Debilidad": "🔴",

        "Idea táctica": "💡",

        "Dato relevante": "📊",

        "Observación": "📝"

    }

    for note in reversed(notes):

        icon = icons.get(

            note["type"],

            "📝"

        )
        titles = {

        "Fortaleza": "🟢 FORTALEZAS",

        "Debilidad": "🔴 DEBILIDADES",

        "Idea táctica": "💡 IDEAS TÁCTICAS",

        "Dato relevante": "📊 DATOS RELEVANTES",

        "Observación": "📝 OBSERVACIONES"

    }

    for note_type, note_list in grouped_notes.items():

        if not note_list:

            continue

        st.markdown(

            f"## {titles[note_type]} ({len(note_list)})"

        )

        for note in reversed(note_list):

            icon = icons[note["type"]]

            with st.container(border=True):

                if st.session_state.editing_note == note["id"]:

                    st.markdown(

                    f"### {icon} Editando"

                )

                new_type = st.selectbox(

                    "Tipo",

                    [

                        "Fortaleza",

                        "Debilidad",

                        "Idea táctica",

                        "Dato relevante",

                        "Observación"

                    ],

                    index=[

                        "Fortaleza",

                        "Debilidad",

                        "Idea táctica",

                        "Dato relevante",

                        "Observación"

                    ].index(

                        note["type"]

                    ),

                    key=f"edit_type_{note['id']}"

                )

                new_text = st.text_area(

                    "Texto",

                    value=note["text"],

                    height=120,

                    key=f"edit_text_{note['id']}"

                )
                c1, c2 = st.columns(2)

                with c1:

                    if st.button(

                        "💾 Guardar cambios",

                        key=f"save_edit_{note['id']}",

                        use_container_width=True

                    ):

                        update_note(

                            team,

                            note["id"],

                            type=new_type,

                            text=new_text

                        )

                        st.session_state.editing_note = None

                        st.success(

                            "Reflexión actualizada."

                        )

                        st.rerun()

                with c2:

                    if st.button(

                        "❌ Cancelar",

                        key=f"cancel_edit_{note['id']}",

                        use_container_width=True

                    ):

                        st.session_state.editing_note = None

                        st.rerun()

        else:

                st.markdown(

                    f"### {icon} {note['type']}"

                )

                st.caption(

                    note["date"][:16]

                )

                st.write(

                    note["text"]

                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(

                        "✏ Editar",

                        key=f"edit_{note['id']}",

                        use_container_width=True

                    ):

                        st.session_state.editing_note = note["id"]

                        st.rerun()

                with c2:

                    if st.button(

                        "🗑 Eliminar",

                        key=f"delete_{note['id']}",

                        use_container_width=True

                    ):

                        delete_note(

                            team,

                            note["id"]

                        )

                        if st.session_state.editing_note == note["id"]:

                            st.session_state.editing_note = None

                        st.success(

                            "Reflexión eliminada."

                        )

                        st.rerun()