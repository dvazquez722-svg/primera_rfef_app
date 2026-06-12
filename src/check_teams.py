
import pandas as pd

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

print(
    df["Equipo"]
    .value_counts()
    .sort_values(
        ascending=False
    )
)