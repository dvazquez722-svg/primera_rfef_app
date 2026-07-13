import pandas as pd

from src.team_summary import (
    build_team_summary
)

from src.team_context_summary import (
    build_team_context
)

from utils.tactical_profile import (
    build_tactical_profile
)

# =====================================================
# LOAD DYNAMIC TEAM
# =====================================================

def load_dynamic_team(

    master_df,
    team,
    start_date=None,
    end_date=None,
    matches_limit=None

):

    """
    Devuelve dinámicamente:

    - team_summary
    - team_tactical
    - team_matches

    utilizando el motor de cálculo.
    """

    # =====================================================
    # LIGA COMPLETA
    # =====================================================

    league_summary = build_team_summary(

        master_df

    )

    league_context = build_team_context(

        master_df

    )

    # =====================================================
    # PARTIDOS DEL EQUIPO
    # =====================================================

    team_matches = (

        master_df[

            master_df["Equipo"] == team

        ]

        .copy()

    )

    if "Fecha" in team_matches.columns:

        team_matches["Fecha"] = pd.to_datetime(

            team_matches["Fecha"]

        )

        team_matches = (

            team_matches

            .sort_values(

                "Fecha"

            )

        )

    # =====================================================
    # FILTRO POR FECHAS
    # =====================================================

    if start_date is not None:

        team_matches = (

            team_matches[

                team_matches["Fecha"] >= pd.to_datetime(

                    start_date

                )

            ]

        )

    if end_date is not None:

        team_matches = (

            team_matches[

                team_matches["Fecha"] <= pd.to_datetime(

                    end_date

                )

            ]

        )

    # =====================================================
    # ÚLTIMOS N PARTIDOS
    # =====================================================

    if matches_limit is not None:

        team_matches = (

            team_matches

            .tail(

                matches_limit

            )

        )

    # =====================================================
    # SEGURIDAD
    # =====================================================

    if team_matches.empty:

        team_matches = (

            master_df[

                master_df["Equipo"] == team

            ]

            .copy()

        )

        team_matches["Fecha"] = pd.to_datetime(

            team_matches["Fecha"]

        )

        team_matches = (

            team_matches

            .sort_values(

                "Fecha"

            )

        )

    # =====================================================
    # RESUMEN DINÁMICO
    # =====================================================

    team_summary = build_team_summary(

        team_matches

    )

    team_context = build_team_context(

        team_matches

    )

    # =====================================================
    # ACTUALIZAR LIGA
    # =====================================================

    league_summary = (

        league_summary[

            league_summary["Equipo"] != team

        ]

    )

    league_summary = pd.concat(

        [

            league_summary,

            team_summary

        ],

        ignore_index=True

    )

    league_context = (

        league_context[

            league_context["Equipo"] != team

        ]

    )

    league_context = pd.concat(

        [

            league_context,

            team_context

        ],

        ignore_index=True

    )

    # =====================================================
    # PERFIL TÁCTICO
    # =====================================================

    tactical = build_tactical_profile(

        league_summary,

        league_context

    )

    # =====================================================
    # EXTRAER EQUIPO
    # =====================================================

    team_summary = (

        league_summary[

            league_summary["Equipo"] == team

        ]

        .iloc[0]

    )

    team_tactical = (

        tactical[

            tactical["Equipo"] == team

        ]

        .iloc[0]

    )

    # =====================================================
    # DEVOLVER
    # =====================================================

    return (

        team_summary,

        team_tactical,

        team_matches

    )