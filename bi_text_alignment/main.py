'''
To start it:
uvicorn main:app 

To use it go to:
http://127.0.0.1:8008/docs/

'''
import time
import uvicorn
import traceback
import ast

from pydantic import BaseModel
from typing import List
from model import BiTextModels
from bi_text_align import align_text
from fastapi import FastAPI, HTTPException, Query

bitext_obj = BiTextModels() # Load Bi-text Alignment model

# api description and tags
description = "It's a bi-text alignment tool. The tool also align tokens from two different languages. It uses SIMALIGN to align two texts."
tags_metadata = [
    {
        "name": "/",
        "description": "The root of this API."
    },
    {
        "name": "bi-align-text",
        "description": "It takes two texts from two different languages and return the list of aligned words among these two texts."
    },
    {
        "name": "bi-align-tokens",
        "description": "It takes two list of tokens from two same or different languages and return the list of aligned words among these two lists."
    }
]

# initialize FastAPI
app = FastAPI(
    title="Bi-text Alignment Tool",
    description = description,
    openapi_tags = tags_metadata
)


# the root directory
@app.get("/", tags=["/"])
def read_root():
    return {"Machine": "Hello! I am Bi-text alignment tool!"}


# route for bi-text alignment of texts
@app.get("/bi-align-text/",  tags=["bi-align-text"])
def read_bi_align_text(src_text: str, tr_text: str):
    try:
        start_time = time.time()
        align_indexes, src_tokens, tr_tokens, tuple_ls  = align_text(bitext_obj, src_text, tr_text)
        end_time = time.time()

        execution_time = round(end_time - start_time, 2)
        return {
            "status": "200 -> OK",
            "source_text": src_text, 
            "target_text": tr_text,
            "source_words": src_tokens,
            "target_words": tr_tokens,
            "alignment_indexes": align_indexes,
            "aligned_words": tuple_ls,
            "execution_time": execution_time
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e)+" "+traceback.format_exc())
    

# route for bi-text alignment of tokens
@app.get("/bi-align-tokens/",  tags=["bi-align-tokens"])
def read_bi_align_tokens(src_tokens: str, tr_tokens: str):
    try:
        src_tokens_ls = ast.literal_eval(src_tokens)
        src_tokens_str = " ".join(src_tokens_ls)
        tr_tokens_ls = ast.literal_eval(tr_tokens)
        tr_tokens_str = " ".join(tr_tokens_ls)

        start_time = time.time()
        align_indexes, src_tokens_res, tr_tokens_res, tuple_ls  = align_text(bitext_obj, src_tokens_str, tr_tokens_str)
        end_time = time.time()

        execution_time = round(end_time - start_time, 2)
        return {
            "status": "200 -> OK",
            "source_token_list": src_tokens, 
            "target_token_list": tr_tokens,
            "source_tokens": src_tokens_res,
            "target_tokens": tr_tokens_res,
            "alignment_indexes": align_indexes,
            "aligned_tokens": tuple_ls,
            "execution_time": execution_time
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e)+" "+traceback.format_exc())


# the main function
if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8008) 
