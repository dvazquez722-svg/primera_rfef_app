import pandas as pd

df = pd.read_csv(
    "data/processed/master_team_stats.csv"
)

pairs = [
    ("xG_x", "xG_y"),
    ("Tiros totales_x", "Tiros totales_y"),
    ("Tiros a portería_x", "Tiros a portería_y"),
    ("% tiros portería_x", "% tiros portería_y"),
]

for c1, c2 in pairs:

    equal = (df[c1] == df[c2]).all()

    print(
        f"{c1} vs {c2} --> {equal}"
    )