import streamlit as st
import os 
import json
# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Video Análisis",
    page_icon="🎬",
    layout="wide"
)

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

.block-container{
    max-width:1600px;
    padding-top:1rem;
}

.hero-card{

    background:linear-gradient(
        135deg,
        #071329,
        #10284d
    );

    padding:35px;

    border-radius:22px;

    border:1px solid rgba(255,255,255,0.08);

    margin-bottom:20px;

}

.module-card{

    background:#071329;

    padding:20px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,0.08);

    text-align:center;

    min-height:120px;

}

.section-title{

    font-size:28px;

    font-weight:700;

    margin-top:20px;

    margin-bottom:20px;

}

</style>
""",
unsafe_allow_html=True)


# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero-card">

<h1 style="
color:white;
margin-bottom:10px;
">

🎬 Video Análisis

</h1>

<p style="
color:white;
font-size:50px;
">

Biblioteca táctica organizada por comportamientos de juego.

</p>

</div>
""",
unsafe_allow_html=True)

# =====================================================
# EQUIPOS
# =====================================================

VIDEOS_PATH = "videos"

teams = sorted(

    [

        folder

        for folder in os.listdir(VIDEOS_PATH)

        if os.path.isdir(
            os.path.join(
                VIDEOS_PATH,
                folder
            )
        )

    ]

)

FAVORITES_FILE = "selected_clips.json"

team = st.selectbox(
    "Seleccionar Equipo",
    teams
)

# =====================================================
# FUNCTIONS
# =====================================================

def load_selected_clips():

    if os.path.exists(FAVORITES_FILE):

        with open(
            FAVORITES_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return []


def save_selected_clips(clips):

    with open(
        FAVORITES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            clips,
            f,
            ensure_ascii=False,
            indent=4
        )


def count_clips(team_name):

    total = 0

    team_folder = os.path.join(
        VIDEOS_PATH,
        team_name
    )

    if not os.path.exists(team_folder):

        return 0

    for category in os.listdir(team_folder):

        category_path = os.path.join(
            team_folder,
            category
        )

        if os.path.isdir(category_path):

            total += len(

                [

                    file

                    for file in os.listdir(category_path)

                    if file.endswith(".mp4")

                ]

            )

    return total


def category_count(team_name, category):

    folder = os.path.join(

        VIDEOS_PATH,

        team_name,

        category

    )

    if not os.path.exists(folder):

        return 0

    return len(

        [

            file

            for file in os.listdir(folder)

            if file.endswith(".mp4")

        ]

    )


def open_category(category):

    st.session_state.selected_category = category

# =====================================================
# SESSION
# =====================================================

if "selected_category" not in st.session_state:

    st.session_state.selected_category = None


if "selected_clips" not in st.session_state:

    st.session_state.selected_clips = (
        load_selected_clips()
    )

if "player_clips" not in st.session_state:

    st.session_state.player_clips = []

if "staff_clips" not in st.session_state:

    st.session_state.staff_clips = []

# =====================================================
# RESUMEN
# =====================================================

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(
        "Equipo",
        team
    )

with c2:

    st.metric(
        "Clips",
        count_clips(team)
    )

with c3:

    st.metric(
        "Categorías",
        len(

            [

                folder

                for folder in os.listdir(
                    os.path.join(
                        VIDEOS_PATH,
                        team
                    )
                )

                if os.path.isdir(
                    os.path.join(
                        VIDEOS_PATH,
                        team,
                        folder
                    )
                )

            ]

        )
    )

# =====================================================
# CATEGORÍAS
# =====================================================

categories = {

    "Construccion": {
        "emoji":"🏗️",
        "title":"Construcción",
        "desc":"Salida de balón"
    },

    "Progresion": {
        "emoji":"🔄",
        "title":"Progresión",
        "desc":"Avance y circulación"
    },

    "Finalizacion": {
        "emoji":"🎯",
        "title":"Finalización",
        "desc":"Último tercio"
    },

    "Juego_Exterior": {
        "emoji":"🌐",
        "title":"Juego Exterior",
        "desc":"Centros y amplitud"
    },

    "Presion_Alta": {
        "emoji":"🔥",
        "title":"Presión Alta",
        "desc":"Presión tras pérdida"
    },

    "Bloque_Medio": {
        "emoji":"⚖️",
        "title":"Bloque Medio",
        "desc":"Organización colectiva"
    },

    "Bloque_Bajo": {
        "emoji":"🧱",
        "title":"Bloque Bajo",
        "desc":"Defensa del área"
    },

    "Transicion_Ofensiva": {
        "emoji":"🚀",
        "title":"Transición Ofensiva",
        "desc":"Ataques rápidos"
    },

    "Transicion_Defensiva": {
        "emoji":"🔄",
        "title":"Transición Defensiva",
        "desc":"Repliegue y balance"
    },

    "Corner_OF": {
        "emoji":"↗️",
        "title":"Corner OF",
        "desc":"Corners ofensivos"
    },

    "Corner_DEF": {
        "emoji":"↘️",
        "title":"Corner DEF",
        "desc":"Corners defensivos"
    },

    "Faltas_Laterales": {
        "emoji":"📐",
        "title":"Faltas Laterales",
        "desc":"ABP lateral"
    },

    "Faltas_Frontales": {
        "emoji":"🎯",
        "title":"Faltas Frontales",
        "desc":"ABP frontal"
    },

    "Acciones_Especiales": {
        "emoji":"🧩",
        "title":"Acciones Especiales",
        "desc":"Saques de banda y patrones"
    }

}

# =====================================================
# TARJETAS
# =====================================================

st.markdown("## 🎬 Biblioteca de Clips")

cols = st.columns(4)

for idx, (folder, info) in enumerate(categories.items()):

    with cols[idx % 4]:

        clips = category_count(
            team,
            folder
        )

        st.markdown(
            f"""
            <div class="module-card">

            <h3 style="color:white;">
            {info['emoji']} {info['title']}
            </h3>

            <p style="color:#C9D4E3;">
            {info['desc']}
            </p>

            <p style="
            color:#8FB8FF;
            font-weight:700;
            ">
            {clips} clips
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "▶ Ver Clips",
            key=f"btn_{folder}",
            use_container_width=True
        ):
            open_category(folder)

# =====================================================
# VISUALIZADOR
# =====================================================

st.markdown("---")

st.markdown(
    "## 🎥 Visualizador"
)

if st.session_state.selected_category:

    category_folder = os.path.join(

        VIDEOS_PATH,

        team,

        st.session_state.selected_category

    )

    st.subheader(
        st.session_state.selected_category
    )

    if os.path.exists(category_folder):

        videos = sorted(

            [

                file

                for file in os.listdir(category_folder)

                if file.endswith(".mp4")

            ]

        )

        if len(videos) == 0:

            st.warning(
                "No hay clips disponibles."
            )

        else:

            col1, col2 = st.columns(2)

            for idx, video in enumerate(videos):

                video_path = os.path.join(
                    category_folder,
                    video
                )

                current_col = (
                    col1
                    if idx % 2 == 0
                    else col2
                )

                with current_col:

                    st.markdown(
                        f"### {video}"
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

    else:

        st.error(
            "La carpeta no existe."
        )



# =====================================================
# PRESENTACIÓN JUGADORES
# =====================================================

st.markdown("---")

st.markdown(
    "## 📌 Presentación Jugadores"
)

selected = (
    st.session_state.selected_clips
)

if len(selected) == 0:

    st.info(
        "No hay clips seleccionados."
    )

else:

    st.success(
        f"{len(selected)} clips seleccionados"
    )

    col1, col2 = st.columns(2)

    for idx, clip in enumerate(selected):

        current_col = (
            col1
            if idx % 2 == 0
            else col2
        )

        with current_col:

            st.markdown(
                f"**{os.path.basename(clip)}**"
            )

            st.video(
                clip
            )

