import streamlit as st


def draw_filter_bar(

    opponents,

    categories,

    tags=None,

    show_favorites=True,

    show_search=True

):

    c1, c2, c3, c4, c5 = st.columns(
        [2,2,2,1.2,2]
    )

    with c1:

        selected_opponent = st.selectbox(

            "⚽ Rival",

            ["Todos"] + sorted(opponents),

            key="filter_opponent"

        )

    with c2:

        selected_category = st.selectbox(

            "🏷 Categoría",

            ["Todas"] + sorted(categories),

            key="filter_category"

        )

    with c3:

        if tags:

            selected_tag = st.selectbox(

                "🏷 Etiqueta",

                ["Todas"] + sorted(tags),

                key="filter_tag"

            )

        else:

            selected_tag = "Todas"

    with c4:

        if show_favorites:

            favorites_only = st.toggle(

                "⭐",

                key="favorites"

            )

        else:

            favorites_only = False

    with c5:

        if show_search:

            search = st.text_input(

                "🔍 Buscar",

                placeholder="Título, descripción...",

                key="search"

            )

        else:

            search = ""

    return {

        "opponent": selected_opponent,

        "category": selected_category,

        "tag": selected_tag,

        "favorites": favorites_only,

        "search": search

    }