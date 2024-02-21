import requests
import json
import base64
import os


# Method to send ASR requests
def send_sentence(audio_path, language_code):
    url = "https://dfki-3109.dfki.de/asr/run/predict"

    with open(audio_path, "rb") as f:
        base64_encoded_audio = base64.b64encode(f.read())
        base64_encoded_audio = str(base64_encoded_audio)[2:-1]

        headers = {"Content-Type": "application/json"}
        request_body = {
            # "fn_index":4,
            "fn_index":3,
            "data": [
                language_code,
                {
                    "data":"data:audio/wav;base64," + str(base64_encoded_audio),
                    "name":"sample_audio.mp3"
                }
            ]
        }
        response = requests.post(url, headers=headers, data = json.dumps(request_body))
        duration  = json.loads(response.text)["duration"]

        print(duration)
    
    return round(duration, 3)


# Method to get all the paths for german audio
def get_mp3_files(path, extension=".mp3"):
    return [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in files if f.endswith(extension)]


en_sound_paths = None
de_sound_paths = get_mp3_files("./asr_sounds_de")

# Define which language to use
language_code = "de"
# language_code = "en"

total_processing_time = 0
if language_code == "en":
    total_processing_time = 0
    for path in en_sound_paths:
        print(path)
        total_processing_time += send_sentence(path, language_code)
        print(path)
    average_time = total_processing_time/len(en_sound_paths)
elif language_code == "de":
    for path in de_sound_paths:
        print(path)
        total_processing_time += send_sentence(path, language_code)
        print()
    average_time = total_processing_time/len(de_sound_paths)  

print(f"Average processing time for a single audio: {round(average_time, 3)} seconds")

"""
Average processing time for a single audio is:
    German: 12.401 secs (approx) 
    audio length:
      1. 7 secs
      2. 13 secs
      3. 10 secs 
      4. 2 secs
      5. 6 secs
      6. 16 secs
"""
