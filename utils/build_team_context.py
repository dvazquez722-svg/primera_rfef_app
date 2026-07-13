import pandas as pd


# =====================================================
# BUILD TEAM CONTEXT
# =====================================================

def build_team_context(team_matches):

    """
    Genera el contexto competitivo del equipo
    utilizando únicamente los partidos recibidos.

    Devuelve una Serie equivalente a una fila de
    team_context_summary.csv.
    """

    # =====================================================
    # VARIABLES
    # =====================================================

    metrics = [

        # RESULTADO

        "xG",
        "GF",
        "GC",
        "Puntos",

        # POSESIÓN

        "Posesión del balón, %",
        "Promedio pases por posesión del balón",

        # CONSTRUCCIÓN

        "Longitud media pases",
        "Lanzamiento largo %",
        "Pases progresivos conseguidos",
        "Pases en el último tercio logrados",
        "% pases",

        # ATAQUE

        "Tiros totales",
        "Tiros a portería",
        "Ataques posicionales finalizados",
        "Contraataques finalizados",
        "Centros lanzados",
        "% centros rematados",

        # DEFENSA

        "PPDA",
        "Tiros en contra",
        "Tiros en contra a portería",
        "Balones recuperados último tercio",
        "Balones recuperados inicio",
        "Balones recuperados medio",

        # DUELOS

        "% duelos aéreos ganados",
        "% duelos defensivos ganados",

        # PÉRDIDAS

        "Balones perdidos inicio",
        "Balones perdidos medio",
        "Balones perdidos último tercio"

    ]

    # =====================================================
    # SOLO COLUMNAS EXISTENTES
    # =====================================================

    metrics = [

        c

        for c in metrics

        if c in team_matches.columns

    ]

    context = {}

    # =====================================================
    # VICTORIAS
    # =====================================================

    victories = team_matches[
        team_matches["Resultado"] == "Victoria"
    ]

    for metric in metrics:

        context[f"{metric}_Victoria"] = round(

            victories[metric].mean(),

            2

        )

    # =====================================================
    # EMPATES
    # =====================================================

    draws = team_matches[
        team_matches["Resultado"] == "Empate"
    ]

    for metric in metrics:

        context[f"{metric}_Empate"] = round(

            draws[metric].mean(),

            2

        )

    # =====================================================
    # DERROTAS
    # =====================================================

    losses = team_matches[
        team_matches["Resultado"] == "Derrota"
    ]

    for metric in metrics:

        context[f"{metric}_Derrota"] = round(

            losses[metric].mean(),

            2

        )

    # =====================================================
    # LOCAL
    # =====================================================

    home = team_matches[
        team_matches["Condicion"] == "Local"
    ]

    for metric in metrics:

        context[f"{metric}_Local"] = round(

            home[metric].mean(),

            2

        )

    # =====================================================
    # VISITANTE
    # =====================================================

    away = team_matches[
        team_matches["Condicion"] == "Visitante"
    ]

    for metric in metrics:

        context[f"{metric}_Visitante"] = round(

            away[metric].mean(),

            2

        )

    return pd.Series(context)