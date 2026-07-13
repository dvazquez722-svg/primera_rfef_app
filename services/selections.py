from config import supabase


# =====================================================
# LOAD
# =====================================================

def load_selections(team_id):

    response = (
        supabase.table("coach_selections")
        .select("*")
        .order(
            "presentation_order"
    )
        .eq("team_id", team_id)
        .execute()
    )

    return response.data


# =====================================================
# LOAD STAFF
# =====================================================

def load_staff_selections(team_id):

    response = (
        supabase.table("coach_selections")
        .select("*")
        .eq("team_id", team_id)
        .eq("target", "Staff")
        .execute()
    )

    return response.data


# =====================================================
# LOAD PLAYERS
# =====================================================

def load_players_selections(team_id):

    response = (
        supabase.table("coach_selections")
        .select("*")
        .eq("team_id", team_id)
        .eq("target", "Jugadores")
        .execute()
    )

    return response.data


# =====================================================
# CREATE
# =====================================================

def create_selection(data):

    response = (
        supabase.table("coach_selections")
        .insert(data)
        .execute()
    )

    return response.data


# =====================================================
# DELETE
# =====================================================

def delete_selection(
    team_id,
    clip_id,
    target
):

    response = (
        supabase.table("coach_selections")
        .delete()
        .eq("team_id", team_id)
        .eq("clip_id", clip_id)
        .eq("target", target)
        .execute()
    )

    return response.data


# =====================================================
# EXISTS
# =====================================================

def selection_exists(
    clip_id,
    target,
    selections
):

    return any(

        selection["clip_id"] == clip_id

        and

        selection["target"] == target

        for selection in selections

    )


# =====================================================
# UPDATE ORDER
# =====================================================

def update_selection_order(
    selection_id,
    order
):

    response = (
        supabase.table(
            "coach_selections"
        )
        .update(
            {
                "presentation_order": order
            }
        )
        .eq(
            "id",
            selection_id
        )
        .execute()
    )

    return response.data

def move_selection_up(

    selection,

    selections

):

    current = selection["presentation_order"]

    previous = None

    for item in selections:

        if (

            item["target"] == selection["target"]

            and

            item["presentation_order"] == current - 1

        ):

            previous = item

            break

    if previous is None:

        return

    update_selection_order(

        selection["id"],

        current - 1

    )

    update_selection_order(

        previous["id"],

        current

    )

def move_selection_down(

    selection,

    selections

):

    current = selection["presentation_order"]

    following = None

    for item in selections:

        if (

            item["target"] == selection["target"]

            and

            item["presentation_order"] == current + 1

        ):

            following = item

            break

    if following is None:

        return

    update_selection_order(

        selection["id"],

        current + 1

    )

    update_selection_order(

        following["id"],

        current

    )