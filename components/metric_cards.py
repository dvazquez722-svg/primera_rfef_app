import streamlit as st


def draw_metrics(metrics):

    """
    metrics = [
        ("📹", "Clips", 245),
        ("⚽", "Rivales", 18),
        ("⭐", "Favoritos", 42),
        ("🎓", "Staff", 17),
        ("👥", "Jugadores", 11)
    ]
    """

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        icon, title, value = metric

        with col:

            with st.container(border=True):

                st.markdown(
                    f"## {icon}"
                )

                st.caption(title)

                st.markdown(
                    f"# {value}"
                )