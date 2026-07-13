"""
==========================================================
DASHBOARD SERVICE
==========================================================

Servicio principal del módulo de Rendimiento.

Responsabilidades
-----------------
- Cargar el dataset de rendimiento.
- Mantener una única copia en memoria.
- Aplicar filtros globales.
- Devolver subconjuntos de datos.
- Proporcionar información común para todas las páginas.

No realiza cálculos deportivos.
No interpreta resultados.
No genera recomendaciones.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st


# ==========================================================
# PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "performance_dataset.csv"
)


# ==========================================================
# FILTER MODEL
# ==========================================================

@dataclass(slots=True)
class DashboardFilters:

    fecha_inicio: Optional[pd.Timestamp] = None

    fecha_fin: Optional[pd.Timestamp] = None

    jugador: Optional[str] = None

    equipo: Optional[str] = None

    competicion: Optional[str] = None

    microciclo: Optional[str] = None

    partido: Optional[str] = None

    tipo_sesion: Optional[str] = None


# ==========================================================
# DASHBOARD SERVICE
# ==========================================================

class DashboardService:

    """
    Servicio principal del dashboard.
    """

    def __init__(

        self,

        dataframe: pd.DataFrame

    ):

        self.df = dataframe.copy()

        self.validate_dataset()


# ==========================================================
# VALIDATION
# ==========================================================

    def validate_dataset(

        self

    ) -> None:

        required_columns = [

            "player",

            "team",

            "date"

        ]

        missing = [

            column

            for column in required_columns

            if column not in self.df.columns

        ]

        if missing:

            raise ValueError(

                "Faltan columnas obligatorias: "

                + ", ".join(missing)

            )

        self.df["date"] = pd.to_datetime(

            self.df["date"]

        )

        self.df.sort_values(

            "date",

            inplace=True

        )

        self.df.reset_index(

            drop=True,

            inplace=True

        )


# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_data(show_spinner=False)
def load_dataset(

    path: Path = DATASET_PATH

) -> pd.DataFrame:

    dataframe = pd.read_csv(

        path,

        low_memory=False

    )

    dataframe["date"] = pd.to_datetime(

        dataframe["date"]

    )

    return dataframe


# ==========================================================
# FACTORY
# ==========================================================

@st.cache_resource(show_spinner=False)
def get_dashboard_service(

) -> DashboardService:

    dataframe = load_dataset()

    return DashboardService(

        dataframe

    )