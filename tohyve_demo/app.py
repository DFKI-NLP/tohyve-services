from flask import Flask, render_template

import asyncio
import websockets
import threading
import json
import requests
import traceback
import sys
import pyaudio
import wave

app = Flask(__name__)

# Store WebSocket clients
clients = set()


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

# Function to handle WebSocket connections
async def audio_socket(websocket, path):
    clients.add(websocket)
    try:
        while True:
            # audio_data = await websocket.recv()
            json_data = await websocket.recv()
            json_data = json.loads(json_data)
            asr_success = False
            mt_success = False
            tts_success = False
            source_language = json_data["data"][0]
            target_language = json_data["target_language"]
            json_data.pop('target_language', None)

            headers = {"Content-Type": "application/json"}
            asr_url = "https://dfki-3109.dfki.de/asr/run/predict"
            mt_url = "https://dfki-3109.dfki.de/mt/run/predict"
            tts_url = "https://dfki-3109.dfki.de/tts/run/predict"
            
            try:
                asr_response = requests.post(asr_url, json=json_data, headers=headers)
                asr_response_text = json.loads(asr_response.text)
                if "data" in asr_response_text.keys():
                    asr_response_text = asr_response_text.get("data")[0]
                    asr_success = True
            except Exception as e:
                print("ASR REQUEST ERROR!!\n"+traceback.print_exception(*sys.exc_info()))

            
            try:
                if asr_success:
                    mt_data = get_mt_formatted_data(asr_response_text, source_language, target_language)
                    mt_response = requests.post(mt_url, json=mt_data, headers=headers)
                    mt_response_text = json.loads(mt_response.text)
                    if "data" in mt_response_text.keys():
                        mt_response_text = mt_response_text.get("data")[0]
                        mt_success = True
                        print(asr_response_text, "  ", mt_response_text)
                else:
                    raise AssertionError
            except AssertionError as e:
                print("ASR response text is broken!!")
            except Exception as e:
                print("MT REQUEST ERROR!!\n"+traceback.print_exception(*sys.exc_info()))

            # Process audio_data as needed
            # For example, you can save it to a file
            # with wave.open('output.wav', 'wb') as wf:
            #     wf.setnchannels(2)
            #     wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            #     wf.setframerate(44100)
            #     wf.writeframes(audio_data)
            # Send a response back to the client (for example)
            # response = {
            #     "status": "success",
            #     "message": "Audio data received and processed."
            # }
            await websocket.send(str(asr_response.json()))
    except websockets.exceptions.ConnectionClosedOK:
        clients.remove(websocket)

# Function to start the WebSocket server
def start_websocket_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(audio_socket, "0.0.0.0", 8761)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Start the WebSocket server in a separate thread
if __name__ == '__main__':
    socket_thread = threading.Thread(target=start_websocket_server)
    socket_thread.start()
    app.run(debug=True, host="0.0.0.0", port=8001)

