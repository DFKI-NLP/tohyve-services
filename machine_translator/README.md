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


## Average Response time for MT:
German to English: ~ 0.37 secs

English to German: ~ 0.233 secs 

N.B: These number depends of sentence length.

We calculate average from 20 german sentences and 20 english sentences.

Convert these german sentences to english:

```
"Die Sonne geht im Osten auf und malt ein goldenes Bild auf den Himmel.",
"Äpfel sind eine Art von Obst, die in vielen verschiedenen Farben und Geschmacksrichtungen erhältlich sind.",
"Hunde sind als bester Freund des Menschen bekannt und begleiten uns in vielen Lebenslagen.",
"Lesen ist eine gute Gewohnheit, die das Wissen erweitert und die Fantasie anregt.",
"Der Eiffelturm in Paris ist ein beeindruckendes Wahrzeichen und bietet einen atemberaubenden Blick auf die Stadt.",
"Wasser kocht bei 100 Grad Celsius und verwandelt sich in Dampf, der in die Atmosphäre aufsteigt.",
"Die Erde dreht sich um die Sonne und schafft so die Bedingungen für Leben, wie wir es kennen.",
"Vögel haben die Fähigkeit zu fliegen, was ihnen eine einzigartige Perspektive auf die Welt bietet.",
"Fische leben im Wasser und haben eine Vielzahl von Anpassungen entwickelt, um in verschiedenen Umgebungen zu überleben.",
"Rosen sind oft rot und werden traditionell als Symbol der Liebe und Romantik angesehen.",
"Der Himmel erscheint an einem klaren Tag blau, ein Phänomen, das durch die Streuung des Lichts in der Atmosphäre verursacht wird.",
"Bäume produzieren Sauerstoff, ein lebenswichtiges Gas, das alle Tiere zum Atmen benötigen.",
"Das Klavier ist ein musikalisches Instrument, das eine breite Palette von Tönen erzeugen kann und in vielen Musikgenres verwendet wird.",
"Autos sind ein Verkehrsmittel, das es uns ermöglicht, schnell und bequem von einem Ort zum anderen zu gelangen.",
"Regenbogen erscheinen nach dem Regen und sind ein schönes Naturphänomen, das oft Freude und Staunen hervorruft.",
"Schmetterlinge beginnen als Raupen und durchlaufen eine bemerkenswerte Verwandlung in ihrem Lebenszyklus.",
"Der Mond umkreist die Erde und beeinflusst viele Aspekte unseres Planeten, einschließlich der Gezeiten.",
"Fußball ist weltweit ein beliebter Sport und bringt Menschen aus allen Lebensbereichen zusammen.",
"Eiscreme ist ein beliebtes Dessert, das in einer Vielzahl von Geschmacksrichtungen erhältlich ist.",
"Elefanten sind die größten Landtiere und sind bekannt für ihre Intelligenz und ihr soziales Verhalten."
```

Convert these english sentences to german:

```
"The sun rises in the east.",
"Apples are a type of fruit.",
"Dogs are known as man's best friend.",
"Reading is a good habit.",
"The Eiffel Tower is in Paris.",
"Water boils at 100 degrees Celsius.",
"The Earth revolves around the Sun.",
"Birds have the ability to fly.",
"Fish live in water.",
"Roses are often red.",
"The sky appears blue during a clear day.",
"Trees produce oxygen.",
"The piano is a musical instrument.",
"Cars are a mode of transportation.",
"Rainbows appear after rain.",
"Butterflies start as caterpillars.",
"The moon orbits the Earth.",
"Soccer is a popular sport worldwide.",
"Ice cream is a popular dessert.",
"Elephants are the largest land animals."
```
