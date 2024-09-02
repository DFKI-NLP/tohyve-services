from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from utils import process_loop, WavHandler

# Set url for the TTS service
# SERVER_URL = "https://dfki-3109.dfki.de/"
# SERVER_URL = "http://localhost:8003/"
SERVER_URL = "http://tts_container:8003/"
TTS_URL = SERVER_URL + "tts/run/predict"
GET_FILE_URL = SERVER_URL + "tts/file="

# Set path of temporary download folder and for the save file
DOWNLOAD_DIR = "/app/downloads/"
UPLOAD_DIR = '/app/box/'

# define the fastapi app
app = FastAPI()


# use pydantics BaseModel to validate the incoming POST requests
class TextInput(BaseModel):
    data: List[str]


@app.post("/split")
async def request_handler(input: TextInput):
    """Uses the TTS service to turn text into speech.

    process_loop: recursively send text to the TTS service and splits it into
    smaller chunks if the service can't handle the size.

    WavHandler download, concatenate: deal with a number of generated
    wav files to expose them for http requests
    """

    # extract the field from the TextInput class and
    # get the filepaths by sending text to the TTS
    language = input.data[0]
    text = input.data[1]
    filepaths = await process_loop(TTS_URL, text, language)

    wavhandler = WavHandler(DOWNLOAD_DIR, UPLOAD_DIR, GET_FILE_URL, filepaths)
    await wavhandler.download()
    await wavhandler.concatenate()

    return wavhandler.get_output()


@app.get(UPLOAD_DIR + "{code}")
def get_file(code):
    """Returns the output file for a http GET comand."""
    file_path = UPLOAD_DIR + code
    return FileResponse(file_path, media_type="audio/wav")
