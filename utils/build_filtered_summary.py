import pandas as pd


# =====================================================
# BUILD FILTERED SUMMARY
# =====================================================

def build_filtered_summary(team_matches):

    """
    Genera un resumen dinámico de un equipo a partir de los
    partidos actualmente filtrados.
    """

    numeric = (

        team_matches

        .select_dtypes(include="number")

    )

    summary = numeric.mean()

    return summary