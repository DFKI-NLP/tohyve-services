# Automatic Speech Recognition (ASR)
ASR transcripes spoken audio into text form. The service works with MP3-encoded audio files and audio streams. For ASR the project uses huggingface's [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) model. This model is published by [Radford et al., 2022](https://arxiv.org/abs/2212.04356).

## Installing Using Docker:
### To Pull it: 

* Medium model (~16GB)
```bash
docker pull dfkitohyve/tohyveservices:stream-asr-medium-cuda-12.2.0-v2 
```
* Large model (~34GB)
```bash
docker pull dfkitohyve/tohyveservices:asr-large-cuda-12.2.0
```

### To Run it: 

CPU
```bash
docker run -p 8001:8001/tcp dfkitohyve/tohyveservices:stream-asr-medium-cuda-12.2.0-v2 
```

GPU
```bash
docker run --gpus '"device=0"' -p 8001:8001/tcp dfkitohyve/tohyveservices:stream-asr-medium-cuda-12.2.0-v2 
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
```bash
python3 -m main
```
## The tool is available in:
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/asr/
* API call [Python example](https://github.com/DFKI-NLP/tohyve-services/blob/master/automatic_speech_recognition/request_example.py)

## API Documentation:

### Base URL:
https://dfki-3109.dfki.de

### Endpoints:
**1. ASR Tool:**

Get the details and the ASR capabilities for file-upload and microphone streaming.

```hs
GET /asr
```

**Parameters**

```
input_language (string, required): Language code of the input audio.
```
*All other language codes can be found [here](https://dfki-3109.dfki.de/asr/).*


**2. ASR Requests:**

The main endpoint which performs the ASR. Anyone using this endpoint can directly get the ASR results from our tool.

```hs
POST /asr/run/predict
```

**Parameters**

```
fn_index (integer, required): 4(A constant number!) 
data (list, required): A list which contains input_language and a dictionary. 
input_language (string, required): Language code of the input audio.
a dictionary (dictioanry, required): Contains two elements, data and name.
inner data (string, required): Base64 encoded string for the input audio.
name (string, required): A name for the audio.
```

N.B: Both **1.** and **2.** endpoints has the same request body and responses. 

**Request Body (Input data format)**
```bash
{
    "fn_index":3, # always use 4, it's a fixed code from the Gradio 
    "data": [
        "input_language", # this need to be change according to the audio language code 
        {
            "data":"data:audio/wav;base64," + str(base64_encoded_audio),
            "name":"sample_audio.mp3" # just give any name
        }
    ]
}
```

**Response**
```bash
{
    "data":["transcribe text"],
    "is_generating":boolean response,
    "duration":time to produce result,
    "average_duration":average time to produce each result
}
```

**Request via Python Script**

To send a request for file uplaod we need a base64 encodings. So we wrote a python script for that. Here you can find the [`script`](./request_example.py).

**Curl Call**
```bash
	curl -X POST \
      -H "Content-Type:application/json" \
      -d @curl.json \
      https://dfki-3109.dfki.de/asr/run/predict  
```
Where [`curl.json`](./curl.json) is a JSON file, which contains input data. Please check curl.json before using it. 


**3. ASR Web Stream:**

We extended the service with web streaming capabilities. In this end-point you can send a streaming URL with its streaming language and get the transcribed text for streaming data asynchronously.

```hs
GET /asr/web-stream
```

**Parameters**
```
url (string, required): A streaming URL.
source_language (string, required): Language code of the streaming audio.
```

**Request Body (Input data format)**
```bash
{
    "url": "your streaming url",
    "source_language": "streaming language code"
}
```

**Response**

Response body is same as above. 

**Request via Python Script**

To fetch streaming data and create a continious request we need a stremaing request. So we wrote a python script for that. Here you can find the [`script`](./request_stream.py). 

**Curl Call**
```bash
curl -G "http://localhost:8001/asr/web-stream" \
    --data-urlencode "url=https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web" \
    --data-urlencode "source_language=de"
```



## Error Handling
* 400 Bad Request: Invalid request parameters.
* 404 Not Found: Resource not found.


## Average Response time for ASR:
**German: ~ 12.401 secs**

We calculate an average from 6 German audios. Where each audio has length:

1. 7 secs
2. 13 secs
3. 10 secs 
4. 2 secs
5. 6 secs
6. 16 secs 

To check all the audio, check at `automatic_speech_recognition/asr_sounds_de`

![avg_audio_file_time](https://github.com/DFKI-NLP/tohyve-services/assets/26096858/ed0a96a8-40c6-48b2-934d-8858ccc00b98)
