import pandas as pd
from pathlib import Path

# =====================================================
# CONFIG
# =====================================================

RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed")

FILES = {
    "general": RAW_PATH / "Team Stats Arenas Club.xlsx",
    "ofensiva": RAW_PATH / "Team Stats Arenas Club Fase Ofensiva.xlsx",
    "defensiva": RAW_PATH / "Team Stats Arenas Club Fase Defensiva.xlsx",
    "organizacion": RAW_PATH / "Team Stats Arenas Club Organización.xlsx",
    "indices": RAW_PATH / "Team Stats Arenas Club Índices.xlsx",
}

KEYS = ["Fecha", "Equipo"]

# =====================================================
# CLEAN FUNCTION
# =====================================================

def clean_team_file(file_path):

    df = pd.read_excel(file_path)

    # rellenar información de partido
    cols_to_fill = [
        "Fecha",
        "Partido",
        "Competición",
        "Duración"
    ]

    existing_cols = [
        c for c in cols_to_fill
        if c in df.columns
    ]

    df[existing_cols] = df[existing_cols].ffill()

    # convertir fecha
    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    )

    # eliminar filas resumen
    df = df[
        df["Fecha"].notna()
    ].copy()

    # reset index
    df.reset_index(
        drop=True,
        inplace=True
    )

    return df

# =====================================================
# LOAD & CLEAN
# =====================================================

general = clean_team_file(FILES["general"])
ofensiva = clean_team_file(FILES["ofensiva"])
defensiva = clean_team_file(FILES["defensiva"])
organizacion = clean_team_file(FILES["organizacion"])
indices = clean_team_file(FILES["indices"])

# =====================================================
# REMOVE DUPLICATED COLUMNS
# =====================================================

base_cols = [
    "Fecha",
    "Equipo",
    "Partido",
    "Competición",
    "Duración",
    "Seleccionar esquema"
]

ofensiva = ofensiva.drop(
    columns=[
        c for c in base_cols
        if c in ofensiva.columns
    ],
    errors="ignore"
)

defensiva = defensiva.drop(
    columns=[
        c for c in base_cols
        if c in defensiva.columns
    ],
    errors="ignore"
)

organizacion = organizacion.drop(
    columns=[
        c for c in base_cols
        if c in organizacion.columns
    ],
    errors="ignore"
)

indices = indices.drop(
    columns=[
        c for c in base_cols
        if c in indices.columns
    ],
    errors="ignore"
)

# =====================================================
# MERGE
# =====================================================

master = general.merge(
    ofensiva,
    left_index=True,
    right_index=True,
    how="left"
)

master = master.merge(
    defensiva,
    left_index=True,
    right_index=True,
    how="left"
)

master = master.merge(
    organizacion,
    left_index=True,
    right_index=True,
    how="left"
)

master = master.merge(
    indices,
    left_index=True,
    right_index=True,
    how="left"
)

# =====================================================
# QUALITY CHECKS
# =====================================================

print("\nMASTER DATASET")
print("=" * 50)

print("Shape:")
print(master.shape)

print("\nDuplicados Fecha+Equipo:")
print(
    master.duplicated(
        subset=["Fecha", "Equipo"]
    ).sum()
)

print("\nNulos:")
print(
    master.isna()
          .sum()
          .sort_values(
              ascending=False
          )
          .head(20)
)

# =====================================================
# REMOVE DUPLICATES
# =====================================================

master = master.drop(
    columns=[
        "xG_y",
        "Tiros totales_y",
        "Tiros a portería_y",
        "% tiros portería_y",
        "Pases logrados_y"
    ],
    errors="ignore"
)

master = master.rename(
    columns={
        "xG_x": "xG",
        "Tiros totales_x": "Tiros totales",
        "Tiros a portería_x": "Tiros a portería",
        "% tiros portería_x": "% tiros portería",
        "Pases logrados_x": "Pases logrados"
    }
)

# =====================================================
# SAVE
# =====================================================

OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)

master.to_csv(
    OUTPUT_PATH / "master_team_stats.csv",
    index=False
)

print(
    "\nArchivo guardado:"
)

print(
    OUTPUT_PATH / "master_team_stats.csv"
)