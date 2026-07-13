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
# LOAD MASTER
# =====================================================

master = pd.read_csv(

    "data/processed/master_team_stats.csv"

)

# =====================================================
# BUILD
# =====================================================

summary = build_team_summary(

    master

)

context = build_team_context(

    master

)

tactical = build_tactical_profile(

    summary,

    context

)

# =====================================================
# SAVE
# =====================================================

summary.to_csv(

    "data/processed/team_summary_test.csv",

    index=False

)

context.to_csv(

    "data/processed/team_context_summary_test.csv",

    index=False

)

tactical.to_csv(

    "data/processed/team_tactical_profile_test.csv",

    index=False

)

print("Motor generado correctamente.")