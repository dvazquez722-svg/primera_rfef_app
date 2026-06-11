import pandas as pd

df = pd.read_excel(
    "data/raw/Team Stats Arenas Club Organización.xlsx"
)

print(df.columns.tolist())