import requests
import base64
import json
import asyncio

# start streaming for specific url
async def start_stream(url, language_code):
    # Make a GET request with stream=True to enable streaming
    response = requests.get(url, stream=True)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the streaming data in chunks
        try:
            for chunk in response.iter_content(chunk_size=102400):
                if chunk:
                    # Process each chunk as needed
                    # Encode bytes to Base64 
                    base64_encoded_chunk = base64.b64encode(chunk)
                
                    # If you want the result as a string
                    base64_encoded_audio = base64_encoded_chunk.decode('utf-8')
                    
                    # Process the Base64 encoded chunk as needed
                    asr_response = await send_asr(base64_encoded_audio, language_code)
                    if asr_response.text:
                        try:
                            yield json.dumps(asr_response.json(), indent=4)
                        except json.JSONDecodeError:
                            print(f"Failed to decode ASR response: {asr_response.text}")
                    else:
                        print("ASR response is empty.")
                    await asyncio.sleep(0)
        except asyncio.CancelledError:
            print("Caught Canceller Error!")
            raise GeneratorExit
    else:
        print(f"Failed to fetch streaming data. Status code: {response.status_code}")


# sends request to our asr service asyncronously 
async def send_asr(chunks, language_code):
    headers = {"Content-Type": "application/json"}
    request_body = {
        # "fn_index":4,
        "fn_index":3,
        "data": [
            str(language_code), # this need to be change according to the audio language code 
            {
                "data":"data:audio/wav;base64," + chunks,
                "name":"sample_audio.mp3"
            }
        ]
    }
    url = "https://dfki-3109.dfki.de/asr/run/predict"
    response = requests.post(url, json=request_body, headers=headers)
    return response


# Start streaming
if __name__ == '__main__':
    stream_url = 'https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web'
    language_code = "de"
    asyncio.run(start_stream(stream_url, language_code))