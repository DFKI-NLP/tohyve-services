import requests
import base64
import json
import asyncio
import socket

# Function to stream audio data from TCP
async def stream_tcp_audio(url: str, source_language:str):
    url_ls = url.split(":")
    TCP_IP = url_ls[1]
    TCP_PORT = url_ls[2]

    while TCP_IP[0] == "/":
        TCP_IP = TCP_IP[1:]
    if "?" in TCP_PORT:
        TCP_PORT = TCP_PORT.split("?")[0]
    TCP_PORT = int(TCP_PORT)
    
    # Audio settings
    CHUNK = 2024*1000

    # Create a TCP/IP socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((TCP_IP, TCP_PORT))
    reader, writer = await asyncio.open_connection(TCP_IP, TCP_PORT)

    try:
        while True:
            # data = sock.recv(CHUNK)
            data = await reader.read(CHUNK)
            if not data:
                # Close the socket
                # sock.close()
                break
            # Encode bytes to Base64 
            base64_encoded_chunk = base64.b64encode(data)
        
            # If you want the result as a string
            base64_encoded_audio = base64_encoded_chunk.decode('utf-8')
            
            # Process the Base64 encoded chunk as needed
            asr_response = await send_asr(base64_encoded_audio, source_language)
            if asr_response.text:
                try:
                    yield json.dumps(asr_response.json(), indent=4)
                except json.JSONDecodeError:
                    print(f"Failed to decode ASR response: {asr_response.text}")
            else:
                print("ASR response is empty.")
            await asyncio.sleep(0)
            # stream.write(data)
    except KeyboardInterrupt:
        print("Stream stopped by user")
    except asyncio.CancelledError:
        print("Caught Canceller Error!")
        raise GeneratorExit
    except Exception as e:
        print(e)
    finally:
        writer.close()
        await writer.wait_closed()



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



async def main(url, language_code):
    if "tcp" in url:
        async for asr_response in stream_tcp_audio(url, language_code):
            print(asr_response)
    else:
        async for asr_response in start_stream(url, language_code):
            print(asr_response)


# Start streaming
if __name__ == '__main__':
    # url = "https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web"
    # language_code = "de"

    tcp_url = "tcp://127.0.0.1:12345"
    language_code = "de"
    asyncio.run(main(tcp_url, language_code))