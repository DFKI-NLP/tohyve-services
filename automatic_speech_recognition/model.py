import pickle
import os
import torch

from transformers import pipeline

# initiate the whisper model
def init_model():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    MODEL_NAME = "openai/whisper-medium" # we can change this name to change whisper model type
    # MODEL_NAME = "openai/whisper-large"
    path = "models/"

    if os.path.exists(path+"/whisper-medium"): # this is for my local env
        pipe = pipeline(
        task="automatic-speech-recognition",
        model=path+"/whisper-medium",
        # model=path+"/whisper-large",
        chunk_length_s=30,
        device=device
        )
    elif os.path.exists("/app/"+path): # this is for docker env
        pipe = pipeline(
        task="automatic-speech-recognition",
        model="/app/"+path+"whisper-medium",
        # model="/app/"+path+"whisper-large",
        chunk_length_s=30,
        device=device
        )
    else:
        pipe = pipeline(
            task="automatic-speech-recognition",
            model=MODEL_NAME,
            chunk_length_s=30,
            device = device
        )
    
    return pipe, MODEL_NAME

