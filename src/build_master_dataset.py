import pandas as pd
from pathlib import Path
import re

# =====================================================
# PATHS
# =====================================================

RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed")

import re

# =====================================================
# MATCH CONTEXT
# =====================================================

def parse_match(row):

    match = str(row["Partido"])
    team = row["Equipo"]

    try:

        match_clean = match.split("(")[0].strip()

        teams_part = re.split(
            r"\d+:\d+",
            match_clean
        )[0].strip()

        score = re.search(
            r"(\d+):(\d+)",
            match_clean
        )

        local_team = (
            teams_part.split(" - ")[0]
            .strip()
        )

        away_team = (
            teams_part.split(" - ")[1]
            .strip()
        )

        local_goals = int(
            score.group(1)
        )

        away_goals = int(
            score.group(2)
        )

    except:

        return pd.Series(
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None
            ]
        )

    # ==============================
    # LOCAL / VISITANTE
    # ==============================

    if team == local_team:

        rival = away_team
        venue = "Local"

        goals_for = local_goals
        goals_against = away_goals

    elif team == away_team:

        rival = local_team
        venue = "Visitante"

        goals_for = away_goals
        goals_against = local_goals

    else:

        rival = None
        venue = None

        goals_for = None
        goals_against = None

    # ==============================
    # RESULTADO
    # ==============================

    if goals_for is None:

        result = None
        points = None

    elif goals_for > goals_against:

        result = "Victoria"
        points = 3

    elif goals_for == goals_against:

        result = "Empate"
        points = 1

    else:

        result = "Derrota"
        points = 0

    goal_diff = (
        goals_for - goals_against
        if goals_for is not None
        else None
    )

    return pd.Series(
        [
            rival,
            venue,
            result,
            points,
            goal_diff,
            goals_for,
            goals_against
        ]
    )

# =====================================================
# CLEAN FUNCTION
# =====================================================

def clean_team_file(file_path):

    df = pd.read_excel(file_path)

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

    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        errors="coerce"
    )

    df = df[
        df["Fecha"].notna()
    ].copy()

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df

# =====================================================
# DETECT TEAMS
# =====================================================

files = list(
    RAW_PATH.glob("*.xlsx")
)

teams = set()

for file in files:

    name = file.stem

    name = name.replace(
        "Team Stats ",
        ""
    )

    name = re.sub(
        r" Fase Defensiva$",
        "",
        name
    )

    name = re.sub(
        r" Fase Ofensiva$",
        "",
        name
    )

    name = re.sub(
        r" Organización$",
        "",
        name
    )

    name = re.sub(
        r" Índices$",
        "",
        name
    )

    teams.add(name)

teams = sorted(
    list(teams)
)

print("\nEquipos encontrados:")
print(len(teams))

for t in teams:
    print("-", t)

# =====================================================
# BUILD MASTER
# =====================================================

all_teams = []

for team in teams:

    print(f"\nProcesando: {team}")

    try:

        general = clean_team_file(
            RAW_PATH / f"Team Stats {team}.xlsx"
        )

        ofensiva = clean_team_file(
            RAW_PATH / f"Team Stats {team} Fase Ofensiva.xlsx"
        )

        defensiva = clean_team_file(
            RAW_PATH / f"Team Stats {team} Fase Defensiva.xlsx"
        )

        organizacion = clean_team_file(
            RAW_PATH / f"Team Stats {team} Organización.xlsx"
        )

        indices = clean_team_file(
            RAW_PATH / f"Team Stats {team} Índices.xlsx"
        )

        base_cols = [
            "Fecha",
            "Partido",
            "Competición",
            "Duración",
            "Equipo",
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

        team_df = general.copy()

        team_df = team_df.merge(
            ofensiva,
            left_index=True,
            right_index=True,
            how="left"
        )

        team_df = team_df.merge(
            defensiva,
            left_index=True,
            right_index=True,
            how="left"
        )

        team_df = team_df.merge(
            organizacion,
            left_index=True,
            right_index=True,
            how="left"
        )

        team_df = team_df.merge(
            indices,
            left_index=True,
            right_index=True,
            how="left"
        )

        # ==========================================
        # REMOVE DUPLICATE COLUMNS
        # ==========================================

        duplicate_map = {
            "xG_x": "xG",
            "Tiros totales_x": "Tiros totales",
            "Tiros a portería_x": "Tiros a portería",
            "% tiros portería_x": "% tiros portería",
            "Pases logrados_x": "Pases logrados"
        }

        team_df = team_df.rename(
            columns=duplicate_map
        )

        cols_to_drop = [
            "xG_y",
            "Tiros totales_y",
            "Tiros a portería_y",
            "% tiros portería_y",
            "Pases logrados_y"
        ]

        team_df = team_df.drop(
            columns=cols_to_drop,
            errors="ignore"
        )

        all_teams.append(
            team_df
        )

        print(
            f"OK -> {len(team_df)} filas"
        )

    except Exception as e:

        print(
            f"ERROR en {team}"
        )

        print(e)

# =====================================================
# CONCAT ALL TEAMS
# =====================================================

master = pd.concat(
    all_teams,
    ignore_index=True
)

# =====================================================
# SORT
# =====================================================

master = master.sort_values(
    ["Fecha", "Equipo"]
)

master.reset_index(
    drop=True,
    inplace=True
)

# =====================================================
# FILTER GROUP 1
# =====================================================

GROUP_1_TEAMS = [
    "Arenas Club",
    "Arenteiro",
    "Athletic Bilbao",
    "Barakaldo",
    "Cacereño",
    "Celta Fortuna",
    "Guadalajara",
    "Lugo",
    "Mérida AD",
    "Osasuna Promesas",
    "Ourense CF",
    "Ponferradina",
    "Pontevedra",
    "Racing Ferrol",
    "Real Avilés",
    "Real Madrid Castilla",
    "Talavera CF",
    "Tenerife",
    "Unionistas de Salamanca",
    "Zamora"
]

master = master[
    master["Equipo"].isin(GROUP_1_TEAMS)
].copy()

# =====================================================
# FILTER REGULAR LEAGUE
# =====================================================

print("\nCompeticiones encontradas:")
print(
    master["Competición"]
    .value_counts(dropna=False)
)

master = master[
    master["Competición"]
    .astype(str)
    .str.contains(
        "Primera Division RFEF",
        case=False,
        na=False
    )
].copy()

print("\nTras filtrar Primera RFEF:")
print(master.shape)


master[
    [
        "Rival",
        "Condicion",
        "Resultado",
        "Puntos",
        "Diferencia_Goles",
        "GF",
        "GC"
    ]
] = master.apply(
    parse_match,
    axis=1
)

# =====================================================
# REMOVE DUPLICATES
# =====================================================

print("\nDuplicados antes:")

print(
    master[
        ["Equipo", "Partido"]
    ]
    .duplicated()
    .sum()
)

master = master.drop_duplicates(
    subset=[
        "Equipo",
        "Partido"
    ]
)

print("\nDuplicados después:")

print(
    master[
        ["Equipo", "Partido"]
    ]
    .duplicated()
    .sum()
)

print("\nShape final:")

print(master.shape)

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

# =====================================================
# REPORT
# =====================================================

print("\n")
print("=" * 60)

print("MASTER DATASET")

print("=" * 60)

print(
    f"Shape: {master.shape}"
)

print(
    f"Equipos: {master['Equipo'].nunique()}"
)

print(
    f"Partidos-equipo: {len(master)}"
)

print(
    f"Columnas: {len(master.columns)}"
)

print("\nArchivo guardado:")

print(
    OUTPUT_PATH / "master_team_stats.csv"
)

print(
    master[
        [
            "Equipo",
            "Rival",
            "Condicion",
            "Resultado",
            "Puntos",
            "GF",
            "GC"
        ]
    ].head(20)
)
print(master.shape)

print(
    master[
        ["Equipo", "Partido"]
    ].duplicated().sum()
)
print(
    master[
        ["Equipo", "Partido"]
    ]
    .value_counts()
    .head(20)
)