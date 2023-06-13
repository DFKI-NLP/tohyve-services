'''
To start it:
python -m main

To use it go to:
http://localhost:8000/docs/

'''
import time
import traceback
import sys
import uvicorn
import warnings

from model import MbartTranslatorModels, M2m100TranslatorModels
from translator import translate_text#, translate_text_lifeline #, extractSentences, cleanText #, translate_text_audio
from fastapi import FastAPI#, File, UploadFile
from utils import identify_language_codes#, identify_tags,  extract_texts

# from fastapi.responses import FileResponse

warnings.filterwarnings("ignore", category=UserWarning)
# os.environ['OPENBLAS_NUM_THREADS'] = '1'
# os.environ['OMP_NUM_THREADS'] = '1'

# initialize machine translation models
# mbart_obj = MbartTranslatorModels()
# mbart_obj = None
m2m_obj = M2m100TranslatorModels()


# root directory for created files
created_data_dir = "./created_data/"

description = "It's a machine translator tool. It translate a text into a targeted language."
tags_metadata = [
    {
        "name": "/",
        "description": "Hello, I am the root of the API."
    },
    # {
    #     "name": "file-translator",
    #     "description": "It takes a single file and translates all the text from the file into specified language text."
    # },
    {
        "name": "translator",
        "description": "It takes a single text and translates it into specified language text."
    }
]

# initialize FastAPI
app = FastAPI(
    title="DFKI NLU Machine Translator Tool",
    description = description,
    openapi_tags = tags_metadata
)


# the root directory
@app.get("/", tags=["/"])
def read_root():
    return {"Machine Translator": "Hello! I am a DFKI Machine Translator Tool!"}


# translator directory
@app.get("/translator/", tags=["translator"])
def translate_sentence(text: str, text_language: str, target_language: str):
    # if mbart_obj:
    #     try:
    #         text_language, target_language = identify_language_codes(text_language, target_language)
    #         m2m_obj = mbart_obj
    #     except Exception:
    #         return "Sorry can't translate! Problem with language codes."

    start_time = time.time()  
    try:
        translated_text, sentences = translate_text(m2m_obj, text, text_language, target_language)
    except Exception:
        # below is the traceback
        type_, value_, traceback_ = sys.exc_info()
        error_ls = traceback.format_exception(type_, value_, traceback_)
        return error_ls[-1]
        
    end_time = time.time()
    execution_time = round(end_time - start_time, 2)
    return {
        "input_text": text,
        "translated_text": translated_text,
        "sentences":sentences, 
        "source_language_code": text_language, 
        "target_language_code": target_language,
        "execution_time": execution_time
    }


# the main function
if __name__=="__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) # this command will use for development purposes only
    uvicorn.run("main:app", host="0.0.0.0", port=8000) # this command will use bofore creating a docker container



