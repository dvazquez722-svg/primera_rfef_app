from pathlib import Path

import streamlit as st

from datetime import datetime


# =====================================================
# SAVE NOTE
# =====================================================

def save_note(

    team,

    section,

    note

):

    if not note.strip():

        return

    folder = Path(

        "reports"

    ) / team

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

    file = folder / "notes.md"

    with open(

        file,

        "a",

        encoding="utf-8"

    ) as f:

        f.write(

f"""

---

## {section}

Fecha: {datetime.now().strftime("%d/%m/%Y %H:%M")}

{note}

"""

        )


# =====================================================
# NOTE BOX
# =====================================================

def reflection_box(

    team,

    section

):

    st.markdown(

        "### 📝 Reflexión"

    )

    note = st.text_area(

        "",

        key=f"note_{section}"

    )

    if st.button(

        "💾 Añadir al informe",

        key=f"save_{section}"

    ):

        save_note(

            team,

            section,

            note

        )

        st.success(

            "Añadido al informe."

        )