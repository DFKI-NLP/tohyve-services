# DFKI NLU Machine Translator Tool
Its a tool to translate a speciafic language text into a targeted language text. For machine translation it uses a huggingface pretrained model <u>[facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M)</u> developed by facebookresearch. **M2M100 418M** is a multilingual encoder-decoder (seq-to-seq) model trained for Many-to-Many multilingual translation. The model that can directly translate between the 9,900 directions of 100 languages. It was first introduced in a paper called <u>[*Beyond English-Centric Multilingual Machine Translation*](https://arxiv.org/abs/2010.11125)</u>. The tool takes a **text**(string), **text_language** code (See ***Language Covered*** section below for the language code!!) and a **target_language** (See ***Language Covered*** section below for the language code!!). We did this translation sentence-wise just to avoid maximum length exceed issue. Our tool can translate directly between any pair of 50 languages. After translation you can download it as JSON! (See **Sample Output**.)

## Language Covered: 
Afrikaans (af), Amharic (am), Arabic (ar), Asturian (ast), Azerbaijani (az), Bashkir (ba), Belarusian (be), Bulgarian (bg), Bengali (bn), Breton (br), Bosnian (bs), Catalan; Valencian (ca), Cebuano (ceb), Czech (cs), Welsh (cy), Danish (da), German (de), Greeek (el), English (en), Spanish (es), Estonian (et), Persian (fa), Fulah (ff), Finnish (fi), French (fr), Western Frisian (fy), Irish (ga), Gaelic; Scottish Gaelic (gd), Galician (gl), Gujarati (gu), Hausa (ha), Hebrew (he), Hindi (hi), Croatian (hr), Haitian; Haitian Creole (ht), Hungarian (hu), Armenian (hy), Indonesian (id), Igbo (ig), Iloko (ilo), Icelandic (is), Italian (it), Japanese (ja), Javanese (jv), Georgian (ka), Kazakh (kk), Central Khmer (km), Kannada (kn), Korean (ko), Luxembourgish; Letzeburgesch (lb), Ganda (lg), Lingala (ln), Lao (lo), Lithuanian (lt), Latvian (lv), Malagasy (mg), Macedonian (mk), Malayalam (ml), Mongolian (mn), Marathi (mr), Malay (ms), Burmese (my), Nepali (ne), Dutch; Flemish (nl), Norwegian (no), Northern Sotho (ns), Occitan (post 1500) (oc), Oriya (or), Panjabi; Punjabi (pa), Polish (pl), Pushto; Pashto (ps), Portuguese (pt), Romanian; Moldavian; Moldovan (ro), Russian (ru), Sindhi (sd), Sinhala; Sinhalese (si), Slovak (sk), Slovenian (sl), Somali (so), Albanian (sq), Serbian (sr), Swati (ss), Sundanese (su), Swedish (sv), Swahili (sw), Tamil (ta), Thai (th), Tagalog (tl), Tswana (tn), Turkish (tr), Ukrainian (uk), Urdu (ur), Uzbek (uz), Vietnamese (vi), Wolof (wo), Xhosa (xh), Yiddish (yi), Yoruba (yo), Chinese (zh), Zulu (zu)

## Installing Using Docker:
* To Pull it: 
```
docker pull akhyarahmed/dfkinludocker:mt_1.2
```
* To Run it: 
```
docker run --rm -it -p 8000:8000/tcp akhyarahmed/dfkinludocker:mt_1.2
```
## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22 or above
* create a python/conda environment and install requirements.txt using pip using 
```
pip install -r requirements.txt
```
* then go to:
```
cd dfki_nlu_docker/machine_translator
```

### To start the API:
```
python3 -m main
```
## To interact with the API:
* Interactive mode: http://localhost:8000/docs/
* Http-call: http://localhost:8000/translator/?text=your_text&text_language=text_language_code&target_language=target_language_code

## Input Constraints: 
* Each sentence length <= 120 
* Each text length can be > 0 words
* Each text can have multiple sentences!

## **Sample Input**
* Lets say, we want to translate ***"Hallo! Wie geht es dir?"*** in English. So it's input should look like below:
### **cURL Call**
```
curl -X 'GET' \
  'http://localhost:8000/translator/?text=Hallo%21%20Wie%20geht%20es%20dir%3F&text_language=de&target_language=en' \
  -H 'accept: application/json'
```

### **HTTP Call**
```
http://localhost:8000/translator/?text=Hallo%21%20Wie%20geht%20es%20dir%3F&text_language=de&target_language=en
```

### **Python Request**
```
import requests
url = "http://localhost:8000/translator/"
params = {"text": "Hallo! Wie geht es dir?", "text_language": "de", "target_language": "en"}
resp = requests.get(url=url, params=params).json()
print(resp)
```
### **Postman Collection**
```
{
	"info": {
		"_postman_id": "d00abcf7-3a7b-4d07-8ede-346161899ff9",
		"name": "DFKI_Machine_translator",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "2294233"
	},
	"item": [
		{
			"name": "translator",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:8000/translator/?text=Hallo! Wie geht es dir?&text_language=de&target_language=en",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8000",
					"path": [
						"translator",
						""
					],
					"query": [
						{
							"key": "text",
							"value": "Hallo! Wie geht es dir?"
						},
						{
							"key": "text_language",
							"value": "de"
						},
						{
							"key": "target_language",
							"value": "en"
						}
					]
				}
			},
			"response": []
		}
	]
}
```

### **Interactive Mode**
(After going to http://localhost:8000/docs/)
![Screenshot 2023-03-10 095144](https://user-images.githubusercontent.com/26096858/224271279-16cc2438-e104-4edd-8468-7c59cb1ba4c9.png)

## **Sample Output**
```yaml
{
  "input_text": "Hallo! Wie geht es dir?",
  "translated_text": "Hello! How are you?",
  "sentences": [
    "Hallo!",
    "Wie geht es dir?"
  ],
  "source_language_code": "de",
  "target_language_code": "en",
  "execution_time": 4.53
}
```

