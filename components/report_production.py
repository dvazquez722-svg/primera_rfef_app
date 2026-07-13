import pandas as pd
import streamlit as st

from utils.analysis_comment import (
    show_analysis_comment
)

# =====================================================
# PRODUCCIÓN → RENDIMIENTO
# =====================================================

def show_report_production(

    summary,

    team,

    team_summary

):

    st.subheader("⚽ Producción → Rendimiento")

    st.caption(
        "Construye indicadores personalizados para evaluar la eficiencia ofensiva del equipo."
    )

    numeric_columns = [

        col

        for col in summary.columns

        if pd.api.types.is_numeric_dtype(

            summary[col]

        )

    ]

    default_num = "Goles" if "Goles" in numeric_columns else numeric_columns[0]

    default_den = "xG" if "xG" in numeric_columns else numeric_columns[1]

    c1, c2 = st.columns(2)

    with c1:

        numerator = st.selectbox(

            "Numerador",

            numeric_columns,

            index=numeric_columns.index(default_num),

            key="report_ratio_num"

        )

    with c2:

        denominator = st.selectbox(

            "Denominador",

            numeric_columns,

            index=numeric_columns.index(default_den),

            key="report_ratio_den"

        )

    if numerator == denominator:

        st.warning(

            "Selecciona variables diferentes."

        )

        return

    league_ratio = (

        summary[numerator]

        /

        summary[denominator].replace(0, pd.NA)

    )

    ratio = (

        float(team_summary[numerator])

        /

        float(team_summary[denominator])

        if float(team_summary[denominator]) != 0

        else 0

    )

    percentile = (

        league_ratio

        .rank(pct=True)

        [summary["Equipo"] == team]

        .iloc[0]

        * 100

    )

    league_mean = league_ratio.mean()

    delta = ratio - league_mean

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Ratio",

            f"{ratio:.2f}"

        )

    with c2:

        st.metric(

            "Percentil Liga",

            f"{percentile:.0f}"

        )

    with c3:

        st.metric(

            "Media Liga",

            f"{league_mean:.2f}",

            f"{delta:+.2f}"

        )

    st.write("")

    comparison = pd.DataFrame({

        "Equipo": summary["Equipo"],

        "Ratio": league_ratio

    })

    comparison = (

        comparison

        .sort_values(

            "Ratio",

            ascending=False

        )

    )

    comparison["Color"] = comparison["Equipo"].apply(

        lambda x:

        "#38bdf8"

        if x == team

        else "#64748b"

    )

    st.bar_chart(

        comparison.set_index(

            "Equipo"

        )["Ratio"]

    )

    st.write("")

    if percentile >= 80:

        level = "Muy por encima de la media."

    elif percentile >= 60:

        level = "Por encima de la media."

    elif percentile >= 40:

        level = "En la media de la competición."

    elif percentile >= 20:

        level = "Por debajo de la media."

    else:

        level = "Muy por debajo de la media."

    st.success(

        f"""

**Indicador:** {numerator} / {denominator}

Valor: **{ratio:.2f}**

Percentil liga: **{percentile:.0f}**

Interpretación:

{level}

"""

    )

    st.divider()

    # =====================================================
    # COMENTARIO DEL ANALISTA
    # =====================================================

    show_analysis_comment(

        team=team,

        module="Informe Automático",

        section="Producción",

        chart="Producción → Rendimiento",

        variables=[

            numerator,

            denominator

        ]

    )