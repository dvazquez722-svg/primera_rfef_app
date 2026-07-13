import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# RESPONSE DIMENSION
# =====================================================

RESPONSE_VARIABLES = [

    "rpe_general",

    "rpe_peripheral",

    "wellness_sleep",

    "wellness_fatigue",

    "wellness_doms",

    "wellness_stress",

    "wellness_mood",

    "heart_rate_avg",

    "heart_rate_max",

    "heart_rate_pct_max"

]

RESPONSE_TREND_VARIABLES = [

    "rpe_general_acute",

    "rpe_general_chronic",

    "rpe_general_ewma_7",

    "rpe_general_ewma_28",

    "wellness_sleep_ewma_7",

    "wellness_fatigue_ewma_7",

    "wellness_doms_ewma_7",

    "wellness_stress_ewma_7",

    "wellness_mood_ewma_7"

]

RESPONSE_COMPARISON_VARIABLES = [

    "rpe_general_percentile",

    "wellness_sleep_percentile",

    "wellness_fatigue_percentile",

    "wellness_doms_percentile",

    "wellness_stress_percentile",

    "wellness_mood_percentile",

    "heart_rate_avg_percentile",

    "heart_rate_max_percentile"

]

# =====================================================
# VARIABLES
# =====================================================

def build_variables(

    dimension,

    row

):

    for variable in RESPONSE_VARIABLES:

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

    for variable in RESPONSE_TREND_VARIABLES:

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

    for variable in RESPONSE_COMPARISON_VARIABLES:

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

        "rpe_general",

        "wellness_sleep",

        "wellness_fatigue",

        "wellness_doms",

        "wellness_stress",

        "wellness_mood",

        "heart_rate_avg"

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

            "La respuesta interna del jugador "

            "es excelente. Los indicadores de "

            "bienestar y percepción del esfuerzo "

            "son muy favorables."

        )

    elif score >= 70:

        text = (

            "La respuesta fisiológica y perceptiva "

            "es adecuada para la carga realizada."

        )

    elif score >= 50:

        text = (

            "La respuesta interna se encuentra "

            "dentro de los valores habituales."

        )

    elif score >= 30:

        text = (

            "Se observan algunos indicadores "

            "compatibles con una respuesta "

            "menos favorable."

        )

    else:

        text = (

            "La respuesta interna sugiere una "

            "recuperación insuficiente o un "

            "estado de fatiga elevado."

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

            "El jugador presenta una respuesta "

            "muy favorable a la carga."

        )

    elif score >= 70:

        recommendation = (

            "Continuar con la planificación "

            "prevista y seguir monitorizando "

            "los indicadores internos."

        )

    elif score >= 50:

        recommendation = (

            "No se requieren modificaciones "

            "específicas. Continuar con la "

            "monitorización habitual."

        )

    elif score >= 30:

        recommendation = (

            "Valorar estrategias de recuperación "

            "y revisar la evolución del wellness "

            "en las próximas sesiones."

        )

    else:

        recommendation = (

            "Priorizar la recuperación. Revisar "

            "la carga acumulada y considerar una "

            "reducción temporal de la exigencia."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_response_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Respuesta",

        description=(

            "Análisis de la respuesta interna "

            "del jugador frente a la carga "

            "de entrenamiento."

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

    sleep = row.get(

        "wellness_sleep_percentile",

        None

    )

    fatigue = row.get(

        "wellness_fatigue_percentile",

        None

    )

    doms = row.get(

        "wellness_doms_percentile",

        None

    )

    stress = row.get(

        "wellness_stress_percentile",

        None

    )

    mood = row.get(

        "wellness_mood_percentile",

        None

    )

    if sleep is not None and not pd.isna(sleep):

        score += (sleep - 50) * 0.15

    if fatigue is not None and not pd.isna(fatigue):

        score += (fatigue - 50) * 0.15

    if doms is not None and not pd.isna(doms):

        score += (doms - 50) * 0.15

    if stress is not None and not pd.isna(stress):

        score += (stress - 50) * 0.15

    if mood is not None and not pd.isna(mood):

        score += (mood - 50) * 0.20

    rpe = row.get(

        "rpe_general",

        None

    )

    if rpe is not None and not pd.isna(rpe):

        if rpe <= 5:

            score += 10

        elif rpe <= 7:

            score += 5

        elif rpe >= 9:

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
# BUILD RESPONSE DIMENSION
# =====================================================

def build_response_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Respuesta",

        description=(

            "Análisis de la respuesta "

            "interna del jugador ante "

            "la carga de entrenamiento."

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

