'''
To start it:
python -m main

To use it go to:
http://localhost:8000/

'''
import traceback
import sys
import warnings

from transcribe import TTS
from model import init_model
from fastapi import FastAPI

warnings.filterwarnings("ignore", category=UserWarning)


models = init_model()


# root directory for created files
created_data_dir = "./created_data/"

description = "It's a text to speech translation tool. It convert a text into a speech. It only works for DEUTSCH and ENGLISH languages."
tags_metadata = [
    {
        "name": "/",
        "description": "Root path."
    },
    {
        "name": "converter",
        "description": "It take texts and convert them into an audio."
    }
]

# initialize FastAPI
app = FastAPI(
    title="Text To Speech Conversion Tool",
    description = description,
    openapi_tags = tags_metadata
)


# the root directory
@app.get("/", tags=["/"])
def read_root():
    return {"TTS": "Hello, I am the root of the API."}


# method to launch Gradio!
def launch_tts():
    try:
        tts_obj = TTS(pipe, MODEL_NAME)
        tts_obj.do_tts()
        return {"ASR": "Hello! I am a DFKI ASR!"}
    except Exception as e:
        return traceback.print_exception(*sys.exc_info())

# the main method
if __name__ == "__main__":
    launch_tts()