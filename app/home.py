import pandas as pd
import streamlit as st
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Primera RFEF Analysis",
    page_icon="⚽",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "data/processed/team_summary.csv"
)

# =====================================================
# HEADER
# =====================================================

st.title("⚽ Primera RFEF - Team Analysis")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Equipos",
    len(df)
)

col2.metric(
    "Variables",
    len(df.columns)
)

col3.metric(
    "Temporada",
    "2025-26"
)

st.divider()

# =====================================================
# TEAM TABLE
# =====================================================

st.subheader("League Overview")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# =====================================================
# VARIABLE SELECTOR
# =====================================================

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

metric = st.selectbox(
    "Selecciona una métrica",
    numeric_cols
)

# =====================================================
# RANKING
# =====================================================

ranking = (
    df[
        ["Equipo", metric]
    ]
    .sort_values(
        metric,
        ascending=False
    )
)

st.subheader(f"Ranking - {metric}")

st.dataframe(
    ranking,
    use_container_width=True
)

# =====================================================
# BAR CHART
# =====================================================

fig = px.bar(
    ranking,
    x="Equipo",
    y=metric
)

st.plotly_chart(
    fig,
    use_container_width=True
)