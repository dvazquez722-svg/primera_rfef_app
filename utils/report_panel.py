import streamlit as st

from services.data_reports import (

    report_statistics

)


# =====================================================
# REPORT PANEL
# =====================================================

def show_report_panel(

    team

):

    stats = report_statistics(

        team

    )

    with st.container(border=True):

        st.subheader(

            "📄 Informe"

        )

        st.metric(

            "Reflexiones",

            stats["total_notes"]

        )

        st.metric(

            "Fortalezas",

            stats["Fortaleza"]

        )

        st.metric(

            "Debilidades",

            stats["Debilidad"]

        )

        st.metric(

            "Ideas",

            stats["Idea táctica"]

        )

        st.metric(

            "Observaciones",

            stats["Observación"]

        )

        st.metric(

            "Módulos",

            stats["modules"]

        )

        st.metric(

            "Apartados",

            stats["sections"]

        )

        st.divider()

        st.button(

            "📄 Generar informe",

            disabled=True,

            use_container_width=True

        )