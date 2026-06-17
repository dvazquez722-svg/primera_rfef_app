import streamlit as st
import pandas as pd
import os

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Scouting Individual",
    page_icon="👤",
    layout="wide"
)

DATA_PATH = "data/Jugadores"
VIDEOS_PATH = "videos"

st.markdown("""
<style>

.block-container{
    max-width:1600px;
    padding-top:1rem;
}

.main-card{

    background:linear-gradient(
        135deg,
        #071329,
        #10284d
    );

    padding:30px;

    border-radius:20px;

    margin-bottom:20px;

}

.info-card{

    background:#071329;

    padding:20px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,0.08);

}

.label{

    color:#8FB8FF;

    font-size:12px;

    letter-spacing:2px;

    text-transform:uppercase;

}

</style>
""",
unsafe_allow_html=True)


# =====================================================
# FUNCTIONS
# =====================================================

def get_teams():

    return sorted(

        [

            folder

            for folder in os.listdir(DATA_PATH)

            if os.path.isdir(
                os.path.join(
                    DATA_PATH,
                    folder
                )
            )

        ]

    )


def get_players(team):

    team_folder = os.path.join(
        DATA_PATH,
        team
    )

    return sorted(

        [

            file

            for file in os.listdir(team_folder)

            if file.endswith(".xlsx")

        ]

    )


def load_player(team, player_file):

    path = os.path.join(
        DATA_PATH,
        team,
        player_file
    )

    return pd.read_excel(path)


# =====================================================
# SELECTORS
# =====================================================

teams = get_teams()

team = st.selectbox(
    "Equipo",
    teams
)

players = get_players(team)

player_file = st.selectbox(
    "Jugador",
    players
)

player_name = (
    player_file
    .replace(".xlsx", "")
    .replace("_", " ")
)

# =====================================================
# SESSION
# =====================================================

if "selected_folder" not in st.session_state:

    st.session_state.selected_folder = None

if "player_clips" not in st.session_state:

    st.session_state.player_clips = []

if "staff_clips" not in st.session_state:

    st.session_state.staff_clips = []

# =====================================================
# LOAD DATA
# =====================================================

player_df = load_player(
    team,
    player_file
)

minutes = player_df[
    "Minutos jugados"
].sum()

minutes_factor = minutes / 90

goals = player_df[
    "Goles"
].sum()

assists = player_df[
    "Asistencias"
].sum()

xg = pd.to_numeric(

    player_df["xG"]

    .astype(str)

    .str.replace(",", "."),

    errors="coerce"

).sum()

# =====================================================
# POSITION GROUPS
# =====================================================

ROLE_MAP = {

    "CF": "Delantero",

    "LW": "Extremo",
    "RW": "Extremo",
    "LWF": "Extremo",
    "RWF": "Extremo",

    "AMF": "Mediapunta",

    "DMF": "Mediocentro",
    "CMF": "Mediocentro",
    "LCMF": "Mediocentro",
    "RCMF": "Mediocentro",

    "CB": "Defensa",
    "LB": "Defensa",
    "RB": "Defensa",
    "LWB": "Defensa",
    "RWB": "Defensa"
}

def per90(series, minutes):

    if minutes == 0:

        return 0

    return round(

        series.sum()

        /

        (minutes / 90),

        2

    )

main_position = (

    player_df[
        "Posición específica"
    ]

    .mode()

    .iloc[0]

)

role = ROLE_MAP.get(
    main_position,
    "Mediocentro"
)


# =====================================================
# POSITION KPIS
# =====================================================

if role == "Delantero":

    kpis = {

        "🎯 Tiros":

        per90(

            player_df[
                "Tiros a portería"
            ],

            minutes

        ),

        "⚽ Goles":

        goals,

        "📈 xG":

        round(xg,2),

        "🛡️ Juego Aéreo":

        per90(

            player_df[
                "Duelos aéreos ganados"
            ],

            minutes

        )

    }

elif role == "Extremo":

    kpis = {

        "🔥 Regates":

        per90(

            player_df[
                "Regates logrados"
            ],

            minutes

        ),

        "🎯 Centros":

        per90(

            player_df[
                "Centros lanzados"
            ],

            minutes

        ),

        "⚽ Asistencias":

        assists,

        "🎯 Tiros":

        per90(

            player_df[
                "Tiros a portería"
            ],

            minutes

        )

    }

elif role == "Mediapunta":

    kpis = {

        "⚽ Asistencias":

        assists,

        "🎯 Pases":

        per90(

            player_df[
                "Pases logrados"
            ],

            minutes

        ),

        "🔥 Regates":

        per90(

            player_df[
                "Regates logrados"
            ],

            minutes

        ),

        "📈 xG":

        round(xg,2)

    }

elif role == "Mediocentro":

    kpis = {

        "🎯 Pases":

        per90(

            player_df[
                "Pases logrados"
            ],

            minutes

        ),

        "🛡️ Recuperaciones":

        per90(

            player_df[
                "Balones recuperados totales"
            ],

            minutes

        ),

        "✂️ Interceptaciones":

        per90(

            player_df[
                "Interceptaciones"
            ],

            minutes

        ),

        "⚔️ Duelos":

        per90(

            player_df[
                "Duelos ganados"
            ],

            minutes

        )

    }

else:

    kpis = {

        "⚔️ Duelos":

        per90(

            player_df[
                "Duelos ganados"
            ],

            minutes

        ),

        "🛡️ Juego Aéreo":

        per90(

            player_df[
                "Duelos aéreos ganados"
            ],

            minutes

        ),

        "✂️ Interceptaciones":

        per90(

            player_df[
                "Interceptaciones"
            ],

            minutes

        ),

        "🔄 Recuperaciones":

        per90(

            player_df[
                "Balones recuperados totales"
            ],

            minutes

        )

    }

# =====================================================
# HERO
# =====================================================

c1,c2 = st.columns([2,1])

with c1:

    st.markdown(f"""
    <div class="main-card">

    <div class="label">
    SCOUTING INDIVIDUAL
    </div>

    <h1 style="color:white;">
    👤 {player_name}
    </h1>

    <p style="
    color:#C9D4E3;
    font-size:18px;
    ">

    {team}

    </p>

    </div>
    """,
    unsafe_allow_html=True)

with c2:

    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "⏱️ Minutos",
            int(minutes)
        )

    with m2:

        st.metric(
            "🏟️ Partidos",
            len(player_df)
        )

# =====================================================
# KPIs
# =====================================================


cols = st.columns(4)

for col, (label, value) in zip(
    cols,
    kpis.items()
):

    with col:

        st.metric(
            label,
            round(value,1)
            if isinstance(
                value,
                float
            )
            else value
        )

# =====================================================
# VIDEO
# =====================================================

st.markdown(
    "## 🎥 Vídeo"
)

c1,c2 = st.columns(2)

with c1:

    st.markdown("""
    <div class="info-card">

    <h3 style="color:white;">
    🎯 Características Principales
    </h3>

    <p style="color:#C9D4E3;">
    Acciones que definen el perfil del jugador.
    </p>

    </div>
    """,
    unsafe_allow_html=True)

    if st.button(
    "▶ Ver Clips",
    use_container_width=True,
    key="traits"
):

        st.session_state.selected_folder = (
        "Caracteristicas"
    )

with c2:

    st.markdown("""
    <div class="info-card">

    <h3 style="color:white;">
    🔥 Acciones Destacadas
    </h3>

    <p style="color:#C9D4E3;">
    Acciones determinantes y de impacto.
    </p>

    </div>
    """,
    unsafe_allow_html=True)

    if st.button(
    "▶ Ver Clips",
    use_container_width=True,
    key="highlights"
):

        st.session_state.selected_folder = (
        "Destacadas"
    )
        
# =====================================================
# VISUALIZADOR
# =====================================================

st.markdown("---")

st.markdown(
    "## 🎥 Visualizador"
)

if st.session_state.selected_folder:

    player_folder = os.path.join(

        VIDEOS_PATH,

        team,

        "Jugadores",

        player_file.replace(
            ".xlsx",
            ""
        ),

        st.session_state.selected_folder
    )

    if os.path.exists(player_folder):

        videos = sorted(

            [

                file

                for file in os.listdir(player_folder)

                if file.endswith(".mp4")

            ]

        )

        if len(videos) > 0:

            col1, col2 = st.columns(2)

            for idx, video in enumerate(videos):

                video_path = os.path.join(
                    player_folder,
                    video
                )

                current_col = (
                    col1
                    if idx % 2 == 0
                    else col2
                )

                with current_col:

                    st.markdown(
                        f"**{video}**"
                    )

                    st.video(
                        video_path
                    )

                    c1, c2 = st.columns(2)

                    with c1:

                        player_selected = st.checkbox(

                            "👥 Jugadores",

                            value=(

                                video_path
                                in
                                st.session_state.player_clips

                            ),

                            key=f"player_{video_path}"

                        )

                    with c2:

                        staff_selected = st.checkbox(

                            "🎓 Staff",

                            value=(

                                video_path
                                in
                                st.session_state.staff_clips

                            ),

                            key=f"staff_{video_path}"

                        )

                    # =========================
                    # JUGADORES
                    # =========================

                    if player_selected:

                        if (

                            video_path
                            not in
                            st.session_state.player_clips

                        ):

                            st.session_state.player_clips.append(
                                video_path
                            )

                    else:

                        if (

                            video_path
                            in
                            st.session_state.player_clips

                        ):

                            st.session_state.player_clips.remove(
                                video_path
                            )

                    # =========================
                    # STAFF
                    # =========================

                    if staff_selected:

                        if (

                            video_path
                            not in
                            st.session_state.staff_clips

                        ):

                            st.session_state.staff_clips.append(
                                video_path
                            )

                    else:

                        if (

                            video_path
                            in
                            st.session_state.staff_clips

                        ):

                            st.session_state.staff_clips.remove(
                                video_path
                            )

        else:

            st.warning(
                "No hay clips disponibles."
            )

    else:

        st.error(
            "La carpeta no existe."
        )

st.markdown("---")

c1, c2 = st.columns(2)

with c1:

    st.metric(

        "👥 Clips Jugadores",

        len(
            st.session_state.player_clips
        )

    )

with c2:

    st.metric(

        "🎓 Clips Staff",

        len(
            st.session_state.staff_clips
        )

    )