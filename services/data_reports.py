from pathlib import Path

import json
import uuid

from datetime import datetime


# =====================================================
# REPORTS FOLDER
# =====================================================

REPORTS_FOLDER = Path("reports")


# =====================================================
# TEAM FOLDER
# =====================================================

def get_team_folder(

    team

):

    folder = REPORTS_FOLDER / team

    folder.mkdir(

        parents=True,

        exist_ok=True

    )

    return folder


# =====================================================
# REPORT FILE
# =====================================================

def get_report_file(

    team

):

    return get_team_folder(

        team

    ) / "report.json"

# =====================================================
# CREATE REPORT
# =====================================================

def create_report(team):

    report_file = get_report_file(team)

    if report_file.exists():

        return

    report = {

        "team": team,

        "created": datetime.now().isoformat(),

        "updated": datetime.now().isoformat(),

        "notes": []

    }

    with open(

        report_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            ensure_ascii=False

        )

# =====================================================
# LOAD REPORT
# =====================================================

def load_report(team):

    create_report(team)

    report_file = get_report_file(team)

    with open(

        report_file,

        "r",

        encoding="utf-8"

    ) as f:

        report = json.load(f)

    return report


# =====================================================
# SAVE REPORT
# =====================================================

def save_report(

    team,

    report

):

    report["updated"] = datetime.now().isoformat()

    report_file = get_report_file(team)

    with open(

        report_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            ensure_ascii=False

        )

# =====================================================
# ADD NOTE
# =====================================================

def add_note(

    team,

    module,

    section,

    note_type,

    text,

    chart=None,
    
    variables=None,

):

    if not text.strip():

        return

    report = load_report(team)

    note = {

        "id": str(uuid.uuid4()),

        "module": module,

        "section": section,

        "chart": chart,

        "variables": variables,

        "type": note_type,

        "text": text,

        "date": datetime.now().isoformat()

    }

    report["notes"].append(

        note

    )

    save_report(

        team,

        report

    )

# =====================================================
# GET NOTES
# =====================================================

def get_notes(team):

    report = load_report(team)

    return report["notes"]


# =====================================================
# GET NOTES BY MODULE
# =====================================================

def get_notes_by_module(

    team,

    module

):

    notes = get_notes(team)

    return [

        note

        for note in notes

        if note["module"] == module

    ]


# =====================================================
# GET NOTES BY TYPE
# =====================================================

def get_notes_by_type(

    team,

    note_type

):

    notes = get_notes(team)

    return [

        note

        for note in notes

        if note["type"] == note_type

    ]

# =====================================================
# GET NOTE
# =====================================================

def get_note(

    team,

    note_id

):

    notes = get_notes(team)

    for note in notes:

        if note["id"] == note_id:

            return note

    return None


# =====================================================
# UPDATE NOTE
# =====================================================

def update_note(

    team,

    note_id,

    **kwargs

):

    report = load_report(team)

    for note in report["notes"]:

        if note["id"] == note_id:

            for key, value in kwargs.items():

                if key in note:

                    note[key] = value

            break

    save_report(

        team,

        report

    )

# =====================================================
# DELETE NOTE
# =====================================================

def delete_note(

    team,

    note_id

):

    report = load_report(team)

    report["notes"] = [

        note

        for note in report["notes"]

        if note["id"] != note_id

    ]

    save_report(

        team,

        report

    )


# =====================================================
# CLEAR NOTES
# =====================================================

def clear_notes(

    team

):

    report = load_report(team)

    report["notes"] = []

    save_report(

        team,

        report

    )


# =====================================================
# CLEAR REPORT
# =====================================================

def clear_report(

    team

):

    report = {

        "team": team,

        "created": datetime.now().isoformat(),

        "updated": datetime.now().isoformat(),

        "notes": []

    }

    save_report(

        team,

        report

    )

# =====================================================
# GET MODULES
# =====================================================

def get_modules(team):

    notes = get_notes(team)

    return sorted(

        list(

            {

                note["module"]

                for note in notes

            }

        )

    )


# =====================================================
# GET SECTIONS
# =====================================================

def get_sections(

    team,

    module=None

):

    notes = get_notes(team)

    if module is not None:

        notes = [

            note

            for note in notes

            if note["module"] == module

        ]

    return sorted(

        list(

            {

                note["section"]

                for note in notes

            }

        )

    )


# =====================================================
# GET NOTE TYPES
# =====================================================

def get_note_types(team):

    notes = get_notes(team)

    return sorted(

        list(

            {

                note["type"]

                for note in notes

            }

        )

    )

# =====================================================
# REPORT STATISTICS
# =====================================================

def report_statistics(team):

    notes = get_notes(team)

    stats = {

        "total_notes": len(notes),

        "modules": len(

            get_modules(team)

        ),

        "sections": len(

            get_sections(team)

        )

    }

    note_types = [

        "Fortaleza",

        "Debilidad",

        "Idea táctica",

        "Dato relevante",

        "Observación"

    ]

    for note_type in note_types:

        stats[note_type] = sum(

            1

            for note in notes

            if note["type"] == note_type

        )

    return stats

# =====================================================
# GET NOTES BY SECTION
# =====================================================

def get_notes_by_section(

    team,

    module,

    section

):

    notes = get_notes(team)

    return [

        note

        for note in notes

        if (

            note["module"] == module

            and

            note["section"] == section

        )

    ]

# =====================================================
# GET NOTE BY CHART
# =====================================================

def get_note_by_chart(

    team,

    module,

    section,

    chart

):

    notes = get_notes(team)

    for note in notes:

        if (

            note["module"] == module

            and note["section"] == section

            and note.get("chart") == chart

        ):

            return note

    return None