import pandas as pd
from pathlib import Path

# =====================================================
# CONFIG
# =====================================================

FILE_PATH = Path(
    "data/raw/Team Stats Arenas Club.xlsx"
)

# =====================================================
# LOAD
# =====================================================

df = pd.read_excel(FILE_PATH)

print("\nShape original:")
print(df.shape)

# =====================================================
# FILL FORWARD
# =====================================================

cols_to_fill = [
    "Fecha",
    "Partido",
    "Competición",
    "Duración"
]

df[cols_to_fill] = df[cols_to_fill].ffill()

# =====================================================
# REMOVE SUMMARY ROWS
# =====================================================

df = df[
    pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    ).notna()
].copy()

# =====================================================
# FORMAT DATE
# =====================================================

df["Fecha"] = pd.to_datetime(
    df["Fecha"]
)

# =====================================================
# SORT
# =====================================================

df = df.sort_values(
    by=["Fecha", "Equipo"]
)

# =====================================================
# RESET INDEX
# =====================================================

df = df.reset_index(drop=True)

# =====================================================
# CHECKS
# =====================================================

print("\nShape limpio:")
print(df.shape)

print("\nPrimeras filas:")
print(
    df[
        ["Fecha", "Equipo"]
    ].head(10)
)

print("\nÚltimas filas:")
print(
    df[
        ["Fecha", "Equipo"]
    ].tail(10)
)

print("\nNulos por columna:")
print(
    df.isna()
      .sum()
      .sort_values(
          ascending=False
      )
      .head(20)
)

print("\nDuplicados Fecha+Equipo:")
print(
    df.duplicated(
        subset=["Fecha", "Equipo"]
    ).sum()
)

# =====================================================
# SAVE
# =====================================================

output_path = Path(
    "data/processed/general_clean.csv"
)

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    output_path,
    index=False
)

print(
    f"\nArchivo guardado en: {output_path}"
)