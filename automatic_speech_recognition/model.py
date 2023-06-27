import pickle
import os
import torch

from transformers import pipeline

# initiate the whisper model
def init_model():
    # device = "cuda:0" if torch.cuda.is_available() else "cpu"
    MODEL_NAME = "openai/whisper-medium" # we can change this name to change whisper model type
    path = "models/"
    model_path = path+MODEL_NAME.split("/")[1]+".pkl"

    if os.path.exists(model_path):
        pipe =  pickle.load(open(model_path, 'rb'))
    else:
        pipe = pipeline(
            task="automatic-speech-recognition",
            model=MODEL_NAME,
            chunk_length_s=30
        )
        pickle.dump(pipe, open(model_path, 'wb'))
    
    # pipe.device = device
    return pipe, MODEL_NAME

