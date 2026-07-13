from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips


# =====================================================
# EXPORTAR RESUMEN
# =====================================================

def export_summary(

    clips,

    output_folder,

    filename

):

    output_folder = Path(

        output_folder

    )

    output_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    final_path = (

        output_folder

        /

        f"{filename}.mp4"

    )

    video_clips = []

    for clip in clips:

        video_path = clip.get(

            "video_url"

        )

        if not video_path:

            continue

        if not Path(

            video_path

        ).exists():

            continue

        try:

            video = VideoFileClip(

                str(video_path)

            )

            video_clips.append(

                video

            )

        except Exception as e:

                print(e)

                continue

    if len(video_clips) == 0:

        return None

    final_video = concatenate_videoclips(

        video_clips,

        method="compose"

    )

    final_video.write_videofile(

        str(final_path),

        codec="libx264",

        audio_codec="aac",

        fps=25

    )

    final_video.close()

    for clip in video_clips:

        clip.close()

    return str(

        final_path

    )