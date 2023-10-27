import requests
import base64
import json


audio_path = "09-Wie können uns Sprachmodelle den Alltag und die Arbeit erleichtern_ _ Paneldiskussion.mp3" # this need to be change according to the file path

with open(audio_path, "rb") as f:
    base64_encoded_audio = base64.b64encode(f.read())
    base64_encoded_audio = str(base64_encoded_audio)[2:-1]

    headers = {"Content-Type": "application/json"}
    request_body = {
        "fn_index":4,
        # "fn_index":3,
        "data": [
            "de", # this need to be change according to the audio language code 
            {
                "data":"data:audio/wav;base64," + str(base64_encoded_audio),
                "name":"sample_audio.mp3"
            }
        ]
    }
    url = "https://dfki-3109.dfki.de/asr/run/predict"
    response = requests.post(url, json=request_body, headers=headers)

    print(json.dumps(response.json(), indent=4))











