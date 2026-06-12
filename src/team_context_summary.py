import pandas as pd

# =====================================================
# LOAD
# =====================================================

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

# =====================================================
# METRICS
# =====================================================

metrics = [
    "xG",
    "Posesión del balón, %",
    "PPDA",
    "GF",
    "GC",
    "Puntos"
]

# =====================================================
# RESULT CONTEXT
# =====================================================

victories = (
    df[df["Resultado"] == "Victoria"]
    .groupby("Equipo")[metrics]
    .mean()
    .add_suffix("_Victoria")
)

draws = (
    df[df["Resultado"] == "Empate"]
    .groupby("Equipo")[metrics]
    .mean()
    .add_suffix("_Empate")
)

losses = (
    df[df["Resultado"] == "Derrota"]
    .groupby("Equipo")[metrics]
    .mean()
    .add_suffix("_Derrota")
)

# =====================================================
# HOME / AWAY CONTEXT
# =====================================================

home = (
    df[df["Condicion"] == "Local"]
    .groupby("Equipo")[metrics]
    .mean()
    .add_suffix("_Local")
)

away = (
    df[df["Condicion"] == "Visitante"]
    .groupby("Equipo")[metrics]
    .mean()
    .add_suffix("_Visitante")
)

# =====================================================
# MERGE
# =====================================================

context = (
    victories
    .join(draws)
    .join(losses)
    .join(home)
    .join(away)
    .reset_index()
)

context = context.round(2)

# =====================================================
# SAVE
# =====================================================

context.to_csv(
    "data/processed/team_context_summary.csv",
    index=False
)

# =====================================================
# CHECKS
# =====================================================

print("\nShape:")
print(context.shape)

print("\nEquipos:")
print(
    context["Equipo"]
    .nunique()
)

print("\nColumnas:")
print(
    len(context.columns)
)

print("\nPreview:")
print(
    context.head()
)

context = pd.read_csv(
    "data/processed/team_context_summary.csv"
)

print(
    context.columns.tolist()
)