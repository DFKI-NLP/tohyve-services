'''
To start it:
python -m request_stream_demo

N.B: TTS encodings are commented out. If you want to use it than use uncomment line 85 and use "tts_audio_encodings" to play audio

'''


import requests
import httpx
import asyncio
import base64
import json
import traceback


# method to perform stream asr->mt->tts sequentially
async def launch_full_pipeline(stream_url, source_language, target_language):
    asr_url = "http://localhost:8001/asr/web-stream"
    params = {
        "url": stream_url,
        "source_language": source_language
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(asr_url, params=params, stream=True)
        responses_ls = []
        if response.status_code == 200:
            print("Response received successfully!")
            if response.iter_content():
                asr_responses = ""
                for i, line in enumerate(response.iter_lines()):
                    if line:
                        response_str = line.decode('utf-8')
                        if "}{" in response_str:
                            responses_ls.append(response_str[0])
                            responses_str = " ".join(responses_ls)
                            full_response = json.loads(responses_str)
                            responses_ls = []
                            responses_ls.append(response_str[1])
                            asr_responses += full_response["data"][0]
                            tts_url = "https://dfki-3109.dfki.de/tts/run/predict"
                            tts_get_audio_url = "https://dfki-3109.dfki.de/tts/file="
                            if len(asr_responses) > 10:
                                async def mt_tts_req(asr_response_text, source_language, target_language):
                                    mt_url = "https://dfki-3109.dfki.de/mt/run/predict"
                                    
                                    mt_data = get_mt_formatted_data(asr_response_text, source_language, target_language)
                                    async with httpx.AsyncClient() as client_mt:
                                        mt_response = await client_mt.post(mt_url, json = mt_data, headers = headers)
                                        mt_response_text = json.loads(mt_response.text)
                                        if "data" in mt_response_text.keys() and mt_response_text.get("data") is not None:
                                            mt_response_text = mt_response_text.get("data")[0]
                                            mt_success = True
                                            if mt_success and mt_response_text:
                                                tts_data = get_tts_formatted_data(mt_response_text, target_language)
                                                async with httpx.AsyncClient() as client_tts_1:
                                                    tts_post_audio = await client_tts_1.post(tts_url, json = tts_data, headers = headers)
                                                tts_post_audio = json.loads(tts_post_audio.text)
                                                tts_get_audio = None
                                                if "data" in tts_post_audio.keys() and tts_post_audio.get("data") is not None:
                                                    async with httpx.AsyncClient() as client_tts_2:
                                                            tts_get_audio = await client_tts_2.get(tts_get_audio_url + tts_post_audio.get("data")[0]["name"])
                                                if tts_get_audio is not None and tts_get_audio.status_code == 200:
                                                    tts_audio = base64.b64encode(tts_get_audio.content).decode("utf-8")
                                                    tts_response_text = "Successful !!"
                                                    return mt_response_text, tts_audio, tts_response_text
                                                else:
                                                    tts_response_text = "Unsuccessful !!"
                                                    raise Exception
                                            else:
                                                raise AssertionError
                                        else:
                                            mt_response_text = None
                                            mt_success = False
                                            raise Exception
                                
                                mt_response, tts_audio_encodings, tts_verdict = await mt_tts_req(asr_responses, source_language, target_language)

                                result_dict = {
                                    "asr_response": asr_responses,
                                    "mt_response": mt_response,
                                    "tts_response": tts_verdict,
                                    # "tts_audio_encodings": tts_audio_encodings ## you just have to uncomment it and use those encoding for playing audio 
                                }

                                asr_responses = ""
                                print(json.dumps(result_dict, indent=4)+"\n")
                                await asyncio.sleep(0)
                        else:
                            responses_ls.append(response_str)
                    else:
                        break # it will stop when their will be no stream data
            else:
                print("No content received from the server.")
        else:
            print(f"Request failed with status code {response.status_code}")
    except Exception as e:
        print(traceback.format_exc())



# Format data for machine translation
def get_mt_formatted_data(asr_text, source_language, target_language):
    body = {
        "data": [
            source_language,
            asr_text,
            target_language
        ]
    }
    return body



# Format data for text to speech
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



# the main method
if __name__ == "__main__":
    # Replace the values below with your stream_url, source_language, and target_language
    stream_url = "https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web"
    source_language = "de"
    target_language = "en"

    asyncio.run(launch_full_pipeline(stream_url = stream_url, source_language = source_language, target_language = target_language))