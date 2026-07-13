import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# TREND DIMENSION
# =====================================================

TREND_VARIABLES = [

    "distance_m_acute",

    "distance_m_chronic",

    "distance_m_ewma_7",

    "distance_m_ewma_28",

    "distance_m_acwr",

    "player_load_acute",

    "player_load_chronic",

    "player_load_ewma_7",

    "player_load_ewma_28",

    "player_load_acwr",

    "high_speed_distance_acute",

    "high_speed_distance_chronic",

    "high_speed_distance_ewma_7",

    "high_speed_distance_ewma_28",

    "high_speed_distance_acwr"

]

TREND_COMPARISON_VARIABLES = [

    "distance_m_zscore",

    "player_load_zscore",

    "high_speed_distance_zscore",

    "distance_m_percentile",

    "player_load_percentile",

    "high_speed_distance_percentile"

]

# =====================================================
# CONFIDENCE
# =====================================================

def build_confidence(

    dimension,

    row

):

    required = [

        "distance_m_acwr",

        "player_load_acwr",

        "high_speed_distance_acwr",

        "distance_m_ewma_7",

        "player_load_ewma_7",

        "high_speed_distance_ewma_7"

    ]

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

            "La evolución de la carga es muy "

            "estable y compatible con una "

            "progresión adecuada del entrenamiento."

        )

    elif score >= 70:

        text = (

            "La tendencia reciente es favorable, "

            "sin cambios bruscos en la carga."

        )

    elif score >= 50:

        text = (

            "La evolución de la carga permanece "

            "dentro de los rangos esperados."

        )

    elif score >= 30:

        text = (

            "Se observan variaciones relevantes "

            "respecto a las semanas anteriores."

        )

    else:

        text = (

            "La evolución reciente muestra "

            "cambios importantes que requieren "

            "seguimiento."

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

            "Mantener la progresión actual de la "

            "carga y continuar monitorizando las "

            "tendencias."

        )

    elif score >= 70:

        recommendation = (

            "La evolución es adecuada. Mantener "

            "la planificación prevista."

        )

    elif score >= 50:

        recommendation = (

            "Continuar monitorizando la evolución "

            "sin necesidad de realizar cambios "

            "importantes."

        )

    elif score >= 30:

        recommendation = (

            "Revisar las cargas de las últimas "

            "sesiones para evitar cambios "

            "excesivamente rápidos."

        )

    else:

        recommendation = (

            "Analizar la planificación reciente. "

            "Se recomienda revisar la progresión "

            "de carga antes de aumentar la exigencia."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_trend_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Tendencia",

        description=(

            "Análisis de la evolución temporal "

            "de la carga y de la intensidad "

            "del jugador."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_comparisons(

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
# BUILD TREND DIMENSION
# =====================================================

def build_trend_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Tendencia",

        description=(

            "Análisis de la evolución de la "

            "carga del jugador en el tiempo."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_comparisons(

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

    for variable in TREND_VARIABLES:

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
# COMPARISONS
# =====================================================

def build_comparisons(

    dimension,

    row

):

    for variable in TREND_COMPARISON_VARIABLES:

        value = row.get(

            variable,

            None

        )

        dimension.add_comparison(

            variable,

            value

        )


# =====================================================
# SCORE
# =====================================================

def build_score(

    dimension,

    row

):

    score = 50

    acwr_variables = [

        "distance_m_acwr",

        "player_load_acwr",

        "high_speed_distance_acwr"

    ]

    for variable in acwr_variables:

        value = row.get(

            variable,

            None

        )

        if value is None or pd.isna(value):

            continue

        if 0.8 <= value <= 1.3:

            score += 10

        elif 1.3 < value <= 1.5:

            score += 5

        elif value > 1.5:

            score -= 10

        else:

            score -= 5

    score = max(

        0,

        min(

            100,

            round(

                score,

                1

            )

        )

    )

    dimension.set_score(

        score

    )