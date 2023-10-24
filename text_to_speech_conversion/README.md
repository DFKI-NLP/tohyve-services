# Text To Speech conversion (TTS)
It's a tool to take a text and create a speech out of it. For speech transformation it uses Nvidia's NeMo [(Text-to-Speech)](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/tts/intro.html) models. It only takes German(de) or English(en) texts and converts them to their respective speech (.wav) versions.

## Installing Using Docker:
### To Pull it: 
* Container Size (~7GB)
```hs
docker pull dfkitohyve/tts:gpu-cuda-12.2.0
```
### To Run it: 

CPU
```hs
docker run -p 8003:8003/tcp dfkitohyve/tts:gpu-cuda-12.2.0
```

GPU
```hs
docker run --gpus '"device=0"' -p 8003:8003/tcp dfkitohyve/tts:gpu-cuda-12.2.0
```




## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* Go to:
```
cd text_to_speech_translation
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
## To interact with the tool:
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/tts/
* <u>cURL call:</u>: 
Need to run two cURL's to get the audio file.
1. Create the audio file:
```hs
	curl -X POST \
      -H "Content-Type:application/json" \
      -d @curl.json \
      -o predict.txt \
      https://dfki-3109.dfki.de/tts/run/predict  
```
Where [curl.json](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/curl.json) is a JSON file, which contains input data.
```hs
{
    "data": [
        "de",
        "Hallo Akhyar, Wie geht's dir?"
    ]
}
```
and [predict.txt](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/predict.txt) is a text file, which contains the directory of the created audio file.
```hs
{
    "data":[
        {
            "name":"/tmp/gradio/2cf38116657fa82ba06c05fe9e04b4fcd44dee44/speech.wav",
            "data":null,
            "is_file":true,
            "orig_name":"speech.wav"
        }
    ],
    "is_generating":false,
    "duration":0.1552410125732422,
    "average_duration":1.4856630116701126
}
```
2. Downlaod the created audio file, use path from the above **data -> name** as an endpoint of **https://dfki-3109.dfki.de/tts/file=**, e.g., "https://dfki-3109.dfki.de/tts/file=/tmp/gradio/2cf38116657fa82ba06c05fe9e04b4fcd44dee44/speech.wav"
```hs
	curl -o output.wav \
      https://dfki-3109.dfki.de/tts/file=/tmp/gradio/2cf38116657fa82ba06c05fe9e04b4fcd44dee44/speech.wav 
```
**Note:** Please keep in mind that the created files extension and output file extension should be the same. In this case created file is ***speech.wav***, So the output file extension is ***output.wav***.



## API Documentation:

### Base URL:
https://dfki-3109.dfki.de

### Endpoints:
**1. GET TTS Interaction Page:**
```hs
GET /tts
```

**Description**

Get the details and the TTS capabilities for a text.

**Parameters**

```
text_language (string, required): Language code of the input text.
text (string, required): Input text.
```
**Request Body**
```hs
{ 
    "data": [
        "text_language", # this need to be change according to the input text's language code
        "text", # input text
    ]
}
```

**Response**
Base64 encoded string of input text which later tranform into an audio.


**2. Direct Text-to-Speech Request:**

Need to send two requests to get the TTS audio. First POST request will generate the audio and second GET request will return the generated audio.

```hs
1. POST /tts/run/predict
```

**Description**

Generate an audio file for a given text and save it to the `./file=/tmp/gradio/uniq_id/file_name` folder in the server.

**Parameters**

```
data (list, required): A list contains two elements which are, input_language, text. 
input_language (string, required): Language code of the input text.
text (string, required): Input text.
```
**Request Body**
```hs
{ 
    "data": [
        "input_language", # this need to be change according to the input text's language code
        "text", # input text
    ]
}
```

**Response**
```hs
{
    "data":[
            {
                "name":"path of generated audio file",
                "data":null,
                "is_file":boolean response,
                "orig_name":"original file name"
            }
        ],
    "is_generating":boolean response,
    "duration":time to produce result,
    "average_duration":average time to produce each result
}
```
```hs
2. GET /tts/file=/tmp/gradio/unique_id/orig_name from the above
```

**Description**
Get the generated audio from the server.

**Parameters**

None

**Response**

Base64 encoded string of input text which later tranform into an audio.

## Error Handling
* 400 Bad Request: Invalid request parameters.
* 404 Not Found: Resource not found.
