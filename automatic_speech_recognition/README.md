# Automatic Speech Recognition (ASR)
It's a tool to extract streaming audio or take an audio file(mp3) than transfrom that audio into text. For text transformation it uses huggingface's [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) model. This model is first implemented by [Radford et al., 2022](https://arxiv.org/abs/2212.04356).

## Installing Using Docker:
### To Pull it: 

* Medium model (~16GB)
```hs
docker pull dfkitohyve/asr:gpu-cuda-12.2.0
```
* Large model (~34GB)
```hs
docker pull dfkitohyve/tohyveservices:asr-large-cuda-12.2.0
```

* To Run it: 

CPU
```hs
docker run -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda-12.2.0
```

GPU
```hs
docker run --gpus '"device=0"' -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda-12.2.0
or
docker run --gpus all -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda-12.2.0
```




## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* Go to:
```
cd automatic_speech_recognition
```
* Create a python/conda environment and install requirements.txt using pip using 
```
pip install -r requirements.txt
```

* downlaod ffmpeg from https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
* than  unzip it and set new environment path using cmd
```hs
setx PATH "<path of unzipped ffmpeg>;%PATH%"
``` 

### To start the API:
```
python3 -m main
```
## To interact with the API:
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/asr/
* API call through [Python script](https://github.com/DFKI-NLP/tohyve-services/blob/master/automatic_speech_recognition/request_example.py)

## API Documentation:

### Base URL:
https://dfki-3109.dfki.de

### Endpoints:
**1. GET ASR Interaction Page:**
```hs
GET /asr
```

**Description**

Get the details and the ASR capabilities for file-upload and microphone streaming.

**Parameters**

```
input_language (string, required): Language code of the input audio. 
```
**Request Body**
```hs
{
    "fn_index":4, # always use 4, it's a fixed code from the Gradio 
    "data": [
        "input_languge", # this need to be change according to the audio language code 
        {
            "data":"data:audio/wav;base64," + str(base64_encoded_audio),
            "name":"sample_audio.mp3" # just give any name
        }
    ]
}
```

**Response**
```hs
{
    "data":["transcribe text"],
    "is_generating":boolean response,
    "duration":time to produce result,
    "average_duration":average time to produce each result
}
```


**2. Direct Transcription Request:**
```hs
POST /asr/run/predict
```

**Description**

Produce transcriptions for a single audio.

**Parameters**

```
fn_index (integer, required): 4(A constant number!) 
data (list, required): A list which contains input_language and a dictionary. 
input_language (string, required): Language code of the input audio.
a dictionary (dictioanry, required): contains two elements, data and name.
inner data (string, required): base64 encoded string for the input audio.
name (string, required): a name for the audio.
```
**Request Body**
```hs
{
    "fn_index":4, # always use 4, it's a fixed code from the Gradio 
    "data": [
        "input_languge", # this need to be change according to the audio language code 
        {
            "data":"data:audio/wav;base64," + str(base64_encoded_audio),
            "name":"sample_audio.mp3" # just give any name
        }
    ]
}
```

**Response**
```hs
{
    "data":["transcribe text"],
    "is_generating":boolean response,
    "duration":time to produce result,
    "average_duration":average time to produce each result
}
```