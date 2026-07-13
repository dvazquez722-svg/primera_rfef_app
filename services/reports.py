from config import supabase


# =====================================================
# LOAD
# =====================================================

def load_reports(team_id):

    response = (
        supabase.table("reports")
        .select("*")
        .eq("team_id", team_id)
        .execute()
    )

    return response.data


# =====================================================
# LOAD ONE
# =====================================================

def get_report(report_id):

    response = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .single()
        .execute()
    )

    return response.data


# =====================================================
# CREATE
# =====================================================

def create_report(data):

    response = (
        supabase.table("reports")
        .insert(data)
        .execute()
    )

    return response.data


# =====================================================
# UPDATE
# =====================================================

def update_report(report_id, data):

    response = (
        supabase.table("reports")
        .update(data)
        .eq("id", report_id)
        .execute()
    )

    return response.data


# =====================================================
# DELETE
# =====================================================

def delete_report(report_id):

    response = (
        supabase.table("reports")
        .delete()
        .eq("id", report_id)
        .execute()
    )

    return response.data