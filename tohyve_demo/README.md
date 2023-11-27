# ToHyVe Demo: Sevice Demonstration

## Description

ToHyVe Demo: Service Demonstration showcases the integration of Automatic Speech Recognition (ASR), Machine Translation (MT), and Text-to-Speech (TTS) into one use case. To provide website streaming capabilities, we used the websocket protocol. For that, the demo needs two types of configuration: server-side and client-side configuration. We also handle the session management of the websocket.
The demo is available [here](https://dfki-3109.dfki.de/tohyve-demo/).

## Project Folder Description

* tohyve_demo
    * templates: Contains HTML templates.
    * Dockerfile: Defines the Docker image for containerization.
    * main.py: The main Python script handling the tool logic.
    * websocket_.py: Python script managing WebSocket communication.
    * requirements.txt: Lists project dependencies.


## Server-side Configuration and Endpoints

We used FastAPI and it's websocket to handle all the requests.

### Configuration

Create a ws(websocket) proxy pass for a endpoint of "/ws" into your server config file. In our case:

```hs
ProxyPass "/ws" "ws://localhost:8005/ws"
ProxyPassReverse "/ws" "ws://localhost:8005/ws"
```

### Endpoints
In [main.py](https://github.com/DFKI-NLP/tohyve-services/blob/master/tohyve_demo/main.py), their are two endpoints written for this demo. One is ***/ws*** and another one is ***/tohyve-demo***.

**1. Websocket endpoint**

Which handles both file-upload and webstreaming audios.

```hs
Websocket /ws
```


**2. Frontend endpoint**

We additioanlly hosted our front-end [/templates/index.html](https://github.com/DFKI-NLP/tohyve-services/blob/master/tohyve_demo/templates/index.html) into this endpoint, just to interact with our services.

```hs
GET /tohyve-demo
```  

## Client-side Configuration
We use JavaScript Websocket to create connection between a client to a server.

```hs
const socket = new WebSocket(websocketServerUrl);
```
and also wrote all the necessasy event handlers for a websockets.

## Front-end Description
In the front end, we utilize HTML5 for interface design and data visualization. We connect with our tool's WebSocket and stream data using JavaScript's WebSocket and Fetch methods. You will find the front-end [/templates/index.html](https://github.com/DFKI-NLP/tohyve-services/blob/master/tohyve_demo/templates/index.html) inside "***script***" tag. Additionally, the front-end interface consists of two tabs: "File Upload" and "Website Streaming".

### File Upload Tab

The "File Upload" tab allows users to upload audio files (mp3/wav) and select language options for ASR, MT, and TTS. The tool encodes audio data into base64, formats the input, and sends requests to a WebSocket ('wss://dfki-3109.dfki.de/ws'). The WebSocket sequentially sends three requests to our ToHyVe Services (ASR -> MT -> TTS), processes the responses, and displays the results on the tool.

### Website Streaming Tab

In the "Website Streaming" tab, users provide a website link with streaming audio. Similar to the File Upload tab, language options can be selected. Clicking "Start" fetches audio streams from the specified website, formats them, and sends asynchronous requests to the WebSocket. The WebSocket processes the responses asynchronously, focusing on sentences after the ASR response, and sends all results back to the tool.

## Containerization Description

Pull the Docker image:
```hs
docker pull dfkitohyve/tohyveservices:tohyve-demo-all-python-3.10-v2
```

Run the Docker container:
```hs
docker run --restart=always -d -p 8005:8005/tcp dfkitohyve/tohyveservices:tohyve-demo-all-python-3.10-v2
```





## API Documentation

### File Upload Tab

Format the file and send requests using JS WebSocket

```hs
wss://dfki-3109.dfki.de/ws #wss is a websocket safe protocol
```
**Input data format**
```bash
{
    fn_index:4, # constant value
    data:[
        sourceLanguage.value, # German(de)/English(en)
        {
            data:base64data, # base64 encoding of your data
            name:"audio.mp3"
        }
    ],
    target_language:targetLanguage.value, # German(de)/English(en)
    file_upload: 1 #1 if its file-upload 0 is for website streaming
}
```


**Response format**
```hs
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
**Input data format**
```bash
{
    fn_index:4, # constant value
    data:[
        sourceLanguage.value, # German(de)/English(en)
        {
            data:base64data, # base64 encoding of your data
            name:"audio.mp3"
        }
    ],
    target_language:targetLanguage.value, # German(de)/English(en)
    file_upload: 0 #1 if its file-upload 0 is for website streaming
}
```
N.B: Please combine several stream chunks and send them our tool. A single stream chunk is mostly empty.  

**Response format**

Same as above

## API Requests inside Websocket

Details on how Websockets send API requests to our services (including data formation) can be found in the respective [GitHub]("https://github.com/DFKI-NLP/tohyve-services/tree/master") repositories of our ToHyVe services or you can also check [websocket_.py](https://github.com/DFKI-NLP/tohyve-services/blob/master/tohyve_demo/websocket_.py) how to format and send all the requests to each services respectively.



