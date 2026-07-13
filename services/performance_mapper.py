from services.performance_schema import (


    IDENTIFICATION_COLUMNS,

    SESSION_COLUMNS,

    LOAD_COLUMNS,

    INTENSITY_COLUMNS,

    RESPONSE_COLUMNS,

    HEART_RATE_COLUMNS,

    TREND_COLUMNS,

    CONTEXT_COLUMNS

)

# =====================================================
# PERFORMANCE MAPPER
# =====================================================

"""
Traduce cualquier proveedor GPS al
Performance Dataset oficial.

Actualmente preparado para:

- WIMU
- Catapult
- STATSports
- CSV personalizados

Todos terminarán utilizando exactamente
los mismos nombres internos.
"""

# =====================================================
# WIMU
# =====================================================

WIMU_MAPPING = {

    # -----------------------------------------------
    # IDENTIFICACIÓN
    # -----------------------------------------------

    "Player": "player",

    "Team": "team",

    "Season": "season",

    "Position": "position",

    "Date": "date",

    # -----------------------------------------------
    # SESIÓN
    # -----------------------------------------------

    "Session": "session",

    "Type Session": "type_session",

    "Session Phase": "session_phase",

    # -----------------------------------------------
    # CARGA
    # -----------------------------------------------

    "Distance": "total_distance",

    "Distance/min": "distance_per_min",

    "Player Load": "player_load",

    "Mechanical Load": "mechanical_load",

    "Energy": "energy_expenditure",

    "Duration": "duration",

    # -----------------------------------------------
    # INTENSIDAD
    # -----------------------------------------------

    "HSR Distance": "high_speed_distance",

    "Sprint Distance": "sprint_distance",

    "Sprint Count": "sprint_count",

    "Max Speed": "max_speed",

    "Accelerations": "accelerations",

    "Decelerations": "decelerations",

    "Metabolic Power": "metabolic_power",

    "HML Distance": "hml_distance"

}

import pandas as pd


# =====================================================
# PERFORMANCE MAPPER
# =====================================================

class PerformanceMapper:

    def __init__(

        self,

        mapping

    ):

        self.mapping = mapping

    # =================================================
    # RENAME COLUMNS
    # =================================================

    def rename_columns(

        self,

        df

    ):

        return df.rename(

            columns=self.mapping

        )

    # =================================================
    # KEEP KNOWN COLUMNS
    # =================================================

    def keep_known_columns(

        self,

        df

    ):

        valid_columns = [

            column

            for column in df.columns

            if column in self.mapping.values()

        ]

        return df[

            valid_columns

        ].copy()

    # =================================================
    # MAP DATASET
    # =================================================

    def transform(

        self,

        df

    ):

        df = self.rename_columns(

            df

        )

        df = self.keep_known_columns(

            df

        )

        return df