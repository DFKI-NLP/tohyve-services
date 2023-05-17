import moviepy.editor as me
import shutil

from moviepy.editor import * 


def convert_video_to_audio(path):
    path = path.strip()
    video_path = path
    video = me.VideoFileClip(video_path)
    aud = video.audio
    mp3_file = "./trans_audio.mp3"
    aud.write_audiofile(mp3_file)
    
    new_destination = "./saved_audio/trans_audio.mp3"
    shutil.move(mp3_file, new_destination)
    return  new_destination