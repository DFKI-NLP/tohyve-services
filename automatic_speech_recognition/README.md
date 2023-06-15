# Automatic Speech Recognition (ASR)
It's a tool to extract streaming audio or take an audio file(mp3) than transfrom that audio into text. For text transformation it uses huggingface's [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) model. This model is first implemented by [Radford et al., 2022](https://arxiv.org/abs/2212.04356).

## Installing Using Docker:
* To Pull it: 
```
docker pull dfkitohyve/machine-translation:1.0
```
* To Run it: 
```
docker run --rm -it -p 8000:8000/tcp dfkitohyve/machine-translation:1.0
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
```
setx PATH "<path of unzipped ffmpeg>;%PATH%"
``` 

### To start the API:
```
python3 -m main
```
## To interact with the API:
* <u>Interactive mode</u>: http://localhost:8000/
* <u>cURL-call</u>:
curl -X POST http://localhost:8000/run/predict/ -H 'Content-Type: application/json' -d '{"data": ["language code","", "audio file path"]}'
