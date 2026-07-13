import streamlit as st

from components.page_config import configure_page
from components.filters import render_filters

configure_page()

filters = render_filters()

st.write(filters)