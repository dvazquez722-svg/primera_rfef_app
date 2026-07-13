from pathlib import Path

import numpy as np
import pandas as pd

# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PERFORMANCE_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "performance_dataset.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics_dataset.csv"
)

# =====================================================
# ANALYTICS DATASET BUILDER
# =====================================================

class AnalyticsDatasetBuilder:

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

        self.df = self.df.sort_values(

            [

                "player",

                "date"

            ]

        ).reset_index(

            drop=True

        )

        self.build_relative_metrics()

        self.build_acute_load()

        self.build_chronic_load()

        self.build_ewma()

        self.build_acwr()

        self.build_percentiles()

        self.build_rankings()

        self.build_zscores()

        self.clean_dataset()

        return self.df

    # =================================================
    # RELATIVE METRICS
    # =================================================

    def build_relative_metrics(

        self

    ):

        duration = self.df[

            "effective_duration_min"

        ].replace(

            0,

            np.nan

        )

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "energy_kcal",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations",

            "sprint_count"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_per_min"

            ] = (

                self.df[metric]

                /

                duration

            )

        return self.df
    
    # =================================================
    # ACUTE LOAD
    # =================================================

    def build_acute_load(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_acute"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.rolling(

                        window=7,

                        min_periods=1

                    ).mean()

                )

            )

        return self.df

    # =================================================
    # CHRONIC LOAD
    # =================================================

    def build_chronic_load(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_chronic"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.rolling(

                        window=28,

                        min_periods=1

                    ).mean()

                )

            )

        return self.df

    # =================================================
    # EWMA
    # =================================================

    def build_ewma(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_ewma_7"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.ewm(

                        span=7,

                        adjust=False

                    ).mean()

                )

            )

            self.df[

                f"{metric}_ewma_28"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.ewm(

                        span=28,

                        adjust=False

                    ).mean()

                )

            )

        return self.df
    
    # =================================================
    # ACUTE LOAD
    # =================================================

    def build_acute_load(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_acute"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.rolling(

                        window=7,

                        min_periods=1

                    ).mean()

                )

            )

        return self.df

    # =================================================
    # CHRONIC LOAD
    # =================================================

    def build_chronic_load(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_chronic"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.rolling(

                        window=28,

                        min_periods=1

                    ).mean()

                )

            )

        return self.df

    # =================================================
    # EWMA
    # =================================================

    def build_ewma(

        self

    ):

        metrics = [

            "distance_m",

            "player_load",

            "mechanical_load",

            "high_speed_distance",

            "sprint_distance",

            "accelerations",

            "decelerations"

        ]

        for metric in metrics:

            if metric not in self.df.columns:

                continue

            self.df[

                f"{metric}_ewma_7"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.ewm(

                        span=7,

                        adjust=False

                    ).mean()

                )

            )

            self.df[

                f"{metric}_ewma_28"

            ] = (

                self.df

                .groupby(

                    "player"

                )[metric]

                .transform(

                    lambda x:

                    x.ewm(

                        span=28,

                        adjust=False

                    ).mean()

                )

            )

        return self.dfs
    
    # =================================================
    # CLEAN DATASET
    # =================================================

    def clean_dataset(

        self

    ):

        self.df = self.df.replace(

            [

                np.inf,

                -np.inf

            ],

            np.nan

        )

        self.df = self.df.loc[

            :,

            ~self.df.columns.duplicated()

        ]

        self.df = self.df.sort_values(

            [

                "player",

                "date"

            ]

        ).reset_index(

            drop=True

        )

        return self.df

    # =================================================
    # SUMMARY
    # =================================================

    def summary(

        self

    ):

        print(

            "=" * 60

        )

        print(

            "ANALYTICS DATASET"

        )

        print(

            "=" * 60

        )

        print(

            f"Filas: {len(self.df)}"

        )

        print(

            f"Columnas: {len(self.df.columns)}"

        )

        print(

            f"Jugadores: {self.df['player'].nunique()}"

        )

        print(

            f"Equipos: {self.df['team'].nunique()}"

        )

        print(

            f"Fechas: {self.df['date'].min()} -> {self.df['date'].max()}"

        )

        print(

            "=" * 60

        )

    # =================================================
    # EXPORT
    # =================================================

    def export(

        self,

        output_path

    ):

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        self.df.to_csv(

            output_path,

            index=False,

            encoding="utf-8-sig"

        )

        print(

            f"Analytics Dataset guardado en:\n{output_path}"

        )

# =====================================================
# MAIN
# =====================================================

def main():

    performance = pd.read_csv(

        PERFORMANCE_DATA,

        low_memory=False

    )

    builder = AnalyticsDatasetBuilder(

        performance

    )

    analytics = builder.build()

    builder.summary()

    builder.export(

        OUTPUT_DATA

    )

if __name__ == "__main__":

    main()