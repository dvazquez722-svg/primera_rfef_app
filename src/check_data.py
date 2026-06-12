
import pandas as pd

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

print(
    df["Partido"]
    .dropna()
    .head(30)
    .tolist()
)