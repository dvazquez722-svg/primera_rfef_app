import streamlit as st


# =====================================================
# LEAGUE HEADER
# =====================================================

def show_league_header(

    df

):

    st.markdown("# 📊 Análisis de Liga")

    num_teams = len(df)

    best_attack = df.loc[

        df["xG"].idxmax()

    ]

    best_defense = df.loc[

        df["Goles recibidos"].idxmin()

    ]

    best_possession = df.loc[

        df["Posesión del balón, %"].idxmax()

    ]

    best_pressing = df.loc[

        df["PPDA"].idxmin()

    ]

    st.markdown(

        f"""

<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(135deg,#0f172a,#1e293b);
border:1px solid rgba(255,255,255,0.08);
">

<h1 style="
margin-bottom:5px;
font-size:42px;
font-weight:800;
color:white;
">

🏆 Primera Federación

</h1>

<h3 style="
margin-top:0;
margin-bottom:25px;
color:#38bdf8;
font-weight:600;
">

Visión Global de la Competición

</h3>

<div style="
display:grid;
grid-template-columns:repeat(2,1fr);
gap:18px;
color:white;
font-size:17px;
">

<div>

<b>Equipos analizados</b><br>

{num_teams}

</div>

<div>

<b>Mayor producción ofensiva</b><br>

{best_attack["Equipo"]}

</div>

<div>

<b>Mayor control del balón</b><br>

{best_possession["Equipo"]}

</div>

<div>

<b>Mejor rendimiento defensivo</b><br>

{best_defense["Equipo"]}

</div>

</div>

</div>

""",

        unsafe_allow_html=True

    )

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Equipos",

            num_teams

        )

    with c2:

        st.metric(

            "Máx. xG",

            round(

                best_attack["xG"],

                2

            )

        )

    with c3:

        st.metric(

            "Menos goles recibidos",

            int(

                best_defense["Goles recibidos"]

            )

        )

    with c4:

        st.metric(

            "PPDA mínimo",

            round(

                best_pressing["PPDA"],

                2

            )

        )

    st.divider()