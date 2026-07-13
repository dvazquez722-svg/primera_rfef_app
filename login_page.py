import streamlit as st

from auth import login, get_profile

st.title("Football Intelligence Platform")

email = st.text_input("Email")

password = st.text_input(
    "Contraseña",
    type="password"
)

if st.button("Iniciar Sesión"):

    response = login(
        email,
        password
    )

    if response:

        profile = get_profile(
            response.user.id
        )

        st.write("PROFILE:")
        st.write(profile)

        st.stop()

    else:

        st.error(
            "Credenciales incorrectas"
        )

if response:

    profile = get_profile(
        response.user.id
    )

    if profile is None:

        st.error(
            "Perfil no encontrado"
        )

        st.stop()

    st.session_state.user = {

        "id": response.user.id,

        "email": response.user.email,

        "full_name": profile["full_name"],

        "role": profile["role"],

        "team_id": profile["team_id"],

        "team_name": profile["team_name"]


    }

    st.success(
        "Login correcto"
    )

if "user" in st.session_state:

    st.success(
        f"Bienvenido {st.session_state.user['full_name']}"
    )

    st.write(
        f"Rol: {st.session_state.user['role']}"
    )