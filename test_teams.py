import streamlit as st

from config import supabase

st.title("Teams Test")

response = supabase.table(
    "teams"
).select("*").execute()

st.write(response.data)