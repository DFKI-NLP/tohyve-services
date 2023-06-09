# Bitext Alignment
Bitext alignment is a tool to find aligned words between two different language sentences. We used [***simalign***](https://github.com/cisnlp/simalign), Which first used in [***SimAlign: High Quality Word Alignments Without Parallel Training Data Using Static and Contextualized Embeddings***](https://aclanthology.org/2020.findings-emnlp.147.pdf) paper. Specially we want to find alignment between **Japanese** and **German** sentences or between **Japanese** and **French** sentences. Simalign takes tokenized sentence list as input. So for Japanese sentence tokenization we used [***fugashi***](https://pypi.org/project/fugashi/) tokenizer, which first used in this [paper](https://aclanthology.org/2020.nlposs-1.7.pdf). For all other languages we used normal [**NLTK**](https://www.nltk.org/api/nltk.tokenize.html) tokenizer.
## Installing Using Docker:
* To Pull it: 
```
docker pull akhyarahmed/dfkinludocker:bi_text_1.1.0
```
* To Run it: 
```
docker run --rm -it -p 8000:8000/tcp akhyarahmed/dfkinludocker:bi_text_1.1.0
```
## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* create a python/conda environment and install requirements.txt using pip using 
```
pip install -r requirements.txt
```
* then go to:
```
cd dfki_nlu_docker/bi_text_alignment
```

### To start the API:
```
python3 -m main
```
## **To interact with the API: (bi-align)**
* Interactive mode: http://localhost:8000/docs/
* Using URL: http://localhost:8000/bi-align/?src_text=your_text&tr_text=your_text

## **Sample Input**
* Lets say, We want to find bitext alignment for **"昼間のレクサプロが副作用ひどくて未だに気持ち悪い"** this text and for **"Daytime Lexapro still makes me sick because the side effects are so bad"** this text . So below are some invoking methods to use this API:

### **Curl Call**
```
curl -X 'GET' \
  'http://localhost:8000/bi-align/?src_text=%E6%98%BC%E9%96%93%E3%81%AE%E3%83%AC%E3%82%AF%E3%82%B5%E3%83%97%E3%83%AD%E3%81%8C%E5%89%AF%E4%BD%9C%E7%94%A8%E3%81%B2%E3%81%A9%E3%81%8F%E3%81%A6%E6%9C%AA%E3%81%A0%E3%81%AB%E6%B0%97%E6%8C%81%E3%81%A1%E6%82%AA%E3%81%84&tr_text=Daytime%20Lexapro%20still%20makes%20me%20sick%20because%20the%20side%20effects%20are%20so%20bad' \
  -H 'accept: application/json'
```

### **HTTP Call**
```
http://localhost:8000/bi-align/?src_text=昼間のレクサプロが副作用ひどくて未だに気持ち悪い&tr_text=Daytime%20Lexapro%20still%20makes%20me%20sick%20because%20the%20side%20effects%20are%20so%20bad
```
### **Python Request**
```
import requests
url = "http://localhost:8000/bi-align"
params = {"src_text": "昼間のレクサプロが副作用ひどくて未だに気持ち悪い", "tr_text": "Daytime Lexapro still makes me sick because the side effects are so bad"}
resp = requests.get(url=url, params=params).json()
print(resp)
```
### **Postman Collection**
```
{
	"info": {
		"_postman_id": "8af37e0a-c798-475a-ae0e-be27d1ac8c71",
		"name": "DFKI_Bi_Text_Alignment",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "2294233"
	},
	"item": [
		{
			"name": "bi-align",
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "Content-Type",
						"name": "Content-Type",
						"value": "application/json",
						"type": "text"
					}
				],
				"url": {
					"raw": "http://localhost:8000/bi-align/?src_text=昼間のレクサプロが副作用ひどくて未だに気持ち悪い&tr_text=Daytime Lexapro still makes me sick because the side effects are so bad",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8000",
					"path": [
						"bi-align",
						""
					],
					"query": [
						{
							"key": "src_text",
							"value": "昼間のレクサプロが副作用ひどくて未だに気持ち悪い"
						},
						{
							"key": "tr_text",
							"value": "Daytime Lexapro still makes me sick because the side effects are so bad"
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
(After going to  http://localhost:8000/docs/)
![image](https://user-images.githubusercontent.com/26096858/223685310-0c0c42e6-1da5-4294-88e6-9033c8001380.png)

## Sample Ouput:
```yaml
{
  "status": "200 -> OK",
  "source_text": "昼間のレクサプロが副作用ひどくて未だに気持ち悪い",
  "target_text": "Daytime Lexapro still makes me sick because the side effects are so bad",
  "source_words": ['昼間', 'の', 'レクサプロ', 'が', '副', '作用', 'ひどく', 'て', '未だ', 'に', '気持ち', '悪い'],
  "target_words": ['Daytime', 'Lexapro', 'still', 'makes', 'me', 'sick', 'because', 'the', 'side', 'effects', 'are', 'so', 'bad'],
  "alignment_indexes": [(0, 0), (1, 7), (2, 1), (3, 6), (4, 8), (5, 9), (8, 4), (9, 2), (10, 3), (10, 10), (10, 11), (11, 5), (11, 12)],
  "aligned_words": [
    "昼間 : Daytime",
    "の : the",
    "レクサプロ : Lexapro",
    "が : because",
    "副 : side",
    "作用 : effects",
    "未だ : me",
    "に : still",
    "気持ち : makes",
    "気持ち : are",
    "気持ち : so",
    "悪い : sick",
    "悪い : bad"
  ],
  "execution_time": 1.07
}
```
## **To interact with the API: (bi-align-tokens)**
* Interactive mode: http://localhost:8000/docs/
* Using URL: http://localhost:8000/bi-align-tokens/?src_tokens=your_token_list&tr_tokens=your_token_list

## **Sample Input**
* Lets say, We want to find bitext alignment for **['Aired', 'on', 'New', 'Zealand', "'s", 'National', 'News', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television']** this token list and for **['Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'National', 'Television']** this token list . So below are some invoking methods to use this API:

### **Curl Call**
```
curl -X 'GET' \
  'http://localhost:8000/bi-align-tokens/?src_tokens=%5B%27Aired%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%22%27s%22%2C%20%27National%27%2C%20%27News%27%2C%20%27Television%27%2C%20%27%3A%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%5D&tr_tokens=%5B%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27%3A%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27National%27%2C%20%27Television%27%5D' \
  -H 'accept: application/json'
```

### **HTTP Call**
```
http://localhost:8000/bi-align-tokens/?src_tokens=%5B%27Aired%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%22%27s%22%2C%20%27National%27%2C%20%27News%27%2C%20%27Television%27%2C%20%27%3A%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%5D&tr_tokens=%5B%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27%3A%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27Television%27%2C%20%27YouTube%27%2C%20%27-%27%2C%20%27Richard%27%2C%20%27Gage%27%2C%20%27AIA%27%2C%20%27on%27%2C%20%27New%27%2C%20%27Zealand%27%2C%20%27National%27%2C%20%27National%27%2C%20%27Television%27%5D
```
### **Python Request**
```
import requests
url = "http://localhost:8000/bi-align-tokens"
src_tokens = ['Aired', 'on', 'New', 'Zealand', "'s", 'National', 'News', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television']
trg_tokens = ['Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'National', 'Television']
params = {"src_tokens": str(src_tokens), "tr_tokens": str(trg_tokens)}
resp = requests.get(url=url, params=params).json()
print(resp)
```
### **Postman Collection**
```
{
	"info": {
		"_postman_id": "f6ab2dcf-eee5-4384-b940-8fc8d4b69a30",
		"name": "DFKI_Bi_Text_Alignment",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "2294233"
	},
	"item": [
		{
			"name": "bi-align-tokens",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "http://localhost:8000/bi-align-tokens/?src_tokens=['Aired', 'on', 'New', 'Zealand', \"'s\", 'National', 'News', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television']&tr_tokens=['Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'National', 'Television']",
					"protocol": "http",
					"host": [
						"localhost"
					],
					"port": "8000",
					"path": [
						"bi-align-tokens",
						""
					],
					"query": [
						{
							"key": "src_tokens",
							"value": "['Aired', 'on', 'New', 'Zealand', \"'s\", 'National', 'News', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television']"
						},
						{
							"key": "tr_tokens",
							"value": "['Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'National', 'Television']"
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
(After going to  http://localhost:8000/docs/)
![image](https://user-images.githubusercontent.com/26096858/226926774-452d0306-effc-4af8-ba63-874cb62f6d89.png)

## Sample Ouput:
```yaml
{
  "status": "200 -> OK",
  "source_token_list": "['Aired', 'on', 'New', 'Zealand', \"'s\", 'National', 'News', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television']",
  "target_token_list": "['Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', ':', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'Television', 'YouTube', '-', 'Richard', 'Gage', 'AIA', 'on', 'New', 'Zealand', 'National', 'National', 'Television']",
  "source_tokens": [
    "Aired",
    "on",
    "New",
    "Zealand",
    "'s",
    "National",
    "News",
    "Television",
    ":",
    "YouTube",
    "-",
    "Richard",
    "Gage",
    "AIA",
    "on",
    "New",
    "Zealand",
    "National",
    "Television",
    "YouTube",
    "-",
    "Richard",
    "Gage",
    "AIA",
    "on",
    "New",
    "Zealand",
    "National",
    "Television"
  ],
  "target_tokens": [
    "Richard",
    "Gage",
    "AIA",
    "on",
    "New",
    "Zealand",
    "National",
    "Television",
    ":",
    "YouTube",
    "-",
    "Richard",
    "Gage",
    "AIA",
    "on",
    "New",
    "Zealand",
    "National",
    "Television",
    "YouTube",
    "-",
    "Richard",
    "Gage",
    "AIA",
    "on",
    "New",
    "Zealand",
    "National",
    "National",
    "Television"
  ],
  "alignment_indexes": [
    [
      0,
      0
    ],
    [
      0,
      2
    ],
    [
      1,
      3
    ],
    [
      2,
      4
    ],
    [
      3,
      5
    ],
    [
      4,
      1
    ],
    [
      4,
      2
    ],
    [
      5,
      6
    ],
    [
      6,
      28
    ],
    [
      7,
      7
    ],
    [
      8,
      8
    ],
    [
      9,
      9
    ],
    [
      10,
      10
    ],
    [
      11,
      11
    ],
    [
      12,
      1
    ],
    [
      12,
      12
    ],
    [
      13,
      13
    ],
    [
      14,
      14
    ],
    [
      15,
      15
    ],
    [
      16,
      16
    ],
    [
      17,
      17
    ],
    [
      18,
      18
    ],
    [
      19,
      19
    ],
    [
      20,
      20
    ],
    [
      21,
      21
    ],
    [
      22,
      22
    ],
    [
      23,
      23
    ],
    [
      24,
      24
    ],
    [
      25,
      25
    ],
    [
      26,
      26
    ],
    [
      27,
      27
    ],
    [
      28,
      29
    ]
  ],
  "aligned_tokens": [
    "Aired : Richard",
    "Aired : AIA",
    "on : on",
    "New : New",
    "Zealand : Zealand",
    "'s : Gage",
    "'s : AIA",
    "National : National",
    "News : National",
    "Television : Television",
    ": : :",
    "YouTube : YouTube",
    "- : -",
    "Richard : Richard",
    "Gage : Gage",
    "Gage : Gage",
    "AIA : AIA",
    "on : on",
    "New : New",
    "Zealand : Zealand",
    "National : National",
    "Television : Television",
    "YouTube : YouTube",
    "- : -",
    "Richard : Richard",
    "Gage : Gage",
    "AIA : AIA",
    "on : on",
    "New : New",
    "Zealand : Zealand",
    "National : National",
    "Television : Television"
  ],
  "execution_time": 1.35
}
