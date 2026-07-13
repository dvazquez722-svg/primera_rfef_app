from config import supabase


# =====================================================
# LOAD
# =====================================================

def load_teams():

    response = (
        supabase.table("teams")
        .select("*")
        .order("name")
        .execute()
    )

    return response.data


# =====================================================
# LOAD ONE
# =====================================================

def get_team(team_id):

    response = (
        supabase.table("teams")
        .select("*")
        .eq("id", team_id)
        .single()
        .execute()
    )

    return response.data


# =====================================================
# CREATE
# =====================================================

def create_team(data):

    response = (
        supabase.table("teams")
        .insert(data)
        .execute()
    )

    return response.data


# =====================================================
# UPDATE
# =====================================================

def update_team(team_id, data):

    response = (
        supabase.table("teams")
        .update(data)
        .eq("id", team_id)
        .execute()
    )

    return response.data


# =====================================================
# DELETE
# =====================================================

def delete_team(team_id):

    response = (
        supabase.table("teams")
        .delete()
        .eq("id", team_id)
        .execute()
    )

    return response.data