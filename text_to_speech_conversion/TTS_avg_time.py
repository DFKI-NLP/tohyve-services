import time
import requests
import json


def send_sentence(sentence, language_code):
    url = "https://dfki-3109.dfki.de/tts/run/predict"

    data = {
        "data": [
            language_code,
            sentence
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    duration  = json.loads(response.text)["duration"]

    print(duration)
    
    return duration


en_sentences = [
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
]

de_sentences = [
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
]

# Define which language to use
# language_code = "de"
language_code = "en"

total_processing_time = 0
if language_code == "en":
    total_processing_time = 0
    for sentence in en_sentences:
        total_processing_time += send_sentence(sentence, language_code)


    average_time = total_processing_time/len(en_sentences)
elif language_code == "de":

    for sentence in de_sentences:
        total_processing_time += send_sentence(sentence, language_code)


    average_time = total_processing_time/len(de_sentences)  

print(f"Average processing time for a single sentence: {round(average_time,3)} seconds")

"""
For above sentences average processing time for a single language is:
    German: 0.17 secs (approx)
    English: 0.047 secs (approx)

(These number depends of sentence length.)
"""