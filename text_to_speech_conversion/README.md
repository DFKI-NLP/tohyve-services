# Text To Speech conversion (TTS)
It's a tool to take a text and create a speech out of it. For speech transformation it uses Nvidia's NeMo [(Text-to-Speech)](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/tts/intro.html) models. It only takes German(de) or English(en) texts and converts them to their respective speech (.wav) versions.

## Installing Using Docker:
* To Pull it: 
```
docker pull dfkitohyve/tts:1.0
```
* To Run it: 
```
docker run --rm -it -p 8000:8000/tcp dfkitohyve/tts:1.0
```
## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* Go to:
```
cd text_to_speech_conversion
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
* <u>Interactive mode</u>: http://localhost:8000/docs
* <u>cURL-call</u>:
curl -X 'POST' \
  'http://localhost:8000/convert-speech/?text=hello%2C%20what%20is%20your%20name%3F%20where%20are%20you%20from%3F&text_language=en' \
  -H 'accept: application/json' \
  -d ''