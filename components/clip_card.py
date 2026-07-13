import streamlit as st


def draw_clip_card(
    clip,
    opponent,
    staff_selected=False,
    players_selected=False
):
    """
    Dibuja una tarjeta de clip.

    Parameters
    ----------
    clip : dict
        Registro de la tabla clips.

    opponent : str
        Nombre del rival.

    staff_selected : bool
        Si el clip está seleccionado para Staff.

    players_selected : bool
        Si el clip está seleccionado para Jugadores.
    """

    with st.container(border=True):

        # ============================
        # MINIATURA
        # ============================

        if clip.get("thumbnail_url"):

            st.image(
                clip["thumbnail_url"],
                use_container_width=True
            )

        else:

            st.empty()

        # ============================
        # TÍTULO
        # ============================

        st.markdown(
            f"### 🎬 {clip['title']}"
        )

        # ============================
        # RIVAL Y CATEGORÍA
        # ============================

        c1, c2 = st.columns(2)

        with c1:

            st.caption(
                f"⚽ {opponent}"
            )

        with c2:

            st.caption(
                f"🏷 {clip['category']}"
            )

        # ============================
        # DESCRIPCIÓN
        # ============================

        description = clip.get(
            "description"
        )

        if description:

            st.write(
                description
            )

        # ============================
        # AUTOR / FECHA
        # ============================

        c1, c2 = st.columns(2)

        with c1:

            st.caption(
                f"👤 {clip.get('created_by_name','-')}"
            )

        with c2:

            created = clip.get(
                "created_at",
                ""
            )

            if created:

                st.caption(
                    f"📅 {created[:10]}"
                )

        # ============================
        # FAVORITO
        # ============================

        favorite = clip.get(
            "favorite",
            False
        )

        if favorite:

            st.markdown("⭐ Favorito")

        # ============================
        # SELECCIONES
        # ============================

        c1, c2 = st.columns(2)

        with c1:

            staff = st.checkbox(

                "Staff",

                value=staff_selected,

                key=f"staff_{clip['id']}"

            )

        with c2:

            players = st.checkbox(

                "Jugadores",

                value=players_selected,

                key=f"players_{clip['id']}"

            )

        # ============================
        # ACCIONES
        # ============================

        c1, c2, c3 = st.columns(3)

        with c1:

            view = st.button(

                "▶ Ver",

                key=f"view_{clip['id']}"

            )

        with c2:

            edit = st.button(

                "✏ Editar",

                key=f"edit_{clip['id']}"

            )

        with c3:

            delete = st.button(

                "🗑 Eliminar",

                key=f"delete_{clip['id']}"

            )

    return {

        "staff": staff,

        "players": players,

        "view": view,

        "edit": edit,

        "delete": delete

    }