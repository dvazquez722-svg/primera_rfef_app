import pandas as pd
from pathlib import Path

# =====================================================
# RUTA DE DATOS
# =====================================================

DATA_PATH = Path("data/raw")

files = {
    "general": DATA_PATH / "Team Stats Arenas Club.xlsx",
    "ofensiva": DATA_PATH / "Team Stats Arenas Club Fase Ofensiva.xlsx",
    "defensiva": DATA_PATH / "Team Stats Arenas Club Fase Defensiva.xlsx",
    "organizacion": DATA_PATH / "Team Stats Arenas Club Organización.xlsx",
    "indices": DATA_PATH / "Team Stats Arenas Club Índices.xlsx",
}

# =====================================================
# INSPECCIÓN
# =====================================================

for name, file in files.items():

    print("\n")
    print("=" * 80)
    print(f"ARCHIVO: {name.upper()}")
    print("=" * 80)

    df = pd.read_excel(file)

    print(f"\nShape: {df.shape}")

    print("\nColumnas:")
    for col in df.columns:
        print(f" - {col}")

    print("\nPrimeras filas:")
    print(df.head())

    if "Equipo" in df.columns:
        print("\nEquipos encontrados:")
        print(df["Equipo"].dropna().unique())

    if "Fecha" in df.columns:
        print("\nFechas válidas:")
        print(df["Fecha"].notna().sum())

    print("\nValores nulos:")
    print(df.isna().sum().head(15))