import pandas as pd


# =====================================================
# BUILD TEAM SUMMARY
# =====================================================

def build_team_summary(team_matches):

    """
    Genera un resumen estadístico de un equipo a partir de
    un conjunto de partidos (temporada completa o filtrada).

    Devuelve una Serie de pandas con exactamente las mismas
    métricas que team_summary.csv.
    """

    # ==========================================
    # COLUMNAS NUMÉRICAS
    # ==========================================

    numeric_columns = (

        team_matches

        .select_dtypes(include="number")

        .columns

    )

    # ==========================================
    # MEDIA DE TODAS LAS VARIABLES
    # ==========================================

    summary = (

        team_matches[numeric_columns]

        .mean()

        .round(2)

    )

    return summary