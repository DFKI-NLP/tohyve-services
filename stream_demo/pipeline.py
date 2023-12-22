import traceback
import json
import uvicorn
import requests
import asyncio
import httpx
import base64

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()

@app.get("/stream-pipe")
async def stream(stream_url: str, source_language: str, target_language: str):
    async def event_stream():
        async for result in send_stream_req_pipe(stream_url, source_language, target_language):
            yield result
            await asyncio.sleep(0)
    return StreamingResponse(content = event_stream(), media_type = "application/json")

        
async def send_stream_req_pipe(stream_url, source_language, target_language):
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
                                    # mt_response = requests.post(mt_url, json = mt_data, headers = headers)
                                    async with httpx.AsyncClient() as client:
                                        mt_response = await client.post(mt_url, json = mt_data, headers = headers)
                                    mt_response_text = json.loads(mt_response.text)
                                    if "data" in mt_response_text.keys() and mt_response_text.get("data") is not None:
                                        mt_response_text = mt_response_text.get("data")[0]
                                        mt_success = True
                                        if mt_success and mt_response_text:
                                            tts_data = get_tts_formatted_data(mt_response_text, target_language)
                                            # tts_post_audio = requests.post(tts_url, json = tts_data, headers = headers).text
                                            async with httpx.AsyncClient() as client:
                                                tts_post_audio = await client.post(tts_url, json = tts_data, headers = headers)
                                            tts_post_audio = json.loads(tts_post_audio.text)
                                            tts_get_audio = None
                                            if "data" in tts_post_audio.keys() and tts_post_audio.get("data") is not None:
                                                # tts_get_audio = requests.get(tts_get_audio_url+tts_post_audio.get("data")[0]["name"])
                                                async with httpx.AsyncClient() as client:
                                                    tts_get_audio = await client.get(tts_get_audio_url + tts_post_audio.get("data")[0]["name"])
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
                                    # "tts_audio_encodings": tts_audio_encodings
                                }

                                asr_responses = ""
                                yield json.dumps(result_dict)+"\n"
                                await asyncio.sleep(0)
                        else:
                            responses_ls.append(response_str)
                    else:
                        break
            else:
                print("No content received from the server.")
        else:
            print(f"Request failed with status code {response.status_code}")
    except Exception as e:
        yield str(traceback.format_exc())



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




# Pipeline Class
class Pipe:
    def run_pipe(self):
        uvicorn.run("pipeline:app", host="0.0.0.0", port=8009)


            


# curl 'http://localhost:8009/stream-pipe?stream_url=https%3A%2F%2Fst01.sslstream.dlf.de%2Fdlf%2F01%2F128%2Fmp3%2Fstream.mp3%3Faggregator%3Dweb&source_language=de&target_language=en' \
# -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,de;q=0.7,bn;q=0.6' \
# -H 'Connection: keep-alive' \
# -H 'Cookie: _ga=GA1.1.2037519331.1702913456; _ga_R1FN4KJKJH=GS1.1.1702932577.4.1.1702932828.0.0.0' \
# -H 'Referer: http://localhost:8009/docs' \
# -H 'Sec-Fetch-Dest: empty' \
# -H 'Sec-Fetch-Mode: cors' \
# -H 'Sec-Fetch-Site: same-origin' \
# -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
# -H 'accept: application/json' \
# -H 'sec-ch-ua: "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"' \
# -H 'sec-ch-ua-mobile: ?0' \
# -H 'sec-ch-ua-platform: "Windows"' \
# --compressed