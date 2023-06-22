import torch

from transformers import pipeline

# initiate the whisper model
def init_model():
    MODEL_NAME = "openai/whisper-medium" # we can change this name to change whisper model type
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    pipe = pipeline(
        task="automatic-speech-recognition",
        model=MODEL_NAME,
        chunk_length_s=30,
        device=device,
    )
    
    return pipe, MODEL_NAME

