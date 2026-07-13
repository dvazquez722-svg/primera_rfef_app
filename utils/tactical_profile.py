import pandas as pd
import numpy as np

# =====================================================

# LOAD

# =====================================================

def build_tactical_profile(summary, context):

    df = summary.merge(
        context,
        on="Equipo",
        how="left"
        )

# =====================================================

# PERCENTILES

# =====================================================

    def pct(series):
        return series.rank(
            pct=True
    ) * 100


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

    pct(df["Goles_Tiro"]) * 0.20 +

    pct(df["Goles_TiroPuerta"]) * 0.20 +

    pct(df["xG_Tiro"]) * 0.20 +

    pct(
        df["% tiros portería"]
    ) * 0.15 +

    pct(
        df["% ataques posicionales finalizados"]
    ) * 0.10 +

    pct(
        df["% contraataques finalizados"]
    ) * 0.10 +

    pct(
        df["% centros rematados"]
    ) * 0.05

    )

    # =====================================================

    # DOMINIO

    # =====================================================

    df["Dominio"] = (

    pct(df["Posesión del balón, %"]) * 0.20 +

    pct(df["% pases logrados"]) * 0.15 +

    pct(df["Pases progresivos conseguidos"]) * 0.15 +

    pct(df["Pases en el último tercio logrados"]) * 0.15 +

    pct(df["Ataques posicionales finalizados"]) * 0.15 +

    pct(df["xG"]) * 0.15 +

    pct(df["Puntos_Local"]) * 0.05

    )

    # =====================================================

    # VERTICALIDAD

    # =====================================================

    df["Verticalidad"] = (

    pct(df["Contraataques"]) * 0.20 +

    pct(df["Contraataques finalizados"]) * 0.20 +

    pct(df["Pases progresivos conseguidos"]) * 0.15 +

    pct(df["Pases hacia adelante logrados"]) * 0.15 +

    pct(df["Intensidad de paso"]) * 0.15 +

    (
        100 -
        pct(
            df[
                "Promedio pases por posesión del balón"
            ]
        )
    ) * 0.15

    )

    # =====================================================

    # PRESION

    # =====================================================

    df["Presion"] = (

    (
        100 -
        pct(df["PPDA"])
    ) * 0.30 +

    pct(
        df[
            "Balones recuperados último tercio"
        ]
    ) * 0.20 +

    pct(
        df["Interceptaciones"]
    ) * 0.15 +

    pct(
        df[
            "% duelos defensivos ganados"
        ]
    ) * 0.15 +

    pct(
        df[
            "Entradas a ras de suelo exitosas"
        ]
    ) * 0.10 +

    pct(
        df[
            "Duelos defensivos ganados"
        ]
    ) * 0.10

    )

    # =====================================================

    # SOLIDEZ

    # =====================================================

    df["Solidez"] = (

    (
        100 -
        pct(df["Goles recibidos"])
    ) * 0.25 +

    (
        100 -
        pct(df["Tiros en contra"])
    ) * 0.20 +

    (
        100 -
        pct(
            df[
                "% tiros en contra a portería"
            ]
        )
    ) * 0.15 +

    pct(
        df[
            "% duelos defensivos ganados"
        ]
    ) * 0.15 +

    pct(
        df["Interceptaciones"]
    ) * 0.10 +

    pct(
        df["Despejes"]
    ) * 0.05 +

    (
        100 -
        pct(df["GC_Local"])
    ) * 0.10

    )

    # =====================================================

    # AGRESIVIDAD

    # =====================================================

    df["Agresividad"] = (

    pct(df["xG"]) * 0.20 +

    pct(df["Tiros totales"]) * 0.15 +

    pct(
        df[
            "Ataques posicionales finalizados"
        ]
    ) * 0.15 +

    pct(
        df[
            "Contraataques finalizados"
        ]
    ) * 0.15 +

    pct(
        df[
            "Duelos ofensivos ganados"
        ]
    ) * 0.15 +

    pct(
        df[
            "Centros rematados"
        ]
    ) * 0.10 +

    pct(
        df[
            "Pases progresivos conseguidos"
        ]
    ) * 0.10

    )

    # =====================================================

    # EFICIENCIA

    # =====================================================

    df["Conversion_xG"] = (
    df["Goles"]
    /
    df["xG"].replace(0, np.nan)
    )

    df["Eficiencia"] = (

    pct(
        df["Conversion_xG"]
    ) * 0.35 +

    pct(
        df["Puntos_Local"]
    ) * 0.20 +

    pct(
        df["Puntos_Visitante"]
    ) * 0.20 +

    pct(
        df["GF_Victoria"]
    ) * 0.15 +

    (
        100 -
        pct(
            df["GC_Victoria"]
        )
    ) * 0.10

    )

    # =====================================================

    # ROUND

    # =====================================================

    indices = [
    "Dominio",
    "Verticalidad",
    "Presion",
    "Solidez",
    "Agresividad",
    "Efectividad",
    "Eficiencia"
    ]

    df[indices] = (
    df[indices]
    .round(1)
    )

    tactical = df[
    ["Equipo"] + indices
    ]

    return tactical
