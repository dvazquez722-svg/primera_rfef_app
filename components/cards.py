"""
==========================================================
CARDS
==========================================================

Componentes visuales reutilizables para toda la aplicación.
"""

import streamlit as st


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(
    title: str,
    value: str | int | float,
    help_text: str = ""
) -> None:

    st.metric(

        label=title,

        value=value,

        help=help_text

    )


# ==========================================================
# STATUS CARD
# ==========================================================

def status_card(
    title: str,
    status: str,
    description: str = ""
) -> None:

    st.markdown(
        f"""
<div class="status-card">

<h4>{title}</h4>

<h2>{status}</h2>

<p>{description}</p>

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# RECOMMENDATION CARD
# ==========================================================

def recommendation_card(
    title: str,
    recommendation: str
) -> None:

    st.markdown(
        f"""
<div class="recommendation-card">

<h3>{title}</h3>

<p>{recommendation}</p>

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# SUCCESS CARD
# ==========================================================

def success_card(
    text: str
) -> None:

    st.markdown(
        f"""
<div class="success-card">

{text}

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# INFO CARD
# ==========================================================

def info_card(
    text: str
) -> None:

    st.markdown(
        f"""
<div class="info-card">

{text}

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# ALERT CARD
# ==========================================================

def alert_card(
    text: str
) -> None:

    st.markdown(
        f"""
<div class="alert-card">

{text}

</div>
""",
        unsafe_allow_html=True
    )