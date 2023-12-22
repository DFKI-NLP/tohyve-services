# Machine Translator Tool
Translate a text from a specific language to another language using machine translation. Machine translation is performed by the huggingface model <u>[facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)</u> developed by [facebook research](https://arxiv.org/abs/2010.11125)facebook-research.  The **M2M100 418M** model is a multilingual encoder-decoder (seq-to-seq) trained for  multilingual translation. The model  can directly translate between a set of 100 languages. The model takes a **text**(string), **source_language**  (See ***Language Covered*** section below for the language code!!) and a **target_language** (See ***Language Covered*** section below for the language code!!). We did this translation sentence-wise just to avoid maximum length exceed issue.
## Installing Using Docker:
### To Pull it: 
* Container Size (~9GB)
```hs
docker pull dfkitohyve/mt:gpu-cuda-12.2.0
```

### To Run it: 

CPU
```hs
docker run -p 8002:8002/tcp dfkitohyve/mt:gpu-cuda-12.2.0
```

GPU
```hs
docker run --gpus '"device=0"' -p 8002:8002/tcp dfkitohyve/mt:gpu-cuda-12.2.0

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
```hs
setx PATH "<path of unzipped ffmpeg>;%PATH%"
``` 

### To start the API:
```
python3 -m main
```
## To interact with the tool:
* <u>Interactive mode</u>:  https://dfki-3109.dfki.de/mt/
* <u>cURL call:</u>: 
```hs
	curl -X POST \
	-H "Content-Type:application/json" \
	-d @curl.json \
	https://dfki-3109.dfki.de/mt/run/predict  
```
Where [curl.json](https://github.com/DFKI-NLP/tohyve-services/blob/master/machine_translator/curl.json) is a JSON file, which contains input data.
```hs
{
    "data": [
        "en",
        "hello! how are you?",
        "de"
    ]
}
```


## API Documentation:

### Base URL:
https://dfki-3109.dfki.de

### Endpoints:
**1. Machine Translation Tool:**

Get the details and the MT functionality for a text.

```hs
GET /mt
```

**Parameters**

```
text_language (string, required): Language code of the input text.
text (string, required): Input text.
target_language (string, required): Language code of the target language.
```
*All other language codes can be found [here](https://dfki-3109.dfki.de/mt/).*


**2. Machine Translation Requests:**

The main endpoint which performs the Machine Transaltion(MT). Anyone using this endpoint can directly get the MT results from our tool.

```hs
POST /mt/run/predict
```

**Parameters**

```
data (list, required): A list contains three elements which are, input_language, text, and target_language. 
input_language (string, required): Language code of the input text.
text (string, required): Input text.
target_language (string, required): Language code of the target language.
```

N.B: Both **1.** and **2.** endpoints has the same request body and responses. 

**Request Body**
```hs
{ 
    "data": [
        "input_language", # this need to be change according to the input text's language code
        "text", # input text
        "target_language" # this need to be change according to the desired text language code
    ]
}
```

**Response**
```hs
{
    "data":["translated text"],
    "is_generating":boolean response,
    "duration":time to produce result,
    "average_duration":average time to produce each result
}
```
**Curl Call**
```hs
	curl -X POST \
      -H "Content-Type:application/json" \
      -d @curl.json \
      https://dfki-3109.dfki.de/tts/run/predict  
```
Where [`curl.json`](./curl.json) is a JSON file, which contains input data. Please check curl.json before using it. 

## Error Handling
* 400 Bad Request: Invalid request parameters.
* 404 Not Found: Resource not found.


