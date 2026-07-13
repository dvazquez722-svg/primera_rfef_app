import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# COMPARISON DIMENSION
# =====================================================

COMPARISON_VARIABLES = [

    "distance_m_percentile",

    "player_load_percentile",

    "high_speed_distance_percentile",

    "sprint_distance_percentile",

    "max_speed_percentile",

    "rpe_general_percentile",

    "wellness_sleep_percentile",

    "wellness_fatigue_percentile",

    "wellness_doms_percentile",

    "wellness_stress_percentile",

    "wellness_mood_percentile"

]

COMPARISON_RANKINGS = [

    "distance_m_ranking",

    "player_load_ranking",

    "high_speed_distance_ranking",

    "sprint_distance_ranking",

    "max_speed_ranking"

]

COMPARISON_ZSCORES = [

    "distance_m_zscore",

    "player_load_zscore",

    "high_speed_distance_zscore",

    "sprint_distance_zscore",

    "max_speed_zscore"

]

# =====================================================
# CONFIDENCE
# =====================================================

def build_confidence(

    dimension,

    row

):

    required = (

        COMPARISON_VARIABLES

        +

        COMPARISON_RANKINGS

        +

        COMPARISON_ZSCORES

    )

    available = 0

    for variable in required:

        value = row.get(

            variable,

            None

        )

        if value is not None:

            if not pd.isna(

                value

            ):

                available += 1

    ratio = available / len(

        required

    )

    if ratio >= 0.90:

        confidence = "Muy Alta"

    elif ratio >= 0.75:

        confidence = "Alta"

    elif ratio >= 0.50:

        confidence = "Media"

    else:

        confidence = "Baja"

    dimension.set_confidence(

        confidence

    )


# =====================================================
# INTERPRETATION
# =====================================================

def build_interpretation(

    dimension

):

    score = dimension.score

    if score >= 85:

        text = (

            "El jugador se sitúa muy por encima "

            "de la referencia del equipo y de su "

            "posición en la mayoría de indicadores."

        )

    elif score >= 70:

        text = (

            "El rendimiento del jugador se sitúa "

            "por encima de la media del grupo."

        )

    elif score >= 50:

        text = (

            "El jugador presenta valores similares "

            "a los esperados respecto a sus "

            "compañeros."

        )

    elif score >= 30:

        text = (

            "El rendimiento es inferior a la media "

            "del equipo en varias variables."

        )

    else:

        text = (

            "El jugador se encuentra claramente "

            "por debajo de las referencias del "

            "grupo."

        )

    dimension.interpretation = text


# =====================================================
# RECOMMENDATION
# =====================================================

def build_recommendation(

    dimension

):

    score = dimension.score

    if score >= 85:

        recommendation = (

            "Mantener la planificación actual. "

            "El jugador presenta un rendimiento "

            "comparativo excelente."

        )

    elif score >= 70:

        recommendation = (

            "Continuar con la planificación "

            "prevista y mantener la evolución."

        )

    elif score >= 50:

        recommendation = (

            "No se requieren cambios relevantes. "

            "El jugador se mantiene en valores "

            "normales respecto al grupo."

        )

    elif score >= 30:

        recommendation = (

            "Identificar las variables en las que "

            "el jugador se sitúa por debajo del "

            "equipo y diseñar tareas específicas."

        )

    else:

        recommendation = (

            "Realizar una valoración individual "

            "para detectar los factores que "

            "explican el bajo rendimiento "

            "comparativo."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_comparison_dimension(

    player_df,

    team_df

):

    dimension = PerformanceDimension(

        name="Comparación",

        description=(

            "Comparación del jugador respecto "

            "a sus compañeros, su posición y "

            "su referencia histórica."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_rankings(

        dimension,

        latest

    )

    build_zscores(

        dimension,

        latest

    )

    build_score(

        dimension,

        latest

    )

    build_confidence(

        dimension,

        latest

    )

    build_interpretation(

        dimension

    )

    build_recommendation(

        dimension

    )

    return dimension

# =====================================================
# BUILD COMPARISON DIMENSION
# =====================================================

def build_comparison_dimension(

    player_df,

    team_df

):

    dimension = PerformanceDimension(

        name="Comparación",

        description=(

            "Comparación del jugador "

            "respecto al equipo, posición "

            "y referencia histórica."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_rankings(

        dimension,

        latest

    )

    build_zscores(

        dimension,

        latest

    )

    build_score(

        dimension,

        latest

    )

    build_confidence(

        dimension,

        latest

    )

    return dimension


# =====================================================
# VARIABLES
# =====================================================

def build_variables(

    dimension,

    row

):

    for variable in COMPARISON_VARIABLES:

        value = row.get(

            variable,

            None

        )

        performance_variable = PerformanceVariable(

            name=variable,

            value=value

        )

        dimension.add_variable(

            performance_variable

        )


# =====================================================
# RANKINGS
# =====================================================

def build_rankings(

    dimension,

    row

):

    for variable in COMPARISON_RANKINGS:

        dimension.add_evidence(

            variable,

            row.get(

                variable,

                None

            )

        )


# =====================================================
# Z-SCORES
# =====================================================

def build_zscores(

    dimension,

    row

):

    for variable in COMPARISON_ZSCORES:

        dimension.add_comparison(

            variable,

            row.get(

                variable,

                None

            )

        )


# =====================================================
# SCORE
# =====================================================

def build_score(

    dimension,

    row

):

    percentiles = [

        row.get(

            variable,

            None

        )

        for variable in COMPARISON_VARIABLES

    ]

    values = [

        value

        for value in percentiles

        if value is not None

        and

        not pd.isna(

            value

        )

    ]

    if len(values) == 0:

        score = 50

    else:

        score = sum(

            values

        ) / len(

            values

        )

    dimension.set_score(

        round(

            score,

            1

        )

    )