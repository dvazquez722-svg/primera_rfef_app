import streamlit as st

from config import supabase

st.title("Login Test")

email = st.text_input("Email")
password = st.text_input(
    "Password",
    type="password"
)

if st.button("Iniciar Sesión"):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        st.success("Login correcto")

        st.write(
            response.user.email
        )

    except Exception as e:

        st.error(str(e))