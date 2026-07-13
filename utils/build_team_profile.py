from utils.build_team_summary import (
    build_team_summary
)

from utils.build_team_context import (
    build_team_context
)


# =====================================================
# BUILD TEAM PROFILE
# =====================================================

def build_team_profile(team_matches):

    """
    Genera automáticamente el perfil estadístico del equipo
    a partir de los partidos seleccionados.

    Devuelve:

        summary
        context

    (El perfil táctico se añadirá en la siguiente fase).
    """

    summary = build_team_summary(

        team_matches

    )

    context = build_team_context(

        team_matches

    )

    return (

        summary,

        context

    )