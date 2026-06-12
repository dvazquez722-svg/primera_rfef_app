# src/check_master.py

import pandas as pd

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

print(
    sorted(
        df["Equipo"]
        .dropna()
        .unique()
    )
)