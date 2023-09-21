# Text To Speech conversion (TTS)
It's a tool to take a text and create a speech out of it. For speech transformation it uses Nvidia's NeMo [(Text-to-Speech)](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/tts/intro.html) models. It only takes German(de) or English(en) texts and converts them to their respective speech (.wav) versions.

## Installing Using Docker:
* To Pull it: 
```
docker pull dfkitohyve/tts:gpu-cuda12.2.0
```
* To Run it: 

CPU
```
docker run -p 8003:8003/tcp dfkitohyve/tts:gpu-cuda12.2.0
```

GPU
```
docker run --gpus '"device=0"' -p 8003:8003/tcp dfkitohyve/tts:gpu-cuda12.2.0
or
docker run --gpus all -p 8003:8003/tcp dfkitohyve/tts:gpu-cuda12.2.0
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
```
setx PATH "<path of unzipped ffmpeg>;%PATH%"
``` 

### To start the API:
```
python3 -m main
```
## To interact with the API:
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/tts/
* <u>cURL call:</u>: 
Need to run two cURL's to get the audio file.
1. Create the audio file:
```
	curl -X POST \
      -H "Content-Type:application/json" \
      -d @curl.json \
      -o predict.txt \
      https://dfki-3109.dfki.de/tts/run/predict  
```
Where [curl.json](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/curl.json) is a JSON file, which contains input data.
```
{
    "data": [
        "de",
        "Hallo Akhyar, Wie geht's dir?"
    ]
}
```
and [predict.txt](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/predict.txt) is a text file, which contains the directory of the created audio file.
```
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
```
	curl -o output.wav \
      https://dfki-3109.dfki.de/tts/file=/tmp/gradio/2cf38116657fa82ba06c05fe9e04b4fcd44dee44/speech.wav 
```
**Note:** Please keep in mind that the created files extension and output file extension should be the same. In this case created file is ***speech.wav***, So the output file extension is ***output.wav***.