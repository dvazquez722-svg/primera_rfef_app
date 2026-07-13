from pathlib import Path

import pandas as pd


# =====================================================
# PERFORMANCE DATASET
# =====================================================

"""
Este módulo prepara el dataset estándar que utilizará
todo el módulo de Rendimiento Físico.

Responsabilidades

- Cargar el dataset.
- Validar columnas.
- Estandarizar nombres.
- Convertir tipos de datos.
- Detectar métricas disponibles.

No realiza:

- Gráficos.
- Interpretaciones.
- Recomendaciones.
- Cálculos científicos.
"""

# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [

    "player",

    "date",

    "team",

    "season"

]

# =====================================================
# OPTIONAL COLUMNS
# =====================================================

OPTIONAL_COLUMNS = [

    "position",

    "session",

    "type_session",

    "session_phase",

    "week_of_year",

    "day_of_week",

    "month"

]

# =====================================================
# DATASET CLASS
# =====================================================

class PerformanceDataset:

    def __init__(

        self,

        dataset_path

    ):

        self.dataset_path = Path(

            dataset_path

        )

        self.df = None

    # =====================================================
    # LOAD DATASET
    # =====================================================

    def load(

        self

    ):

        if not self.dataset_path.exists():

            raise FileNotFoundError(

                f"No existe el archivo: {self.dataset_path}"

            )

        suffix = self.dataset_path.suffix.lower()

        if suffix == ".csv":

            self.df = pd.read_csv(

                self.dataset_path

            )

        elif suffix in [

            ".xlsx",

            ".xls"

        ]:

            self.df = pd.read_excel(

                self.dataset_path

            )

        else:

            raise ValueError(

                "Formato de archivo no soportado."

            )

        self.validate_required_columns()

        self.standardize_types()

        self.remove_duplicates()

        self.sort_dataset()

        return self.df

    # =====================================================
    # VALIDATE REQUIRED COLUMNS
    # =====================================================

    def validate_required_columns(

        self

    ):

        missing = [

            col

            for col in REQUIRED_COLUMNS

            if col not in self.df.columns

        ]

        if missing:

            raise ValueError(

                "Faltan columnas obligatorias:\n\n"

                + "\n".join(missing)

            )

    # =====================================================
    # STANDARDIZE TYPES
    # =====================================================

    def standardize_types(

        self

    ):

        self.df["date"] = pd.to_datetime(

            self.df["date"]

        )

        self.df["player"] = (

            self.df["player"]

            .astype(str)

            .str.strip()

        )

        self.df["team"] = (

            self.df["team"]

            .astype(str)

            .str.strip()

        )

        self.df["season"] = (

            self.df["season"]

            .astype(str)

            .str.strip()

        )

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    def remove_duplicates(

        self

    ):

        self.df = (

            self.df

            .drop_duplicates()

            .reset_index(

                drop=True

            )

        )

    # =====================================================
    # SORT DATASET
    # =====================================================

    def sort_dataset(

        self

    ):

        sort_columns = [

            col

            for col in [

                "player",

                "date"

            ]

            if col in self.df.columns

        ]

        if sort_columns:

            self.df = (

                self.df

                .sort_values(

                    sort_columns

                )

                .reset_index(

                    drop=True

                )

            )

    # =====================================================
    # AVAILABLE COLUMNS
    # =====================================================

    def get_columns(

        self

    ):

        return list(

            self.df.columns

        )

    # =====================================================
    # AVAILABLE PLAYERS
    # =====================================================

    def get_players(

        self

    ):

        return sorted(

            self.df[

                "player"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =====================================================
    # AVAILABLE TEAMS
    # =====================================================

    def get_teams(

        self

    ):

        return sorted(

            self.df[

                "team"

            ]

            .dropna()

            .unique()

            .tolist()

        )

    # =====================================================
    # AVAILABLE SEASONS
    # =====================================================

    def get_seasons(

        self

    ):

        return sorted(

            self.df[

                "season"

            ]

            .dropna()

            .unique()

            .tolist()

        )
    
    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def summary(

        self

    ):

        return {

            "rows": len(

                self.df

            ),

            "columns": len(

                self.df.columns

            ),

            "players": len(

                self.get_players()

            ),

            "teams": len(

                self.get_teams()

            ),

            "seasons": len(

                self.get_seasons()

            ),

            "date_min": self.df[

                "date"

            ].min(),

            "date_max": self.df[

                "date"

            ].max()

        }

    # =====================================================
    # CHECK COLUMN
    # =====================================================

    def has_column(

        self,

        column

    ):

        return (

            column

            in

            self.df.columns

        )

    # =====================================================
    # CHECK COLUMNS
    # =====================================================

    def has_columns(

        self,

        columns

    ):

        return all(

            column in self.df.columns

            for column in columns

        )

    # =====================================================
    # GET PLAYER DATA
    # =====================================================

    def get_player(

        self,

        player

    ):

        return (

            self.df[

                self.df["player"]

                ==

                player

            ]

            .copy()

        )

    # =====================================================
    # GET TEAM DATA
    # =====================================================

    def get_team(

        self,

        team

    ):

        return (

            self.df[

                self.df["team"]

                ==

                team

            ]

            .copy()

        )

    # =====================================================
    # GET SEASON DATA
    # =====================================================

    def get_season(

        self,

        season

    ):

        return (

            self.df[

                self.df["season"]

                ==

                season

            ]

            .copy()

        )