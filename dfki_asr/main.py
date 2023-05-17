'''
To start it:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

To use it go to:
http://127.0.0.1:8000/docs/

'''
import time
import logging
import os
import shutil
import traceback
import sys
import uvicorn

from extract_audio import convert_video_to_audio
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from transform_video import init_huggingface_whisper, transcribe_audio #, audio_converter, create_subtitle_video, init_whisper

app = FastAPI()
# whisper = init_whisper()
whisper_model = init_huggingface_whisper()
video_file_path = None


# the root directory
@app.get("/asr/")
def read_root():
    return {"ASR": "Hello! I am a DFKI ASR!"}



# upload and load a video into the disk
@app.post("/asr/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        global video_file_path 
        # video_file_path = os.path.join(os.getcwd(),file.filename)
        video_file_path = file.filename

        return {
            "filename": file.filename.split(".")[0],
            "file saved": video_file_path
            }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e)+" "+traceback.format_exc())


# translator directory
@app.get("/asr/transform/")
def whisper_transcribe(source_language: str, is_english: int):
    start_time = time.time()
    flag = False
    try:
        if video_file_path == None:
            raise FileNotFoundError
        
        if video_file_path[-3:] == "mp3":
            audio_path = video_file_path[:]
        # else:
        #     audio_path = convert_video_to_audio(video_file_path)
        
        logging.info("Audio conversion completed!")
        if is_english == 0 or is_english == 1:
            if video_file_path[-3:] == "mp3":
                text = transcribe_audio(audio_path, whisper_model, source_language, is_english)
            # else:
            #     text = audio_converter(audio_path, whisper, is_english)
            #     output_video = create_subtitle_video(audio_path = audio_path, video_path = video_file_path, result = text)
            
            text["text"] = text["text"].strip()
            logging.info("Text extraction completed!")
            logging.info("Subtitle creation started!")
            
            logging.info("Subtitled video created!")
        else:
            raise ValueError
    except:
        flag = True
        traceback.print_exception(*sys.exc_info())
    end_time = time.time()

    execution_time = round(end_time - start_time, 2)
    
    try:
        if video_file_path == None:
            raise FileNotFoundError 
        os.remove(video_file_path)
    except FileNotFoundError:
        flag = True
        traceback.print_exception(*sys.exc_info())

    if flag:
       return {
            "status": "Error!",
            "information": "Can not extract the audio/text! For more information see command shell.",
            "execution_time": execution_time
            }
    else:
        if video_file_path[-3:] == "mp3":
            return {
            "download_audio": "http://localhost:8000/asr/audio/",
            "extracted_text": text["text"],
            "execution_time": execution_time
            }
        else:
            return {
            "download_audio": "http://localhost:8000/asr/audio/",
            "download_subtitled_video": "http://localhost:8000/asr/video/",
            "extracted_text": text["text"],
            "execution_time": execution_time
            }


@app.get("/asr/audio/")
async def download_audio():
    try:
        file_path = "./saved_audio/trans_audio.mp3"
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="audio/mpeg", filename = "trans_audio.mp3")
        return {"error": "File not found!"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e)+" "+traceback.format_exc())


@app.get("/asr/video/")
async def download_video():
    try:
        file_path = "./saved_audio/trans_audio_subtitled.mp4"
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type="video/mp4", filename = "trans_audio_subtitled.mp4")
        return {"error": "File not found!"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e)+" "+traceback.format_exc())


# the main function
if __name__=="__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # this command will use for development purposes only
    uvicorn.run("main:app", host="0.0.0.0", port=8000) # this command will use bofore creating a docker container