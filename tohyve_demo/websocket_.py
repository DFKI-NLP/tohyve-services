
import json
import requests
import traceback
import sys
import base64

from fastapi import WebSocket


# format data for machine translation
def get_mt_formatted_data(asr_text, source_language, target_language):
    body = {
        "data": [
            source_language,
            asr_text,
            target_language
        ]
    }
    return body


# format data for text to speech
def get_tts_formatted_data(mt_text, target_language):
    # Split the string into words using space as delimiter
    words = mt_text.split()
    
    # Merge the first 25 words using space in between
    merged_string = " ".join(words[:25])
    body = {
        "data": [
            target_language,
            merged_string
        ]
    }
    return body



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        json_data = json.loads(message)
        asr_success = False
        mt_success = False
        source_language = json_data["data"][0]
        target_language = json_data["target_language"]
        json_data.pop('target_language', None)
        asr_response_text = ""
        mt_response_text = ""
        tts_response_text = "Unsuccessful !!"
        tts_audio =""
        headers = {"Content-Type": "application/json"}
        asr_url = "https://dfki-3109.dfki.de/asr/run/predict"
        mt_url = "https://dfki-3109.dfki.de/mt/run/predict"
        tts_url = "https://dfki-3109.dfki.de/tts/run/predict"
        tts_get_audio_url = "https://dfki-3109.dfki.de/tts/file="
        
        try:
            asr_response = requests.post(asr_url, json=json_data, headers=headers)
            asr_response_text = json.loads(asr_response.text)
            if "error" in asr_response_text.keys() and len(list(asr_response_text.keys())):
                asr_response_text = ""
            elif "data" in asr_response_text.keys() and asr_response_text.get("data") is not None:
                asr_response_text = asr_response_text.get("data")[0]
                asr_success = True
            else:
                asr_success = False
                raise Exception
        except Exception as e:
            asr_response_text = "ASR REQUEST ERROR !!\n"+str(traceback.print_exception(*sys.exc_info()))

        
        try:
            if asr_success and asr_response_text:
                mt_data = get_mt_formatted_data(asr_response_text, source_language, target_language)
                mt_response = requests.post(mt_url, json=mt_data, headers=headers)
                mt_response_text = json.loads(mt_response.text)
                if "data" in mt_response_text.keys() and mt_response_text.get("data") is not None:
                    mt_response_text = mt_response_text.get("data")[0]
                    mt_success = True
                else:
                    mt_success = False
                    raise Exception
            else:
                raise AssertionError
        except AssertionError as e:
            asr_response_text = "ASR response text is empty !!"
        except Exception as e:
            mt_response_text = "MT REQUEST ERROR !!\n"+str(traceback.print_exception(*sys.exc_info()))
        
        try:
            if mt_success and asr_success and mt_response_text:
                tts_data = get_tts_formatted_data(mt_response_text, target_language)
                tts_post_audio = json.loads(requests.post(tts_url, json=tts_data, headers=headers).text)
                tts_get_audio = None
                if "data" in tts_post_audio.keys() and tts_post_audio.get("data") is not None:
                    tts_get_audio = requests.get(tts_get_audio_url+tts_post_audio.get("data")[0]["name"]) 
                
                if tts_get_audio is not None and tts_get_audio.status_code == 200:
                    tts_audio = base64.b64encode(tts_get_audio.content).decode("utf-8")
                    tts_response_text = "Successful !!"
                else:
                    tts_response_text = "Unsuccessful !!"
                    raise Exception
            else:
                raise AssertionError
        except AssertionError as e:
            mt_response_text = "MT response text is empty !!"
            tts_response_text = "Unsuccessful !!"
        
        except Exception as e:
            tts_response_text = "TTS REQUEST ERROR !!\n"+str(traceback.print_exception(*sys.exc_info()))

        if tts_response_text == "Successful !!":
            pipeline_response ={
                "asr": str("ASR: "+asr_response_text), 
                "mt": str("MT: "+mt_response_text),
                "tts": str("TTS: "+tts_response_text+"\n"),
                "audio": tts_audio
            }
        else:
            pipeline_response ={
                "asr": str("ASR: "+asr_response_text), 
                "mt": str("MT: "+mt_response_text),
                "tts": str("TTS: "+tts_response_text+"\n")
            }
        await websocket.send_text(json.dumps(pipeline_response))
