import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# AVAILABILITY DIMENSION
# =====================================================

AVAILABILITY_VARIABLES = [

    "distance_m_acwr",

    "player_load_acwr",

    "high_speed_distance_acwr",

    "rpe_general",

    "wellness_sleep",

    "wellness_fatigue",

    "wellness_doms",

    "wellness_stress",

    "wellness_mood",

    "heart_rate_avg"

]

AVAILABILITY_SUPPORT_VARIABLES = [

    "distance_m_ewma_7",

    "player_load_ewma_7",

    "high_speed_distance_ewma_7",

    "distance_m_percentile",

    "player_load_percentile",

    "high_speed_distance_percentile"

]


# =====================================================
# BUILD AVAILABILITY DIMENSION
# =====================================================

def build_availability_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Disponibilidad",

        description=(

            "Estimación del estado de "

            "disponibilidad del jugador "

            "para entrenar y competir."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_support(

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

    for variable in AVAILABILITY_VARIABLES:

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
# SUPPORT
# =====================================================

def build_support(

    dimension,

    row

):

    for variable in AVAILABILITY_SUPPORT_VARIABLES:

        dimension.add_evidence(

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

    score = 100

    acwr = row.get(

        "player_load_acwr",

        None

    )

    fatigue = row.get(

        "wellness_fatigue",

        None

    )

    sleep = row.get(

        "wellness_sleep",

        None

    )

    doms = row.get(

        "wellness_doms",

        None

    )

    stress = row.get(

        "wellness_stress",

        None

    )

    if acwr is not None and not pd.isna(acwr):

        if acwr > 1.5:

            score -= 20

        elif acwr > 1.3:

            score -= 10

        elif acwr < 0.8:

            score -= 5

    if fatigue is not None and not pd.isna(fatigue):

        score -= fatigue * 2

    if doms is not None and not pd.isna(doms):

        score -= doms * 2

    if stress is not None and not pd.isna(stress):

        score -= stress * 2

    if sleep is not None and not pd.isna(sleep):

        score += sleep

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
# CONFIDENCE
# =====================================================

def build_confidence(

    dimension,

    row

):

    required = (

        AVAILABILITY_VARIABLES

        +

        AVAILABILITY_SUPPORT_VARIABLES

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

    if score >= 90:

        text = (

            "El jugador presenta un estado óptimo "

            "de disponibilidad para entrenar y competir."

        )

    elif score >= 75:

        text = (

            "La disponibilidad es elevada. No se "

            "detectan indicadores relevantes de riesgo."

        )

    elif score >= 60:

        text = (

            "La disponibilidad es adecuada, aunque "

            "conviene continuar monitorizando la "

            "respuesta del jugador."

        )

    elif score >= 40:

        text = (

            "Existen indicadores que sugieren una "

            "disminución de la disponibilidad."

        )

    else:

        text = (

            "La disponibilidad actual del jugador "

            "es reducida y requiere una valoración "

            "individual antes de incrementar la carga."

        )

    dimension.interpretation = text


# =====================================================
# RECOMMENDATION
# =====================================================

def build_recommendation(

    dimension

):

    score = dimension.score

    if score >= 90:

        recommendation = (

            "El jugador puede afrontar con normalidad "

            "las cargas previstas, manteniendo el "

            "seguimiento habitual."

        )

    elif score >= 75:

        recommendation = (

            "Mantener la planificación prevista y "

            "continuar monitorizando las variables "

            "de bienestar y carga."

        )

    elif score >= 60:

        recommendation = (

            "Revisar diariamente la evolución del "

            "wellness y de la carga acumulada antes "

            "de incrementar la exigencia."

        )

    elif score >= 40:

        recommendation = (

            "Considerar estrategias de recuperación "

            "y valorar una reducción temporal de la "

            "carga si la tendencia continúa."

        )

    else:

        recommendation = (

            "Se recomienda una valoración individual "

            "por parte del cuerpo técnico y del "

            "preparador físico antes de planificar "

            "la siguiente sesión."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_availability_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Disponibilidad",

        description=(

            "Estimación del estado de disponibilidad "

            "del jugador a partir de la integración "

            "de la carga, la intensidad y la respuesta."

        )

    )

    latest = player_df.iloc[-1]

    build_variables(

        dimension,

        latest

    )

    build_support(

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