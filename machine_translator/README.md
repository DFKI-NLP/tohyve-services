# Machine Translator Tool
Its a tool to translate a speciafic language text into a targeted language text. For machine translation it uses a huggingface pretrained model <u>[facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)</u> developed by facebookresearch. **M2M100 418M** is a multilingual encoder-decoder (seq-to-seq) model trained for Many-to-Many multilingual translation. The model that can directly translate between the 9,900 directions of 100 languages. It was first introduced in a paper called <u>[*Beyond English-Centric Multilingual Machine Translation*](https://arxiv.org/abs/2010.11125)</u>. The tool takes a **text**(string), **text_language** code (See ***Language Covered*** section below for the language code!!) and a **target_language** (See ***Language Covered*** section below for the language code!!). We did this translation sentence-wise just to avoid maximum length exceed issue. Our tool can translate directly between any pair of 50 languages. After translation you can download it as JSON! (See **Sample Output**.)

## Installing Using Docker:
* To Pull it: 
```
docker pull dfkitohyve/mt:gpu-cuda12.2.0
```
* To Run it: 

CPU
```
docker run -p 8002:8002/tcp dfkitohyve/mt:gpu-cuda12.2.0
```

GPU
```
docker run --gpus '"device=0"' -p 8002:8002/tcp dfkitohyve/mt:gpu-cuda12.2.0
or
docker run --gpus all -p 8002:8002/tcp dfkitohyve/mt:gpu-cuda12.2.0
```




## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* Go to:
```
cd machine_translation
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
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/mt/
* <u>cURL call:</u>: 
```
	curl -X POST \
	-H "Content-Type:application/json" \
	-d @curl.json \
	https://dfki-3109.dfki.de/mt/run/predict  
```
Where [curl.json](https://github.com/DFKI-NLP/tohyve-services/blob/master/machine_translator/curl.json) is a JSON file, which contains input data.
```
{
    "data": [
        "en",
        "hello! how are you?",
        "de"
    ]
}
```