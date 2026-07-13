import uuid

from config import supabase


# =====================================================
# CONFIG
# =====================================================

BUCKET = "videos"


# =====================================================
# UPLOAD VIDEO
# =====================================================

def upload_video(video_file):

    file_name = f"{uuid.uuid4()}.mp4"

    file_bytes = video_file.read()

    supabase.storage.from_(

        BUCKET

    ).upload(

        file_name,

        file_bytes,

        {

            "content-type": "video/mp4"

        }

    )

    public_url = supabase.storage.from_(

        BUCKET

    ).get_public_url(

        file_name

    )

    return public_url


# =====================================================
# DELETE VIDEO
# =====================================================

def delete_video(video_url):

    file_name = video_url.split("/")[-1]

    response = supabase.storage.from_(

        BUCKET

    ).remove(

        [file_name]

    )

    return response


# =====================================================
# GET FILE NAME
# =====================================================

def get_file_name(video_url):

    return video_url.split("/")[-1]