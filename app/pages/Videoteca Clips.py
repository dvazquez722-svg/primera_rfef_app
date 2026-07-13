import streamlit as st

from services.clips import (
    load_clips,
    create_clip,
    delete_clip
)

from services.reports import (
    load_reports,
    create_report
)

from services.selections import (
    load_selections,
    create_selection,
    delete_selection,
    selection_exists
)

from services.teams import (
    load_teams
)

from services.storage import (
    upload_video
)

from utils.clip_utils import (
    build_reports_dict,
    build_categories,
    build_opponents,
    filter_clips,
    selection_for_clip
)

from services.selections import (


    move_selection_up,

    move_selection_down

)

from auth import get_current_user

user = get_current_user()

if user is None:
    st.switch_page("Portada.py")
    st.stop()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Videoteca",

    page_icon="🎥",

    layout="wide"

)

# =====================================================
# USER
# =====================================================

if "user" not in st.session_state:

    st.error("Sesión no iniciada.")

    st.stop()

user = st.session_state.user

# =====================================================
# HEADER
# =====================================================

st.title("🎥 Video Analysis")

st.subheader("Videoteca")

st.caption(
    f"{user['team_name']} · {user['full_name']}"
)

st.divider()

# =====================================================
# LOAD DATA
# =====================================================

reports = load_reports(user["team_id"]) or []

clips = load_clips(user["team_id"]) or []

selections = load_selections(user["team_id"]) or []

teams = load_teams() or []

# =====================================================
# PREPARE DATA
# =====================================================

reports_dict = build_reports_dict(reports)

categories = build_categories(clips)

opponents = build_opponents(
    clips,
    reports_dict
)

# =====================================================
# METRICS
# =====================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Informes", len(reports))

with c2:
    st.metric("Clips", len(clips))

with c3:
    st.metric("Seleccionados", len(selections))

st.divider()

# =====================================================
# FILTER BAR
# =====================================================

c1, c2, c3, c4 = st.columns([1, 2, 2, 2])

with c1:

    upload_clicked = st.button(

        "➕ Subir clips",

        use_container_width=True

    )

with c2:

    search_text = st.text_input(

        "Buscar",

        placeholder="Título del clip..."

    )

with c3:

    selected_opponent = st.selectbox(

        "Rival",

        ["Todos"] + opponents

    )

with c4:

    selected_category = st.selectbox(

        "Categoría",

        ["Todas"] + categories

    )

st.divider()

# =====================================================
# FILTER CLIPS
# =====================================================

filtered_clips = filter_clips(

    clips=clips,

    reports_dict=reports_dict,

    search_text=search_text,

    opponent=selected_opponent,

    category=selected_category

)

st.metric(

    "Resultados",

    len(filtered_clips)

)

st.divider()

# =====================================================
# UPLOAD DIALOG
# =====================================================

@st.dialog("➕ Subir clips", width="large")
def upload_dialog():

    report_mode = st.radio(

        "Informe",

        [

            "Utilizar informe existente",

            "Crear nuevo informe"

        ]

    )

    report_id = None

    if report_mode == "Utilizar informe existente":

        report_options = {

            report["opponent"]: report["id"]

            for report in reports

        }

        selected_report = st.selectbox(

            "Informe",

            list(report_options.keys())

        )

        report_id = report_options[selected_report]

    else:

        opponents = sorted(

            [

                team["name"]

                for team in teams

                if team["id"] != user["team_id"]

            ]

        )

        opponent = st.selectbox(

            "Rival",

            opponents

        )

    category = st.selectbox(

        "Categoría",

        [

            "Salida de balón",

            "Presión alta",

            "Transiciones ofensivas",

            "Transiciones defensivas",

            "ABP ofensiva",

            "ABP defensiva"

        ]

    )

    description = st.text_area(

        "Descripción",

        placeholder="Objetivo táctico, correcciones, aspectos importantes..."

    ) 


    videos = st.file_uploader(

        "Vídeos",

        type=["mp4"],

        accept_multiple_files=True

    )

    if st.button(

        "⬆️ Subir",

        type="primary",

        use_container_width=True

    ):

        if report_mode == "Crear nuevo informe":

            report = create_report({

                "team_id": user["team_id"],

                "created_by": user["id"],

                "opponent": opponent

            })

            report_id = report[0]["id"]

        if not videos:

            st.error("Selecciona al menos un vídeo.")

            st.stop()

        for video in videos:

            video_url = upload_video(video)

            create_clip({

                "team_id": user["team_id"],

                "report_id": report_id,

                "created_by": user["id"],

                "title": video.name.replace(".mp4", ""),

                "category": category,

                "description": description,

                "video_url": video_url

            })

        st.success("Clips subidos correctamente.")

        st.rerun()


# =====================================================
# OPEN DIALOG
# =====================================================

if upload_clicked:

    upload_dialog()

# =====================================================
# CLIP GRID
# =====================================================

if not filtered_clips:

    st.info(
        "No hay clips para los filtros seleccionados."
    )

else:

    cols = st.columns(2)

    for index, clip in enumerate(filtered_clips):

        opponent = reports_dict.get(
            clip["report_id"],
            "Sin rival"
        )

        with cols[index % 2]:

            with st.container(border=True):

                # =====================================
                # HEADER
                # =====================================

                staff_selected = selection_exists(
                    clip["id"],
                    "Staff",
                    selections
                )

                players_selected = selection_exists(
                    clip["id"],
                    "Jugadores",
                    selections
                )

                if staff_selected and players_selected:

                    status = "🟣 Staff + Jugadores"

                elif staff_selected:

                    status = "🟢 Staff"

                elif players_selected:

                    status = "🔵 Jugadores"

                else:

                    status = "⚪ Sin seleccionar"

                st.caption(status)

                st.markdown(
                    f"### {clip['title']}"
                )

                info1, info2 = st.columns(2)

                with info1:

                    st.caption(
                        f"⚽ {opponent}"
                    )

                with info2:

                    st.caption(
                        f"🏷 {clip['category']}"
                    )

                st.divider()

                # =====================================
                # STAFF
                # =====================================

                row1, row2 = st.columns([5, 1])

                with row1:

                    staff = st.checkbox(

                        "📋 Staff",

                        value=staff_selected,

                        key=f"staff_{clip['id']}"

                    )

                with row2:

                    staff_selection = selection_for_clip(

                        clip["id"],

                        "Staff",

                        selections

                    )

                if staff != staff_selected:

                    if staff:

                        create_selection({

                            "team_id": user["team_id"],

                            "created_by": user["id"],

                            "clip_id": clip["id"],

                            "target": "Staff"

                        })

                    else:

                        delete_selection(

                            user["team_id"],

                            clip["id"],

                            "Staff"

                        )

                    st.rerun()

                st.divider()

 
                # =====================================
                # PLAYERS
                # =====================================

                row1, row2 = st.columns([5, 1])

                with row1:

                    players = st.checkbox(

                        "👥 Jugadores",

                        value=players_selected,

                        key=f"players_{clip['id']}"

                    )

                with row2:

                    players_selection = selection_for_clip(

                        clip["id"],

                        "Jugadores",

                        selections

                    )

                if players != players_selected:

                    if players:

                        create_selection({

                            "team_id": user["team_id"],

                            "created_by": user["id"],

                            "clip_id": clip["id"],

                            "target": "Jugadores"

                        })

                    else:

                        delete_selection(

                            user["team_id"],

                            clip["id"],

                            "Jugadores"

                        )

                    st.rerun()

                st.divider()

                # =====================================
                # ACTIONS
                # =====================================

                action1, action2 = st.columns([3, 1])

                with action1:

                    if st.button(

                        "▶ Reproducir",

                        key=f"view_{clip['id']}",

                        type="primary",

                        use_container_width=True

                    ):

                        st.session_state.selected_clip = clip

                        st.session_state.show_video = True

                        st.rerun()

                with action2:

                    if st.button(

                        "🗑",

                        key=f"delete_{clip['id']}",

                        use_container_width=True

                    ):

                        st.session_state.selected_clip = clip

                        st.session_state.show_delete = True

                        st.rerun()



                
# =====================================================
# VIDEO DIALOG
# =====================================================

@st.dialog("🎥 Clip", width="large")
def show_video_dialog():

    clip = st.session_state.selected_clip

    opponent = reports_dict.get(

        clip["report_id"],

        "Sin rival"

    )

    st.video(

        clip["video_url"]

    )

    st.markdown(

        f"### {clip['title']}"

    )

    st.caption(

        f"⚽ {opponent} · 🏷 {clip['category']}"

    )
    
    if clip.get("description"):

        st.info(

            clip["description"]

    )


    st.divider()

    staff_selected = selection_exists(

        clip["id"],

        "Staff",

        selections

    )

    players_selected = selection_exists(

        clip["id"],

        "Jugadores",

        selections

    )

    c1, c2 = st.columns(2)

    with c1:

        staff = st.checkbox(

            "Staff",

            value=staff_selected

        )

    with c2:

        players = st.checkbox(

            "Jugadores",

            value=players_selected

        )

    # -----------------------------------------
    # STAFF
    # -----------------------------------------

    if staff != staff_selected:

        if staff:

            create_selection({

                "team_id": user["team_id"],

                "created_by": user["id"],

                "clip_id": clip["id"],

                "target": "Staff"

            })

        else:

            delete_selection(

                user["team_id"],

                clip["id"],

                "Staff"

            )

        st.rerun()

    # -----------------------------------------
    # PLAYERS
    # -----------------------------------------

    if players != players_selected:

        if players:

            create_selection({

                "team_id": user["team_id"],

                "created_by": user["id"],

                "clip_id": clip["id"],

                "target": "Jugadores"

            })

        else:

            delete_selection(

                user["team_id"],

                clip["id"],

                "Jugadores"

            )

        st.rerun()


# =====================================================
# DELETE DIALOG
# =====================================================

@st.dialog("Eliminar clip")
def show_delete_dialog():

    clip = st.session_state.selected_clip

    st.warning(

        "¿Seguro que quieres eliminar este clip?"

    )

    if st.button(

        "Eliminar",

        type="primary",

        use_container_width=True

    ):

        delete_clip(

            clip["id"]

        )

        st.success(

            "Clip eliminado."

        )

        st.rerun()


# =====================================================
# OPEN DIALOGS
# =====================================================

if st.session_state.get(

    "show_video",

    False

):

    st.session_state.show_video = False

    show_video_dialog()

if st.session_state.get(

    "show_delete",

    False

):

    st.session_state.show_delete = False

    show_delete_dialog()

# =====================================================
# FINAL CLEANUP
# =====================================================

# Eliminar estados temporales vacíos

if "selected_clip" not in st.session_state:

    st.session_state.selected_clip = None

if "show_video" not in st.session_state:

    st.session_state.show_video = False

if "show_delete" not in st.session_state:

    st.session_state.show_delete = False


# =====================================================
# PAGE STYLE
# =====================================================

st.markdown(
    """
    <style>

    div[data-testid="stVerticalBlockBorderWrapper"]{
        border-radius:12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)