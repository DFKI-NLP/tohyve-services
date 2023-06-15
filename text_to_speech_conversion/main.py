'''
To start it:
python -m main

To use it go to:
http://localhost:8000/

'''
import traceback
import sys
import warnings
import time
import uvicorn
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from convert import TTS
from model import init_model


warnings.filterwarnings("ignore", category=UserWarning)


fast_pitch_dic, model_dic, device = init_model()


# root directory for created files
created_data_dir = "./text_to_speech_conversion/created_audio"

description = "It's a text to speech conversion tool. It convert a text into a speech. It only works for DEUTSCH and ENGLISH languages."
tags_metadata = [
    {
        "name": "/",
        "description": "Root path."
    },
    {
        "name": "converter",
        "description": "It take texts and convert them into an audio."
    },
    {
        "name": "download_audio",
        "description": "To download the audio."
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


# conversion directory
@app.post("/convert-speech/", tags=["converter"])
def convert_text(text: str, text_language: str):
    # remove the existing audio
    if os.path.exists(created_data_dir+"/speech.wav"):
        os.remove(created_data_dir+"/speech.wav")

    start_time = time.time()  
    try:
        text_language = text_language.strip()
        model = model_dic[f"model_{text_language}"]
        spec_generator = fast_pitch_dic[f"spec_generator_{text_language}"]
        tts_obj = TTS(spec_generator, model, created_data_dir)
        tts_obj.do_tts(text)
    except Exception:
        # below is the traceback
        type_, value_, traceback_ = sys.exc_info()
        error_ls = traceback.format_exception(type_, value_, traceback_)
        return error_ls[-1]
        
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    return {
        "input_text": text,
        "input_language": text_language,
        "download_audio": "http://localhost:8000/download-audio/",
        "execution_time": execution_time
    }


# download directory
@app.get("/download-audio/", tags=["download_audio"])
async def download_audio():
    try:
        file_path = created_data_dir+"/speech.wav"
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="audio/mpeg", filename = "speech.wav")
        return {"error": "File not found!"}
    except Exception:
        # below is the traceback
        type_, value_, traceback_ = sys.exc_info()
        error_ls = traceback.format_exception(type_, value_, traceback_)
        return error_ls[-1]




# the main function
if __name__=="__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # this command will use for development purposes only
    uvicorn.run("main:app", host="0.0.0.0", port=8000) # this command will use bofore creating a docker container