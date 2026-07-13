import pandas as pd


# =====================================================
# BUILD TEAM SUMMARY
# =====================================================

def build_team_summary(df):

    """
    Genera un resumen estadístico por equipo.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame con un partido por fila
        (master_team_stats).

    Devuelve
    --------
    pandas.DataFrame
        Un DataFrame con una fila por equipo y la media
        de todas las variables numéricas.
    """

    numeric_cols = (

        df

        .select_dtypes(include="number")

        .columns

    )

    team_summary = (

        df

        .groupby("Equipo")[numeric_cols]

        .mean()

        .round(2)

        .reset_index()

    )

    return team_summary


# =====================================================
# SCRIPT
# =====================================================

if __name__ == "__main__":

    df = pd.read_csv(

        "data/processed/master_team_stats.csv"

    )

    team_summary = build_team_summary(df)

    team_summary.to_csv(

        "data/processed/team_summary.csv",

        index=False

    )

    print("\nShape:")

    print(team_summary.shape)

    print("\nEquipos:")

    print(team_summary["Equipo"].nunique())

    print("\nGoles recibidos:")

    print(

        team_summary[
            ["Equipo", "Goles recibidos"]
        ]

        .sort_values(

            "Goles recibidos"

        )

        .head(10)

    )

    print("\nxG:")

    print(

        team_summary[
            ["Equipo", "xG"]
        ]

        .sort_values(

            "xG",

            ascending=False

        )

        .head(10)

    )

    print("\nShape original:")

    print(df.shape)

    print("\nDuplicados Equipo-Partido:")

    print(

        df[
            ["Equipo", "Partido"]
        ]

        .duplicated()

        .sum()

    )

    print("\nColumnas:")

    print(team_summary.columns.tolist())