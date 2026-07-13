import pandas as pd


# =====================================================
# PERFORMANCE DIMENSIONS
# =====================================================

"""
Cada dimensión representa una parte del estado físico
del jugador.

Las funciones de este módulo NO realizan:

- Interpretaciones
- Recomendaciones
- Colores
- Semáforos

Únicamente organizan las variables que pertenecen
a cada dimensión.
"""


# =====================================================
# LOAD
# =====================================================

def calculate_load(

    profile

):

    data = profile["raw_data"]

    dimension = {

        "name": "Carga",

        "description": (

            "Cantidad de trabajo realizada "

            "por el jugador."

        ),

        "variables": {},

        "score": None,

        "confidence": None

    }

    return dimension