import pandas as pd


# =====================================================
# BUILD TEAM CONTEXT
# =====================================================

def build_team_context(df):

    """
    Genera el contexto estadístico por equipo
    (victorias, empates, derrotas, local y visitante).

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con un partido por fila.

    Devuelve
    --------
    pandas.DataFrame
        Una fila por equipo con todas las métricas de contexto.
    """

    # =====================================================
    # METRICS
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

    # Solo columnas existentes

    metrics = [

        c

        for c in metrics

        if c in df.columns

    ]

    # =====================================================
    # RESULTADOS
    # =====================================================

    victories = (

        df[df["Resultado"] == "Victoria"]

        .groupby("Equipo")[metrics]

        .mean()

        .add_suffix("_Victoria")

    )

    draws = (

        df[df["Resultado"] == "Empate"]

        .groupby("Equipo")[metrics]

        .mean()

        .add_suffix("_Empate")

    )

    losses = (

        df[df["Resultado"] == "Derrota"]

        .groupby("Equipo")[metrics]

        .mean()

        .add_suffix("_Derrota")

    )

    # =====================================================
    # LOCAL / VISITANTE
    # =====================================================

    home = (

        df[df["Condicion"] == "Local"]

        .groupby("Equipo")[metrics]

        .mean()

        .add_suffix("_Local")

    )

    away = (

        df[df["Condicion"] == "Visitante"]

        .groupby("Equipo")[metrics]

        .mean()

        .add_suffix("_Visitante")

    )

    # =====================================================
    # MERGE
    # =====================================================

    context = (

        victories

        .join(draws)

        .join(losses)

        .join(home)

        .join(away)

        .reset_index()

    )

    context = context.round(2)

    return context


# =====================================================
# SCRIPT
# =====================================================

if __name__ == "__main__":

    df = pd.read_csv(

        "data/processed/master_team_stats.csv"

    )

    context = build_team_context(df)

    context.to_csv(

        "data/processed/team_context_summary.csv",

        index=False

    )

    print("\nShape:")

    print(context.shape)

    print("\nEquipos:")

    print(context["Equipo"].nunique())

    print("\nColumnas:")

    print(len(context.columns))

    print("\nPreview:")

    print(context.head())

    print("\nColumnas disponibles:")

    print(context.columns.tolist())