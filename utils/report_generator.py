from pathlib import Path
from datetime import datetime

from docx import Document

from utils.report_styles import (

    configure_styles,

    add_cover,

    add_logo,

    add_module,

    add_section,

    add_variables,

    add_comment,

    add_signature,

    add_page

)


# =====================================================
# REPORT GENERATOR
# =====================================================

def generate_report(

    team,

    notes

):

    # =====================================================
    # CARPETA DE INFORMES
    # =====================================================

    reports_folder = (

        Path("reports")

        / team

    )

    reports_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    timestamp = datetime.now().strftime(

        "%Y-%m-%d_%H-%M"

    )

    report_path = (

        reports_folder

        /

        f"Informe_{timestamp}.docx"

    )

    # =====================================================
    # DOCUMENTO
    # =====================================================

    document = Document()

    configure_styles(

        document

    )

    add_logo(

        document,

        team

    )

    add_cover(

        document,

        team

    )

    # =====================================================
    # AGRUPAR OBSERVACIONES
    # =====================================================

    modules = {}

    for note in notes:

        module = note.get(

            "module",

            "General"

        )

        if module not in modules:

            modules[module] = []

        modules[module].append(

            note

        )

    # =====================================================
    # GENERAR INFORME
    # =====================================================

    for module in sorted(modules.keys()):

        add_module(

            document,

            module

        )

        current_section = None

        for note in modules[module]:

            section = note.get(

                "section",

                "General"

            )

            if section != current_section:

                current_section = section

                add_section(

                    document,

                    section

                )

            variables = note.get(

                "variables",

                []

            )

            add_variables(

                document,

                variables

            )

            comment = note.get(

                "text",

                ""

            )

            note_type = note.get(

                "type",

                "Observación"

            )

            date = note.get(

                "date",

                None

            )

            add_comment(

                document,

                note_type=note_type,

                comment=comment,

                date=date

            )

        add_page(

            document

        )

    # =====================================================
    # RESUMEN
    # =====================================================

    total_modules = len(

        modules

    )

    total_notes = len(

        notes

    )

    add_module(

        document,

        "Resumen del Informe"

    )

    add_section(

        document,

        "Información General"

    )

    add_variables(

        document,

        [

            f"Equipo: {team}",

            f"Fecha: {datetime.now().strftime('%d/%m/%Y')}",

            f"Módulos: {total_modules}",

            f"Observaciones: {total_notes}"

        ]

    )

    add_comment(

        document,

        note_type="Dato relevante",

        comment=(

            "Este documento reúne todas las observaciones "

            "registradas durante el proceso de análisis "

            "y constituye la versión oficial del informe "

            "técnico generado por la plataforma."

        )

    )

    add_page(

        document

    )

    # =====================================================
    # FIRMA
    # =====================================================

    add_signature(

        document

    )

    # =====================================================
    # GUARDAR
    # =====================================================

    document.save(

        report_path

    )

    return {

        "team": team,

        "file": str(

            report_path

        ),

        "modules": total_modules,

        "notes": total_notes,

        "created_at": datetime.now().strftime(

            "%d/%m/%Y %H:%M"

        )

    }