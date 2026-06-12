import pandas as pd
import numpy as np

# =====================================================
# LOAD
# =====================================================

summary = pd.read_csv(
    "data/processed/team_summary.csv"
)

context = pd.read_csv(
    "data/processed/team_context_summary.csv"
)

df = summary.merge(
    context,
    on="Equipo",
    how="left"
)

# =====================================================
# PERCENTILES
# =====================================================

def pct(series):
    return (
        series.rank(pct=True)
        * 100
    )

import pandas as pd

# =====================================================
# LOAD
# =====================================================

summary = pd.read_csv(
    "data/processed/team_summary.csv"
)

context = pd.read_csv(
    "data/processed/team_context_summary.csv"
)

df = summary.merge(
    context,
    on="Equipo",
    how="left"
)

# =====================================================
# PERCENTILES
# =====================================================

def pct(series):
    return (
        series.rank(pct=True)
        * 100
    )

# =====================================================
# EFECTIVIDAD
# =====================================================

df["Goles_xG"] = (
    df["Goles"]
    /
    df["xG"].replace(0, np.nan)
)

df["Goles_Tiro"] = (
    df["Goles"]
    /
    df["Tiros totales"].replace(0, np.nan)
)

df["Goles_TiroPuerta"] = (
    df["Goles"]
    /
    df["Tiros a portería"].replace(0, np.nan)
)

df["xG_Tiro"] = (
    df["xG"]
    /
    df["Tiros totales"].replace(0, np.nan)
)

df["Efectividad"] = (

    pct(
        df["Goles_Tiro"]
    ) * 0.20 +

    pct(
        df["Goles_TiroPuerta"]
    ) * 0.20 +

    pct(
        df["xG_Tiro"]
    ) * 0.20 +

    pct(
        df[
            "% tiros portería"
        ]
    ) * 0.15 +

    pct(
        df[
            "% ataques posicionales finalizados"
        ]
    ) * 0.10 +

    pct(
        df[
            "% contraataques finalizados"
        ]
    ) * 0.10 +

    pct(
        df[
            "% centros rematados"
        ]
    ) * 0.05

)

# =====================================================
# DOMINIO
# =====================================================

df["Dominio"] = (

    pct(df["Posesión del balón, %"]) * 0.30 +

    pct(df["xG"]) * 0.30 +

    pct(df["Pases progresivos conseguidos"]) * 0.20 +

    pct(df["Ataques posicionales finalizados"]) * 0.10 +

    pct(df["Puntos_Local"]) * 0.10

)

# =====================================================
# VERTICALIDAD
# =====================================================

df["Verticalidad"] = (

    pct(df["Contraataques"]) * 0.30 +

    pct(df["Contraataques finalizados"]) * 0.25 +

    pct(df["Pases progresivos conseguidos"]) * 0.20 +

    (
        100 -
        pct(
            df[
                "Promedio pases por posesión del balón"
            ]
        )
    ) * 0.25

)

# =====================================================
# PRESION
# =====================================================

df["Presion"] = (

    (
        100 -
        pct(df["PPDA"])
    ) * 0.40 +

    pct(
        df[
            "Balones recuperados último tercio"
        ]
    ) * 0.30 +

    pct(
        df["Interceptaciones"]
    ) * 0.15 +

    pct(
        df[
            "% duelos defensivos ganados"
        ]
    ) * 0.15

)

# =====================================================
# SOLIDEZ
# =====================================================

df["Solidez"] = (

    (
        100 -
        pct(df["Goles recibidos"])
    ) * 0.40 +

    (
        100 -
        pct(df["Tiros en contra"])
    ) * 0.30 +

    pct(
        df[
            "% duelos defensivos ganados"
        ]
    ) * 0.15 +

    (
        100 -
        pct(df["GC_Local"])
    ) * 0.15

)

# =====================================================
# AGRESIVIDAD OFENSIVA
# =====================================================

df["Agresividad"] = (

    pct(df["xG"]) * 0.30 +

    pct(df["Tiros totales"]) * 0.25 +

    pct(
        df[
            "Ataques posicionales finalizados"
        ]
    ) * 0.20 +

    pct(
        df[
            "Contraataques finalizados"
        ]
    ) * 0.15 +

    pct(
        df[
            "Pases progresivos conseguidos"
        ]
    ) * 0.10

)

# =====================================================
# EFICIENCIA
# =====================================================

df["Eficiencia"] = (

    pct(df["Goles_xG"]) * 0.40 +

    pct(df["Puntos_Local"]) * 0.20 +

    pct(df["Puntos_Visitante"]) * 0.20 +

    pct(df["GF_Victoria"]) * 0.20

)

# =====================================================
# REDONDEAR
# =====================================================

indices = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Eficiencia",
    "Efectividad"
]

df[indices] = (
    df[indices]
    .round(1)
)

# =====================================================
# SAVE
# =====================================================

tactical = df[
    ["Equipo"] + indices
]

tactical.to_csv(
    "data/processed/team_tactical_profile.csv",
    index=False
)

# =====================================================
# CHECK
# =====================================================

print(
    tactical
    .sort_values(
        "Dominio",
        ascending=False
    )
    .head(10)
)

print(
    tactical
    .sort_values(
        "Solidez",
        ascending=False
    )
    .head(10)
)

# =====================================================
# REDONDEAR
# =====================================================

indices = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Eficiencia"
]

df[indices] = (
    df[indices]
    .round(1)
)

# =====================================================
# SAVE
# =====================================================

tactical = df[
    ["Equipo"] + indices
]

tactical.to_csv(
    "data/processed/team_tactical_profile.csv",
    index=False
)

# =====================================================
# CHECK
# =====================================================

print(
    tactical
    .sort_values(
        "Dominio",
        ascending=False
    )
    .head(10)
)

print(
    tactical
    .sort_values(
        "Solidez",
        ascending=False
    )
    .head(10)
)