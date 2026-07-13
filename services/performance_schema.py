# =====================================================
# PERFORMANCE SCHEMA
# =====================================================

"""
Definición oficial del Performance Dataset.

Este archivo centraliza todas las columnas utilizadas
por la plataforma.

Cualquier modificación del dataset deberá realizarse
aquí antes de afectar al resto de módulos.
"""

# =====================================================
# IDENTIFICATION
# =====================================================

IDENTIFICATION_COLUMNS = [

    "player",

    "team",

    "season",

    "position",

    "date"

]

# =====================================================
# SESSION
# =====================================================

SESSION_COLUMNS = [

    "session",

    "type_session",

    "session_phase",

    "week_of_year",

    "day_of_week",

    "month"

]

# =====================================================
# EXTERNAL LOAD
# =====================================================

LOAD_COLUMNS = [

    "total_distance",

    "distance_per_min",

    "player_load",

    "mechanical_load",

    "energy_expenditure",

    "duration"

]

# =====================================================
# INTENSITY
# =====================================================

INTENSITY_COLUMNS = [

    "high_speed_distance",

    "sprint_distance",

    "sprint_count",

    "max_speed",

    "accelerations",

    "decelerations",

    "metabolic_power",

    "hml_distance"

]

# =====================================================
# INTERNAL LOAD
# =====================================================

RESPONSE_COLUMNS = [

    "wellness",

    "fatigue",

    "sleep",

    "stress",

    "muscle_soreness",

    "mood",

    "rpe"

]

# =====================================================
# HEART RATE
# =====================================================

HEART_RATE_COLUMNS = [

    "heart_rate_avg",

    "heart_rate_max",

    "heart_rate_min",

    "heart_rate_reserve",

    "hrv"

]

# =====================================================
# TREND
# =====================================================

TREND_COLUMNS = [

    "acute_load",

    "chronic_load",

    "acwr",

    "ewma_7",

    "ewma_28",

    "rolling_7",

    "rolling_28"

]

# =====================================================
# PREDICTIONS
# =====================================================

PREDICTION_COLUMNS = [

    "pred_distance",

    "pred_player_load",

    "pred_hsr",

    "prediction_confidence"

]

# =====================================================
# CONTEXT
# =====================================================

CONTEXT_COLUMNS = [

    "is_training",

    "is_match",

    "is_friendly",

    "minutes_played",

    "days_since_match",

    "days_until_match"

]

# =====================================================
# PERFORMANCE DIMENSIONS
# =====================================================

DIMENSION_MAP = {

    "Carga": LOAD_COLUMNS,

    "Intensidad": INTENSITY_COLUMNS,

    "Respuesta": (

        RESPONSE_COLUMNS

        +

        HEART_RATE_COLUMNS

    ),

    "Tendencia": TREND_COLUMNS,

    "Microciclo": CONTEXT_COLUMNS,

    "Comparación": []

}