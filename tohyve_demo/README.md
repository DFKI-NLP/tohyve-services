# ToHyVe Demo: Sevice Demonstration

## Description

ToHyVe Demo: Service Demonstration  showcases the integration of Automatic Speech Recognition (ASR), Machine Translation (MT), and Text-to-Speech (TTS) into one use-case. 
The front-end consists of two tabs: "File Upload" and "Website Streaming."
The demo is available [here](https://dfki-3109.dfki.de/tohyve-demo/).
Additionally, the service provides an API for programmatic use. 

### File Upload Tab

The "File Upload" tab allows users to upload audio files (mp3/wav) and select language options for ASR, MT, and TTS. The tool encodes audio data into base64, formats the input, and sends requests to a WebSocket ('wss://dfki-3109.dfki.de/ws'). The WebSocket sequentially sends three requests to our ToHyVe Services (ASR -> MT -> TTS), processes the responses, and displays the results on the tool.

### Website Streaming Tab

In the "Website Streaming" tab, users provide a website link with streaming audio. Similar to the File Upload tab, language options can be selected. Clicking "Start" fetches audio streams from the specified website, formats them, and sends asynchronous requests to the WebSocket. The WebSocket processes the responses asynchronously, focusing on sentences after the ASR response, and sends all results back to the tool.

## Project Folder Description

* tohyve_demo
    * templates: Contains HTML templates.
    * Dockerfile: Defines the Docker image for containerization.
    * main.py: The main Python script handling the tool logic.
    * websocket_.py: Python script managing WebSocket communication.
    * requirements.txt: Lists project dependencies.


## Containerization Description

Pull the Docker image:
```bash
docker pull dfkitohyve/tohyveservices:tohyve-demo-all-python-3.10-v2
```

Run the Docker container:
```bash
docker run --restart=always -d -p 8005:8005/tcp dfkitohyve/tohyveservices:tohyve-demo-all-python-3.10-v2
```

## API Documentation

### File Upload Tab

Sending Requests using JS WebSocket

```bash
wss://dfki-3109.dfki.de/ws
```

Recieved response format from the WebSocket
```bash
{
    "asr": "ASR: ASR response text",
    "mt": "MT: MT response text",
    "tts": "TTS: TTS response text",
    "audio": "TTS audio in base64 encodings"
}
```

### Website Streaming Tab

Sending Requests

1. Fetch audio streams from a website: e.g., https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web
2. Send asynchronous requests to the WebSocket: 
```bash
wss://dfki-3109.dfki.de/ws
```

Recieved response format from the WebSocket
```bash
{
    "asr": "ASR: ASR response text",
    "mt": "MT: MT response text",
    "tts": "TTS: TTS response text",
    "audio": "TTS audio in base64 encodings"
}
```

## API Requests inside Websocket

Details on how Websockets send API requests to our services (including data formation) can be found in the respective [GitHub]("https://github.com/DFKI-NLP/tohyve-services/tree/master") repositories of our ToHyVe services.
