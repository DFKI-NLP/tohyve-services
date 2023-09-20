# Automatic Speech Recognition (ASR)
It's a tool to extract streaming audio or take an audio file(mp3) than transfrom that audio into text. For text transformation it uses huggingface's [openai/whisper-medium](https://huggingface.co/openai/whisper-medium) model. This model is first implemented by [Radford et al., 2022](https://arxiv.org/abs/2212.04356).

## Installing Using Docker:
* To Pull it: 
```
docker pull dfkitohyve/asr:gpu-cuda12.2
```
* To Run it: 

CPU
```
docker run -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda12.2
```

GPU
```
docker run --gpus '"device=0"' -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda12.2
or
docker run --gpus all -p 8001:8001/tcp dfkitohyve/asr:gpu-cuda12.2
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
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/asr/
* API call through [Python script](https://github.com/DFKI-NLP/tohyve-services/blob/master/automatic_speech_recognition/request_example.py)

