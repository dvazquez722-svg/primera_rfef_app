import pandas as pd

# =====================================================
# LOAD
# =====================================================

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

# =====================================================
# VARIABLES NUMÉRICAS
# =====================================================

numeric_cols = df.select_dtypes(
    include="number"
).columns

# =====================================================
# RESUMEN POR EQUIPO
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

print(team_summary.head())

print("\nShape:")
print(team_summary.shape)