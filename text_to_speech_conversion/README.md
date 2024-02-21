# Text To Speech conversion (TTS)
Generates speech for an input text. For speech transformation it uses the Nvidia NeMo [(Text-to-Speech)](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/tts/intro.html). Nvidia NeMo also provides TTS for other languages, but we have to use their specific models for that particular language. For that anyone have to go to that [link](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/stable/tts/checkpoints.html) and select their model. To use that model you just have to import them in this code [script](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/model.py) and have to modify code in **get_conversion()** method from [convert.py](https://github.com/DFKI-NLP/tohyve-services/blob/master/text_to_speech_conversion/convert.py) for that particular language model. For now we only takes German(de) or English(en) texts and converts them to their respective speech (.wav) versions.

## Installation Using Docker:
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
**1. Text-to-Speech Tool:**

Get the details and the Text-to-Speech functionality for a text.

```hs
GET /tts
```

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

```
Base64 encoded string of input text which later tranform into an audio.
```

**2. Text-to-Speech Requests:**

Need to send two requests to get the TTS audio. First POST request will generate the audio and second GET request will return the generated audio.

```hs
2.1 POST /tts/run/predict
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

The same request body as before.


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
2.2 GET /tts/file=/tmp/gradio/unique_id/orig_name from the above
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


## Average Response time for TTS:
**German: ~ 0.17 secs**

**English: ~ 0.047 secs**

N.B: These number depends of sentence length.

We calculate average from 20 german sentences and 20 english sentences.

German Sentences:

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

English Sentences:

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

