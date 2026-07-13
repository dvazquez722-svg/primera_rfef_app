import plotly.express as px
import streamlit as st


# =====================================================
# TIME SERIES ANALYSIS
# =====================================================

def show_time_series_analysis(

    team_matches,

    league_df,

    team,

    module,

    section,

    available_metrics

):

    st.subheader("📈 Evolución Temporal")

    st.write("")

    # =====================================================
    # CONTROLES
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        metric = st.selectbox(

            "Variable",

            available_metrics,

            key=f"{module}_{section}_metric"

        )

    with c2:

        period = st.selectbox(

            "Periodo",

            [

                5,

                10,

                15,

                20,

                "Toda la temporada"

            ],

            index=1,

            key=f"{module}_{section}_period"

        )

    with c3:

        chart_type = st.selectbox(

            "Tipo de gráfico",

            [

                "Línea",

                "Área",

                "Barras"

            ],

            key=f"{module}_{section}_chart"

        )

    c1, c2, c3 = st.columns(3)

    with c1:

        comparison = st.selectbox(

            "Comparar con",

            [

                "Ninguna",

                "Media temporada",

                "Media últimos 5",

                "Media primeros 5"

            ],

            key=f"{module}_{section}_comparison"

        )

    with c2:

        show_markers = st.toggle(

            "Marcadores",

            value=True,

            key=f"{module}_{section}_markers"

        )

    with c3:

        show_labels = st.toggle(

            "Etiquetas",

            value=False,

            key=f"{module}_{section}_labels"

        )

    # =====================================================
    # DATOS
    # =====================================================

    df = team_matches.copy()

    df = df.sort_values("Fecha")

    if period != "Toda la temporada":

        df = df.tail(period)

    st.divider()

    # =====================================================
    # CONSTRUCCIÓN DEL GRÁFICO
    # =====================================================

    if chart_type == "Línea":

        fig = px.line(

            df,

            x="Fecha",

            y=metric,

            markers=show_markers

        )

    elif chart_type == "Área":

        fig = px.area(

            df,

            x="Fecha",

            y=metric

        )

    else:

        fig = px.bar(

            df,

            x="Fecha",

            y=metric

        )

    # =====================================================
    # LÍNEA DE COMPARACIÓN
    # =====================================================

    comparison_value = None

    if comparison == "Media temporada":

        comparison_value = team_matches[metric].mean()

    elif comparison == "Media últimos 5":

        comparison_value = (

            team_matches

            .tail(5)[metric]

            .mean()

        )

    elif comparison == "Media primeros 5":

        comparison_value = (

            team_matches

            .head(5)[metric]

            .mean()

        )

    if comparison_value is not None:

        fig.add_hline(

            y=comparison_value,

            line_dash="dash",

            annotation_text=comparison,

            annotation_position="top left"

        )

    # =====================================================
    # ETIQUETAS
    # =====================================================

    if show_labels:

        fig.update_traces(

            text=df[metric],

            textposition="top center"

        )

    # =====================================================
    # DISEÑO DEL GRÁFICO
    # =====================================================

    fig.update_layout(

        template="plotly_dark",

        height=520,

        margin=dict(

            l=20,

            r=20,

            t=20,

            b=20

        ),

        showlegend=False,

        xaxis_title="",

        yaxis_title=metric

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # =====================================================
    # ESTADÍSTICAS DEL PERIODO
    # =====================================================

    mean_value = df[metric].mean()

    max_value = df[metric].max()

    min_value = df[metric].min()

    std_value = df[metric].std()

    if len(df) >= 6:

        half = len(df) // 2

        first_half = df.iloc[:half][metric].mean()

        second_half = df.iloc[half:][metric].mean()

        delta = second_half - first_half

        if first_half != 0:

            delta_pct = (delta / abs(first_half)) * 100

        else:

            delta_pct = 0

        if delta_pct > 5:

            trend_text = "📈 Mejorando"

        elif delta_pct < -5:

            trend_text = "📉 Empeorando"

        else:

            trend_text = "➡️ Estable"

    else:

        trend_text = "➖ Sin datos"

        delta_pct = 0

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(

            "Media",

            f"{mean_value:.2f}"

        )

    with c2:

        st.metric(

            "Máximo",

            f"{max_value:.2f}"

        )

    with c3:

        st.metric(

            "Mínimo",

            f"{min_value:.2f}"

        )

    with c4:

        st.metric(

            "Desv. típica",

            f"{std_value:.2f}"

        )

    with c5:

        st.metric(

            "Tendencia",

            trend_text,

            f"{delta_pct:+.1f}%"

        )