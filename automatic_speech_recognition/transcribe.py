import gradio as gr
import hyperlink
import uvicorn
import socket

from web_stream import start_stream, stream_tcp_audio 
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import StreamingResponse


app = FastAPI()

CUSTOM_PATH = "/asr"


# Endpoint to serve streaming
@app.get("/asr/web-stream")
async def stream_asr(url: str, source_language: str):
    try:
        if "tcp" in url:
            # async for asr_response in stream_tcp_audio(url, source_language):
            #     yield asr_response
            return StreamingResponse(stream_tcp_audio(url, source_language), media_type = "application/json")
            # return StreamingResponse(content = stream_tcp_audio(url, source_language), media_type = "application/json")
        else:
            return StreamingResponse(content = start_stream(url, source_language), media_type = "application/json")
    except socket.error as e:
        print(f"Socket error: {e}")



# ASR Class
class ASR:
    # initialize model and model name
    def __init__(self, pipe, MODEL_NAME) -> None:
        self.pipe = pipe
        self.MODEL_NAME = MODEL_NAME

    
    # transcreibe method for microphone streaming
    def transcribe_microphone(self, Input_language, Microphone,  state=""):
        if Input_language is None or Microphone is None:
            state =""
            return state, state
        
        if Input_language and Input_language[0]=="d":
            Input_language = "de"
        elif Input_language and Input_language[0]=="e":
            Input_language = "en"
        # if Input_language is None:
        #     return "ERROR: You didn't set transcribe language code!\n"
        
        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=Input_language, task="transcribe")
        
        # time.sleep(10)
        text = self.pipe(Microphone)["text"]
        state += text + " "
        return text, state

        
    # transcreibe method for audio file upload
    def transcribe_file(self, Input_language, File_upload):
        warn_output = ""
        if File_upload is None:
            warn_output = "ERROR: You didn't upload an audio file !\n"
        elif Input_language is None:
            warn_output =  "ERROR: You didn't set transcribe language code!\n"
        
        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=Input_language, task="transcribe")
        text = self.pipe(File_upload)["text"]
        return warn_output + text


    # method which launch Gradio to do ASR
    def do_asr(self) -> None:
        url = hyperlink.parse(u"https://github.com/DFKI-NLP/tohyve-services/tree/master/automatic_speech_recognition")
        css_code = 'div {\
            margin-left:auto;\
            margin-right:auto;\
            width:100%;\
            background-image:url("https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs");\
            background-repeat: no-repeat;\
            background-size: auto;\
            background-position: relative;\
            }'
        title = "Automatic Speech Recognition Demonstrator"
        description = (
                f"""\n\nThis is the demonstrator for multilingual automatic speech recognition for the ToHyVe project. It supports static file upload (mp3 and wav format) and audio streaming from the local microphone. 
                To use the online demo please specify the language. Supported languages are:
                'en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi','he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la', 'mi', 
                'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn', 'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw',  'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be', 'tg', 'sd', 
                'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn', 'mt', 'sa', 'lb', 'my', 'bo', 'tl', 'mg', 'as', 'tt', 'haw', 'ln', 'ha', 'ba', 'jw', 'su', 'my', 'ca', 'nl', 'ht', 'lb', 'ps', 'pa', 'ro', 'ro', 'si', 'es'
                \nMore information can be found in the technical documentation ({url.to_text()})."""
            )
        demo = gr.Blocks(css=".gradio-container {background: url('https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs'); background-repeat: no-repeat; background-attachment:absolute; background-position: 30px 40px; background-size: 150px 75px;}")
        
        # interface for microphone
        micro_transcribe = gr.Interface(
            fn=self.transcribe_microphone,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="e.g. de or en", type="text"),
                gr.Audio(source="microphone", type="filepath", streaming=True),
                "state",
            ],
            outputs=["textbox", "state"],
            title=title,
            description=description,
            live=True,
            # auto_submit_duration=20,
            allow_flagging="never" 
        )

        # interface for file upload
        file_transcribe = gr.Interface(
            fn=self.transcribe_file,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="e.g. de or en", type="text"),
                gr.components.Audio(source="upload", type="filepath")
            ],
            outputs="text",
            css=css_code,
            title=title,
            description=description,
            allow_flagging="never",
        )
        with demo:
            gr.TabbedInterface([micro_transcribe, file_transcribe], ["Transcribe Microphone", "Transcribe File"])


        global app 
        app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)
        
        uvicorn.run("transcribe:app", host="0.0.0.0", port=8001)
        return