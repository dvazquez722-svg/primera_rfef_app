import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# INTENSITY DIMENSION
# =====================================================

INTENSITY_VARIABLES = [

    "high_speed_distance",

    "high_speed_distance_per_min",

    "high_speed_actions",

    "sprint_distance",

    "sprint_distance_per_min",

    "sprint_count",

    "sprints_per_min",

    "accelerations",

    "accelerations_per_min",

    "decelerations",

    "decelerations_per_min",

    "max_speed",

    "hmld",

    "metabolic_power"

]

INTENSITY_TREND_VARIABLES = [

    "high_speed_distance_acute",

    "high_speed_distance_chronic",

    "high_speed_distance_ewma_7",

    "high_speed_distance_ewma_28",

    "high_speed_distance_acwr",

    "sprint_distance_acute",

    "sprint_distance_chronic",

    "sprint_distance_ewma_7",

    "sprint_distance_ewma_28",

    "sprint_distance_acwr"

]

INTENSITY_COMPARISON_VARIABLES = [

    "high_speed_distance_percentile",

    "high_speed_distance_ranking",

    "high_speed_distance_zscore",

    "sprint_distance_percentile",

    "sprint_distance_ranking",

    "sprint_distance_zscore",

    "max_speed_percentile",

    "max_speed_ranking",

    "max_speed_zscore"

]

# =====================================================
# VARIABLES
# =====================================================

def build_variables(

    dimension,

    row

):

    for variable in INTENSITY_VARIABLES:

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
# TREND
# =====================================================

def build_trend(

    dimension,

    row

):

    for variable in INTENSITY_TREND_VARIABLES:

        value = row.get(

            variable,

            None

        )

        dimension.add_evidence(

            variable,

            value

        )


# =====================================================
# COMPARISONS
# =====================================================

def build_comparisons(

    dimension,

    row

):

    for variable in INTENSITY_COMPARISON_VARIABLES:

        value = row.get(

            variable,

            None

        )

        dimension.add_comparison(

            variable,

            value

        )

# =====================================================
# CONFIDENCE
# =====================================================

def build_confidence(

    dimension,

    row

):

    required = [

        "high_speed_distance",

        "sprint_distance",

        "max_speed",

        "high_speed_distance_acwr",

        "high_speed_distance_percentile",

        "max_speed_percentile"

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

            "La intensidad alcanzada por el jugador "

            "ha sido muy elevada respecto a su perfil "

            "habitual."

        )

    elif score >= 70:

        text = (

            "La intensidad de la sesión ha sido alta "

            "y compatible con una exposición adecuada "

            "a acciones de alta velocidad."

        )

    elif score >= 50:

        text = (

            "La intensidad registrada se encuentra "

            "dentro de los valores esperados."

        )

    elif score >= 30:

        text = (

            "La intensidad ha sido inferior a la "

            "habitual del jugador."

        )

    else:

        text = (

            "La exposición a acciones de alta "

            "intensidad ha sido muy reducida."

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

            "Controlar la recuperación en las próximas "

            "24-48 horas y monitorizar la respuesta "

            "del jugador."

        )

    elif score >= 70:

        recommendation = (

            "Mantener la planificación prevista. "

            "La exposición a alta intensidad ha sido "

            "adecuada."

        )

    elif score >= 50:

        recommendation = (

            "No se requieren modificaciones. "

            "La intensidad se mantiene dentro "

            "del rango esperado."

        )

    elif score >= 30:

        recommendation = (

            "Valorar incluir tareas que aumenten la "

            "exposición a acciones de alta velocidad "

            "en próximas sesiones."

        )

    else:

        recommendation = (

            "La intensidad ha sido muy baja. "

            "Revisar si la sesión correspondía a una "

            "estrategia de recuperación o si conviene "

            "incrementar la exposición progresivamente."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_intensity_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Intensidad",

        description=(

            "Análisis de la intensidad del esfuerzo "

            "realizado por el jugador."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_trend(

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
# SCORE
# =====================================================

def build_score(

    dimension,

    row

):

    score = 50

    hsr_percentile = row.get(

        "high_speed_distance_percentile",

        None

    )

    sprint_percentile = row.get(

        "sprint_distance_percentile",

        None

    )

    max_speed_percentile = row.get(

        "max_speed_percentile",

        None

    )

    acwr = row.get(

        "high_speed_distance_acwr",

        None

    )

    if hsr_percentile is not None:

        if not pd.isna(

            hsr_percentile

        ):

            score += (

                hsr_percentile

                - 50

            ) * 0.25

    if sprint_percentile is not None:

        if not pd.isna(

            sprint_percentile

        ):

            score += (

                sprint_percentile

                - 50

            ) * 0.25

    if max_speed_percentile is not None:

        if not pd.isna(

            max_speed_percentile

        ):

            score += (

                max_speed_percentile

                - 50

            ) * 0.20

    if acwr is not None:

        if not pd.isna(

            acwr

        ):

            if 0.8 <= acwr <= 1.3:

                score += 15

            elif 1.3 < acwr <= 1.5:

                score += 5

            elif acwr > 1.5:

                score -= 15

            elif acwr < 0.8:

                score -= 10

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

# =====================================================
# BUILD INTENSITY DIMENSION
# =====================================================

def build_intensity_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Intensidad",

        description=(

            "Análisis de la intensidad "

            "del esfuerzo realizado por "

            "el jugador."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_trend(

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