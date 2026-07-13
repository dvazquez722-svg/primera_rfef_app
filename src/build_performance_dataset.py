from pathlib import Path

import numpy as np
import pandas as pd


# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "Temporada 2022-2023 Las Palmas_CLEAN.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "performance_dataset.csv"
)


# =====================================================
# PERFORMANCE DATASET BUILDER
# =====================================================

class PerformanceDatasetBuilder:

    def __init__(

        self,

        dataframe

    ):

        self.raw = dataframe.copy()

        self.df = dataframe.copy()

    # =================================================
    # BUILD
    # =================================================

    def build(

        self

    ):

        self.build_identification()

        self.build_context()

        self.build_duration()

        self.build_external_load()

        self.build_high_speed_running()

        self.build_accelerations()

        self.build_decelerations()

        self.build_metabolic_load()

        self.build_internal_load()

        self.build_wellness()

        self.build_biomechanics()

        self.build_availability()

        self.clean_dataset()

        self.sort_dataset()

        self.validate_dataset()

        return self.df

    # =================================================
    # IDENTIFICATION
    # =================================================

    def build_identification(

        self

    ):

        self.df["player"] = self.get_column(

            "player"

        )

        self.df["team"] = self.get_column(

            "team"

        )

        self.df["position"] = self.get_column(

            "position"

        )

        self.df["sport"] = self.get_column(

            "sport"

        )

        self.df["date"] = pd.to_datetime(

            self.get_column(

                "date"

            )

        )

        self.df["season"] = self.generate_season()

        self.df["competition"] = self.get_column(

            "competition"

        )

        self.df["opponent"] = self.get_column(

            "opponent"

        )

        self.df["home_away"] = self.get_column(

            "home_away"

        )

        players = (

            self.df["player"]

            .drop_duplicates()

            .reset_index(

                drop=True

            )

        )

        mapping = {

            player: idx + 1

            for idx, player in enumerate(

                players

            )

        }

        self.df.insert(

            0,

            "player_id",

            self.df["player"].map(

                mapping

            )

        )
    # =================================================
    # CONTEXT
    # =================================================

    def build_context(

        self

    ):

        self.df["session"] = self.get_column(

            "session"

        )

        self.df["type_session"] = self.get_column(

            "type_session"

        )

        self.df["group"] = self.get_column(

            "group"

        )

        self.df["match_day"] = self.get_column(

            "match_day"

        )

        self.df["week_calendar"] = self.get_column(

            "week_calendar"

        )

        self.df["week_team"] = self.get_column(

            "week_team"

        )

        self.df["week_match_day"] = self.get_column(

            "week_match_day"

        )

        self.df["num_session_day"] = self.to_numeric(

            self.get_column(

                "num_session_day"

            )

        )

        self.df["num_total_session"] = self.to_numeric(

            self.get_column(

                "num_total_session"

            )

        )

        self.df["is_match"] = (

            self.df["type_session"]

            .astype(str)

            .str.lower()

            .str.contains(

                "match",

                na=False

            )

        )

        self.df["is_training"] = ~self.df["is_match"]


    # =================================================
    # DURATION
    # =================================================

    def build_duration(

        self

    ):

        self.df["start_hour"] = self.get_column(

            "start_hour"

        )

        self.df["final_hour"] = self.get_column(

            "final_hour"

        )

        self.df["start_hour_seconds"] = self.to_numeric(

            self.get_column(

                "start_hour_seconds"

            )

        )

        self.df["final_hour_seconds"] = self.to_numeric(

            self.get_column(

                "final_hour_seconds"

            )

        )

        self.df["drills_duration"] = self.to_numeric(

            self.get_column(

                "drills_duration"

            )

        )

        self.df["positioning_duration"] = self.to_numeric(

            self.get_column(

                "positioning_duration"

            )

        )

        self.df["session_duration_min"] = (

            self.df["final_hour_seconds"]

            -

            self.df["start_hour_seconds"]

        ) / 60

        self.df["effective_duration_min"] = (

            self.df["drills_duration"]

            / 60

        )

        self.df["positioning_duration_min"] = (

            self.df["positioning_duration"]

            / 60

        )

        self.df["rest_duration_min"] = (

            self.df["session_duration_min"]

            -

            self.df["effective_duration_min"]

        )

        self.df["work_rest_ratio"] = np.where(

            self.df["rest_duration_min"] > 0,

            self.df["effective_duration_min"]

            /

            self.df["rest_duration_min"],

            np.nan

        )

    # =================================================
    # EXTERNAL LOAD
    # =================================================

    def build_external_load(

        self

    ):

        self.df["distance_m"] = self.to_numeric(

            self.find_column(

                [

                    "distance_abs_m",

                    "distance_m",

                    "total_distance",

                    "distance"

                ]

            )

        )

        self.df["distance_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["distance_m"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["player_load"] = self.to_numeric(

            self.find_column(

                [

                    "player_load_a_u",

                    "player_load",

                    "playerload"

                ]

            )

        )

        self.df["player_load_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["player_load"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["mechanical_load"] = self.to_numeric(

            self.find_column(

                [

                    "dsl_a_u",

                    "dynamic_stress_load",

                    "mechanical_load"

                ]

            )

        )

        self.df["energy_kcal"] = self.to_numeric(

            self.find_column(

                [

                    "energy_expenditure_kcal",

                    "energy_kcal"

                ]

            )

        )

        self.df["energy_kcal_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["energy_kcal"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["distance_player_load_ratio"] = np.where(

            self.df["player_load"] > 0,

            self.df["distance_m"]

            /

            self.df["player_load"],

            np.nan

        )

    # =================================================
    # HIGH SPEED RUNNING
    # =================================================

    def build_high_speed_running(

        self

    ):

        self.df["high_speed_distance"] = self.to_numeric(

            self.find_column(

                [

                    "abs_hsr_m",

                    "high_speed_distance",

                    "hsr_distance"

                ]

            )

        )

        self.df["high_speed_distance_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["high_speed_distance"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["high_speed_actions"] = self.to_numeric(

            self.find_column(

                [

                    "abs_hsr_count",

                    "high_speed_actions",

                    "hsr_count"

                ]

            )

        )

        self.df["sprint_distance"] = self.to_numeric(

            self.find_column(

                [

                    "abs_sprint_m",

                    "sprint_distance"

                ]

            )

        )

        self.df["sprint_distance_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["sprint_distance"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["sprint_count"] = self.to_numeric(

            self.find_column(

                [

                    "sprints_abs_count",

                    "sprint_count",

                    "sprints"

                ]

            )

        )

        self.df["sprints_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["sprint_count"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

        self.df["max_speed"] = self.to_numeric(

            self.find_column(

                [

                    "max_speed_km_h",

                    "max_speed"

                ]

            )

        )

    # =================================================
    # ACCELERATIONS
    # =================================================

    def build_accelerations(

        self

    ):

        self.df["accelerations"] = self.to_numeric(

            self.find_column(

                [

                    "accelerations_count",

                    "accelerations",

                    "acc_count"

                ]

            )

        )

        self.df["accelerations_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["accelerations"]

            /

            self.df["effective_duration_min"],

            np.nan

        )


    # =================================================
    # DECELERATIONS
    # =================================================

    def build_decelerations(

        self

    ):

        self.df["decelerations"] = self.to_numeric(

            self.find_column(

                [

                    "decelerations_count",

                    "decelerations",

                    "dec_count"

                ]

            )

        )

        self.df["decelerations_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["decelerations"]

            /

            self.df["effective_duration_min"],

            np.nan

        )


    # =================================================
    # METABOLIC LOAD
    # =================================================

    def build_metabolic_load(

        self

    ):

        self.df["hmld"] = self.to_numeric(

            self.find_column(

                [

                    "hmld_m",

                    "hmld",

                    "high_metabolic_load_distance"

                ]

            )

        )

        self.df["metabolic_power"] = self.to_numeric(

            self.find_column(

                [

                    "power_metabolic_w_kg",

                    "metabolic_power",

                    "metabolic_power_w_kg"

                ]

            )

        )

        self.df["energy_expenditure"] = self.to_numeric(

            self.find_column(

                [

                    "energy_expenditure_kcal",

                    "energy_kcal",

                    "energy_expenditure"

                ]

            )

        )

        self.df["energy_expenditure_per_min"] = np.where(

            self.df["effective_duration_min"] > 0,

            self.df["energy_expenditure"]

            /

            self.df["effective_duration_min"],

            np.nan

        )

    # =================================================
    # INTERNAL LOAD
    # =================================================

    def build_internal_load(

        self

    ):

        self.df["rpe_general"] = self.to_numeric(

            self.find_column(

                [

                    "rpe_general",

                    "rpe"

                ]

            )

        )

        self.df["rpe_peripheral"] = self.to_numeric(

            self.find_column(

                [

                    "rpe_peripheral",

                    "rpe_muscular"

                ]

            )

        )

        self.df["heart_rate_avg"] = self.to_numeric(

            self.find_column(

                [

                    "avg_heart_rate_bpm",

                    "average_hr",

                    "heart_rate_avg"

                ]

            )

        )

        self.df["heart_rate_max"] = self.to_numeric(

            self.find_column(

                [

                    "max_heart_rate_bpm",

                    "heart_rate_max",

                    "max_hr"

                ]

            )

        )

        self.df["heart_rate_pct_max"] = self.to_numeric(

            self.find_column(

                [

                    "avg_hr_pct_of_player_max_hr",

                    "heart_rate_pct_max"

                ]

            )

        )

        self.df["session_load"] = (

            self.df["rpe_general"]

            *

            self.df["effective_duration_min"]

        )


    # =================================================
    # WELLNESS
    # =================================================

    def build_wellness(

        self

    ):

        self.df["wellness_sleep"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_sleep",

                    "sleep"

                ]

            )

        )

        self.df["wellness_fatigue"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_fatigue",

                    "wellness_fatige",

                    "fatigue"

                ]

            )

        )

        self.df["wellness_doms"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_doms",

                    "doms"

                ]

            )

        )

        self.df["wellness_stress"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_stress",

                    "stress"

                ]

            )

        )

        self.df["wellness_mood"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_mood",

                    "mood"

                ]

            )

        )

        wellness = [

            "wellness_sleep",

            "wellness_fatigue",

            "wellness_doms",

            "wellness_stress",

            "wellness_mood"

        ]

        self.df["wellness_score"] = self.df[

            wellness

        ].mean(

            axis=1,

            skipna=True

        )

    # =================================================
    # INTERNAL LOAD
    # =================================================

    def build_internal_load(

        self

    ):

        self.df["rpe_general"] = self.to_numeric(

            self.find_column(

                [

                    "rpe_general",

                    "rpe"

                ]

            )

        )

        self.df["rpe_peripheral"] = self.to_numeric(

            self.find_column(

                [

                    "rpe_peripheral",

                    "rpe_muscular"

                ]

            )

        )

        self.df["heart_rate_avg"] = self.to_numeric(

            self.find_column(

                [

                    "avg_heart_rate_bpm",

                    "average_hr",

                    "heart_rate_avg"

                ]

            )

        )

        self.df["heart_rate_max"] = self.to_numeric(

            self.find_column(

                [

                    "max_heart_rate_bpm",

                    "heart_rate_max",

                    "max_hr"

                ]

            )

        )

        self.df["heart_rate_pct_max"] = self.to_numeric(

            self.find_column(

                [

                    "avg_hr_pct_of_player_max_hr",

                    "heart_rate_pct_max"

                ]

            )

        )

        self.df["session_load"] = (

            self.df["rpe_general"]

            *

            self.df["effective_duration_min"]

        )


    # =================================================
    # WELLNESS
    # =================================================

    def build_wellness(

        self

    ):

        self.df["wellness_sleep"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_sleep",

                    "sleep"

                ]

            )

        )

        self.df["wellness_fatigue"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_fatigue",

                    "wellness_fatige",

                    "fatigue"

                ]

            )

        )

        self.df["wellness_doms"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_doms",

                    "doms"

                ]

            )

        )

        self.df["wellness_stress"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_stress",

                    "stress"

                ]

            )

        )

        self.df["wellness_mood"] = self.to_numeric(

            self.find_column(

                [

                    "wellness_mood",

                    "mood"

                ]

            )

        )

        wellness = [

            "wellness_sleep",

            "wellness_fatigue",

            "wellness_doms",

            "wellness_stress",

            "wellness_mood"

        ]

        self.df["wellness_score"] = self.df[

            wellness

        ].mean(

            axis=1,

            skipna=True

        )