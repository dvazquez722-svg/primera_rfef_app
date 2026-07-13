from config import supabase

import streamlit as st


def login(email, password):

    try:

        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        return response

    except Exception as e:

        st.error(str(e))

        return None


def logout():

    supabase.auth.sign_out()

    st.session_state.clear()


def get_current_user():

    if "user" not in st.session_state:

        return None

    return st.session_state.user


def is_logged():

    return "user" in st.session_state


def get_profile(user_id):

    response = supabase.table(
        "users_profile"
    ).select("*").eq(
        "id",
        user_id
    ).execute()

    if len(response.data) == 0:

        return None

    profile = response.data[0]

    if profile["team_id"] is not None:

        team_response = supabase.table(
            "teams"
        ).select("*").eq(
            "id",
            profile["team_id"]
        ).execute()

        if len(team_response.data) > 0:

            profile["team_name"] = (
                team_response.data[0]["name"]
            )

        else:

            profile["team_name"] = None

    else:

        profile["team_name"] = None

    return profile
