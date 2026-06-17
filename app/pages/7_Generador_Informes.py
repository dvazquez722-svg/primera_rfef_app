import streamlit as st

st.set_page_config(
    page_title="Generador de Informes",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Generador de Informes")

rival = st.selectbox(
    "Rival",
    [
        "Ponferradina",
        "Real Madrid Castilla"
    ]
)

tipo = st.radio(
    "Tipo de informe",
    [
        "Jugadores",
        "Cuerpo Técnico"
    ]
)

st.button(
    "Generar Informe",
    use_container_width=True
)