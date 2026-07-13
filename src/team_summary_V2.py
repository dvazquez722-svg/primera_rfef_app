import pandas as pd

# =====================================================
# LOAD
# =====================================================

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

# =====================================================
# NUMERIC COLS
# =====================================================

numeric_cols = (
    df.select_dtypes(
        include="number"
    )
    .columns
)

# =====================================================
# TEAM SUMMARY
# =====================================================

team_summary = (
    df.groupby("Equipo")[numeric_cols]
      .mean()
      .round(2)
      .reset_index()
)

# =====================================================
# SAVE
# =====================================================

team_summary.to_csv(
    "data/processed/team_summary.csv",
    index=False
)

# =====================================================
# CHECKS
# =====================================================

print("\nShape:")
print(team_summary.shape)

print("\nEquipos:")
print(team_summary["Equipo"].nunique())

print("\nGoles recibidos:")
print(
    team_summary[
        ["Equipo", "Goles recibidos"]
    ]
    .sort_values(
        "Goles recibidos"
    )
    .head(10)
)

print("\nxG:")
print(
    team_summary[
        ["Equipo", "xG"]
    ]
    .sort_values(
        "xG",
        ascending=False
    )
    .head(10)
)

print("\nShape original:")
print(df.shape)

print("\nDuplicados Equipo-Partido:")
print(
    df[
        ["Equipo", "Partido"]
    ]
    .duplicated()
    .sum()
)

context = pd.read_csv(
    "data/processed/team_summary.csv"
)

print(
    context.columns.tolist()
)