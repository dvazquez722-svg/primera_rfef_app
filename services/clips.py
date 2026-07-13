from config import supabase


# =====================================================
# LOAD
# =====================================================

def load_clips(team_id):

    response = (
        supabase.table("clips")
        .select("*")
        .eq("team_id", team_id)
        .execute()
    )

    return response.data


# =====================================================
# LOAD REPORT CLIPS
# =====================================================

def load_report_clips(report_id):

    response = (
        supabase.table("clips")
        .select("*")
        .eq("report_id", report_id)
        .execute()
    )

    return response.data


# =====================================================
# LOAD ONE
# =====================================================

def get_clip(clip_id):

    response = (
        supabase.table("clips")
        .select("*")
        .eq("id", clip_id)
        .single()
        .execute()
    )

    return response.data


# =====================================================
# CREATE
# =====================================================

def create_clip(data):

    response = (
        supabase.table("clips")
        .insert(data)
        .execute()
    )

    return response.data


# =====================================================
# UPDATE
# =====================================================

def update_clip(clip_id, data):

    response = (
        supabase.table("clips")
        .update(data)
        .eq("id", clip_id)
        .execute()
    )

    return response.data


# =====================================================
# DELETE
# =====================================================



def delete_clip(clip_id):

    response = (
        supabase.table("clips")
        .delete()
        .eq("id", clip_id)
        .execute()
    )

    print(response)

    return response


# =====================================================
# FAVORITE
# =====================================================

def set_favorite(clip_id, favorite):

    return update_clip(

        clip_id,

        {

            "favorite": favorite

        }

    )


# =====================================================
# NOTES
# =====================================================

def update_notes(clip_id, notes):

    return update_clip(

        clip_id,

        {

            "notes": notes

        }

    )


# =====================================================
# DESCRIPTION
# =====================================================

def update_description(

    clip_id,

    description

):

    return update_clip(

        clip_id,

        {

            "description": description

        }

    )


# =====================================================
# CATEGORIES
# =====================================================

def clip_categories(clips):

    return sorted(

        {

            clip["category"]

            for clip in clips

            if clip["category"]

        }

    )


# =====================================================
# REPORTS
# =====================================================

def clip_reports(

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

