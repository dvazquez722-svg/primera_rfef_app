import streamlit as st

from services.clips import load_clips
from services.reports import load_reports
from services.selections import load_selections

from utils.clip_utils import (
    build_reports_dict
)

from pathlib import Path

import streamlit as st

from services.video_summary import (
    export_summary
)

from pathlib import Path

import streamlit as st

from services.video_edit_list import (
    generate_edit_list
)
# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Video Informes",

    page_icon="🎬",

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
# SESSION STATE
# =====================================================

defaults = {

    "presentation_mode": False,

    "playlist": [],

    "current_clip": 0,

    "selected_opponent": None,

    "video_summary_selection": set()

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# =====================================================
# LOAD DATA
# =====================================================

clips = load_clips(

    user["team_id"]

) or []

reports = load_reports(

    user["team_id"]

) or []

selections = load_selections(

    user["team_id"]

) or []

reports_dict = build_reports_dict(

    reports

)

# =====================================================
# HEADER
# =====================================================

st.title("🎬 Video Informes")

st.caption(

    f"{user['team_name']} · {user['full_name']}"

)

st.divider()

# =====================================================
# TARGET
# =====================================================

target = st.radio(

    "Destinatario",

    [

        "Staff",

        "Jugadores"

    ],

    horizontal=True

)

# =====================================================
# BUILD PLAYLISTS
# =====================================================

selected_ids = {

    item["clip_id"]

    for item in selections

    if item["target"] == target

}

selected_clips = [

    clip

    for clip in clips

    if clip["id"] in selected_ids

]

presentations = {}

for clip in selected_clips:

    opponent = reports_dict.get(

        clip["report_id"],

        "Sin rival"

    )

    presentations.setdefault(

        opponent,

        []

    ).append(

        clip

    )

if not presentations:

    st.info(

        "No existen clips para este destinatario."

    )

    st.stop()

# =====================================================
# HOME
# =====================================================

if not st.session_state.presentation_mode:

    opponent = st.selectbox(

        "Rival",

        sorted(

            presentations.keys()

        )

    )

    playlist = presentations[opponent]

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Clips",

            len(

                playlist

            )

        )

    with c2:

        st.metric(

            "Categorías",

            len(

                {

                    clip["category"]

                    for clip in playlist

                }

            )

        )

    st.divider()

    if st.button(

        "▶ Abrir presentación",

        type="primary",

        use_container_width=True

    ):

        st.session_state.playlist = playlist

        st.session_state.current_clip = 0

        st.session_state.selected_opponent = opponent

        st.session_state.presentation_mode = True

        st.session_state.video_summary_selection = set()

        st.rerun()

# =====================================================
# PLAYER
# =====================================================

else:

    playlist = st.session_state.playlist

    index = st.session_state.current_clip

    clip = playlist[index]

    opponent = st.session_state.selected_opponent

    top_left, top_right = st.columns(

        [1, 5]

    )

    with top_left:

        if st.button(

            "← Volver",

            use_container_width=True

        ):

            st.session_state.presentation_mode = False

            st.session_state.playlist = []

            st.session_state.current_clip = 0

            st.session_state.selected_opponent = None

            st.session_state.video_summary_selection = set()

            st.rerun()

    with top_right:

        st.title(

            opponent

        )

    st.divider()

    video_col, playlist_col = st.columns(

        [3, 1],

        gap="large"

    )

    # =================================================
    # VIDEO
    # =================================================

    with video_col:

        st.video(

            clip["video_url"]

        )

        st.subheader(

            clip["title"]

        )

        st.caption(

            f"🏷 {clip['category']}"

        )

        st.progress(

            (index + 1) /

            len(playlist)

        )

        st.caption(

            f"Clip {index + 1} de {len(playlist)}"

        )

        st.divider()

        prev_col, next_col = st.columns(2)

        with prev_col:

            if st.button(

                "◀ Anterior",

                disabled=index == 0,

                use_container_width=True

            ):

                st.session_state.current_clip -= 1

                st.rerun()

        with next_col:

            if st.button(

                "Siguiente ▶",

                disabled=index == len(playlist) - 1,

                use_container_width=True

            ):

                st.session_state.current_clip += 1

                st.rerun()

    # =================================================
    # PLAYLIST
    # =================================================

    with playlist_col:

        st.subheader(

            "Playlist"

        )

        st.caption(

            f"{len(playlist)} clips"

        )

        st.divider()

        selected = st.session_state.video_summary_selection

        for i, item in enumerate(playlist):

            current = i == index

            clip_id = item["id"]

            checked = clip_id in selected

            new_checked = st.checkbox(

                item["title"],

                value=checked,

                key=f"check_{clip_id}"

            )

            if new_checked:

                selected.add(

                    clip_id

                )

            else:

                selected.discard(

                    clip_id

                )

            if st.button(

                "▶ Ver clip",

                key=f"play_{clip_id}",

                use_container_width=True,

                type="primary" if current else "secondary"

            ):

                st.session_state.current_clip = i

                st.rerun()

            st.caption(

                item["category"]

            )

            st.divider()

    # =================================================
    # VIDEO SUMMARY
    # =================================================

    st.divider()

    total_selected = len(

        st.session_state.video_summary_selection

    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Clips seleccionados",

            total_selected

        )

    with c2:

        st.metric(

            "Clips totales",

            len(

                playlist

            )

        )

    st.write("")

    if st.button(

        "🎬 Generar vídeo resumen",

        type="primary",

        use_container_width=True,

        disabled=total_selected == 0

    ):

        summary_playlist = [

            clip

            for clip in playlist

            if clip["id"] in st.session_state.video_summary_selection

        ]

        st.session_state.summary_playlist = summary_playlist

        st.success(

            f"{len(summary_playlist)} clips preparados para exportar."

        )

    if (

        "summary_playlist" in st.session_state

        and

        len(

            st.session_state.summary_playlist

        ) > 0

    ):

        st.info(

            "La generación automática del MP4 se implementará en el siguiente paso."

        )

        st.write(

            "Clips incluidos:"

        )

        for clip in st.session_state.summary_playlist:

            st.write(

                f"• {clip['title']}"

            )

# =================================================
# EXPORTAR LISTA DE EDICIÓN
# =================================================

    st.divider()

    st.subheader(

        "📋 Lista de edición"

    )

    if (

        "summary_playlist" in st.session_state

        and

        len(

            st.session_state.summary_playlist

        ) > 0

    ):

        st.success(

            f"{len(st.session_state.summary_playlist)} clips preparados."

        )

        export_name = st.text_input(

            "Nombre del informe",

            value=f"{opponent}_Lista_Edicion"

        )

        if st.button(

            "📋 Generar Lista de Edición",

            use_container_width=True,

            type="primary"

        ):

            output = generate_edit_list(

                clips=st.session_state.summary_playlist,

                output_folder="exports",

                filename=export_name,

                opponent=opponent

            )

            st.success(

                "Lista generada correctamente."

            )

            with open(

                output,

                "rb"

            ) as file:

                st.download_button(

                    "📥 Descargar Excel",

                    data=file,

                    file_name=Path(output).name,

                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    use_container_width=True

                )

    else:

        st.info(

            "Selecciona uno o más clips para generar la lista de edición."

        )