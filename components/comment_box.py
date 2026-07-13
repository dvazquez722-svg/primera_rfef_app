import streamlit as st

# =====================================================
# COMMENT BOX
# =====================================================

def show_comment_box(
    key: str,
    title: str = "📝 Comentarios del analista"
):
    """
    Caja estándar de comentarios para toda la aplicación.
    """

    st.markdown("### " + title)

    comment = st.text_area(

        label="",

        key=key,

        height=140,

        placeholder="Escribe aquí tus observaciones..."

    )

    return comment