import pandas as pd

from services.performance_dimension import (
    PerformanceDimension
)

from services.performance_variable import (
    PerformanceVariable
)

# =====================================================
# LOAD DIMENSION
# =====================================================

LOAD_VARIABLES = [

    "distance_m",

    "distance_per_min",

    "player_load",

    "player_load_per_min",

    "mechanical_load",

    "energy_kcal",

    "energy_kcal_min",

    "effective_duration_min",

    "work_rest_ratio",

    "distance_player_load_ratio"

]

LOAD_TREND_VARIABLES = [

    "distance_m_acute",

    "distance_m_chronic",

    "distance_m_ewma_7",

    "distance_m_ewma_28",

    "distance_m_acwr",

    "player_load_acute",

    "player_load_chronic",

    "player_load_ewma_7",

    "player_load_ewma_28",

    "player_load_acwr"

]

LOAD_COMPARISON_VARIABLES = [

    "distance_m_percentile",

    "player_load_percentile",

    "distance_m_ranking",

    "player_load_ranking",

    "distance_m_zscore",

    "player_load_zscore"

]


# =====================================================
# BUILD LOAD DIMENSION
# =====================================================

def build_load_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Carga",

        description=(

            "Análisis de la carga externa "

            "del jugador."

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

# =====================================================
# VARIABLES
# =====================================================

def build_variables(

    dimension,

    row

):

    for variable in LOAD_VARIABLES:

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

    for variable in LOAD_TREND_VARIABLES:

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

    for variable in LOAD_COMPARISON_VARIABLES:

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

    player_load_percentile = row.get(

        "player_load_percentile",

        None

    )

    distance_percentile = row.get(

        "distance_m_percentile",

        None

    )

    acwr = row.get(

        "player_load_acwr",

        None

    )

    if player_load_percentile is not None:

        if not pd.isna(

            player_load_percentile

        ):

            score += (

                player_load_percentile

                - 50

            ) * 0.30

    if distance_percentile is not None:

        if not pd.isna(

            distance_percentile

        ):

            score += (

                distance_percentile

                - 50

            ) * 0.30

    if acwr is not None:

        if not pd.isna(

            acwr

        ):

            if 0.8 <= acwr <= 1.3:

                score += 20

            elif 1.3 < acwr <= 1.5:

                score += 10

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
# CONFIDENCE
# =====================================================

def build_confidence(

    dimension,

    row

):

    required = [

        "distance_m",

        "player_load",

        "distance_m_acwr",

        "player_load_acwr",

        "distance_m_percentile",

        "player_load_percentile"

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

            "La carga externa del jugador "

            "se encuentra muy por encima "

            "de su nivel habitual."

        )

    elif score >= 70:

        text = (

            "La carga externa es elevada "

            "y acorde al momento de la "

            "temporada."

        )

    elif score >= 50:

        text = (

            "La carga externa se encuentra "

            "dentro de los valores esperados."

        )

    elif score >= 30:

        text = (

            "La carga externa es inferior "

            "a la habitual del jugador."

        )

    else:

        text = (

            "La carga externa es muy baja "

            "respecto a su referencia."

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

            "Mantener una monitorización estrecha. "

            "Valorar estrategias de recuperación y "

            "controlar la carga de las próximas sesiones."

        )

    elif score >= 70:

        recommendation = (

            "La carga es adecuada. Continuar con la "

            "planificación prevista y monitorizar la "

            "respuesta del jugador."

        )

    elif score >= 50:

        recommendation = (

            "La carga se encuentra dentro del rango "

            "esperado. No se requieren modificaciones."

        )

    elif score >= 30:

        recommendation = (

            "Valorar un incremento progresivo de la "

            "carga para aproximarse a los valores "

            "habituales del jugador."

        )

    else:

        recommendation = (

            "Carga muy reducida. Revisar el motivo "

            "(recuperación, lesión, descanso o baja "

            "participación) antes de modificar la "

            "planificación."

        )

    dimension.recommendation = recommendation


# =====================================================
# BUILD COMPLETE DIMENSION
# =====================================================

def build_load_dimension(

    player_df

):

    dimension = PerformanceDimension(

        name="Carga",

        description=(

            "Análisis de la carga externa "

            "del jugador."

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

