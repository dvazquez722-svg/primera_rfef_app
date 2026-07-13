# =====================================================
# REPORT DICTIONARY
# =====================================================

def build_reports_dict(reports):

    return {

        report["id"]: report["opponent"]

        for report in reports

    }


# =====================================================
# CATEGORIES
# =====================================================

def build_categories(clips):

    return sorted(

        {

            clip["category"]

            for clip in clips

            if clip.get("category")

        }

    )


# =====================================================
# OPPONENTS
# =====================================================

def build_opponents(
    clips,
    reports_dict
):

    return sorted(

        {

            reports_dict.get(

                clip["report_id"],

                "Sin rival"

            )

            for clip in clips

        }

    )


# =====================================================
# FILTER CLIPS
# =====================================================

def filter_clips(

    clips,

    reports_dict,

    search_text="",

    opponent="Todos",

    category="Todas"

):

    filtered = clips.copy()

    if opponent != "Todos":

        filtered = [

            clip

            for clip in filtered

            if reports_dict.get(

                clip["report_id"]

            ) == opponent

        ]

    if category != "Todas":

        filtered = [

            clip

            for clip in filtered

            if clip["category"] == category

        ]

    if search_text:

        search = search_text.lower()

        filtered = [

            clip

            for clip in filtered

            if search in clip["title"].lower()

        ]

    return filtered


# =====================================================
# GROUP CLIPS
# =====================================================

def group_clips(

    clips,

    reports_dict

):

    grouped = {}

    for clip in clips:

        opponent = reports_dict.get(

            clip["report_id"],

            "Sin rival"

        )

        category = clip["category"]

        grouped.setdefault(opponent, {})

        grouped[opponent].setdefault(category, [])

        grouped[opponent][category].append(clip)

    return grouped

def selection_for_clip(

    clip_id,

    target,

    selections

):

    for selection in selections:

        if (

            selection["clip_id"] == clip_id

            and

            selection["target"] == target

        ):

            return selection

    return None

def selection_for_clip(

    clip_id,

    target,

    selections

):

    for selection in selections:

        if (

            selection["clip_id"] == clip_id

            and

            selection["target"] == target

        ):

            return selection

    return None