import soundfile as sf
import numpy as np
import gradio as gr
import hyperlink
import uvicorn
import traceback
import sys
import os

from fastapi import FastAPI
from model import init_model

app = FastAPI()


CUSTOM_PATH = "/tts"

# TTS Class
class TTS:
    # initialize models
    def __init__(self, created_data_dir) -> None:
        self.fast_pitch_dic, self.model_dic = init_model()
        self.data_dir = created_data_dir


    # specifiy german or english model to use
    def specify_model(self, text_language) -> None:
        self.model = self.model_dic[f"model_{text_language}"]
        self.spec_generator = self.fast_pitch_dic[f"spec_generator_{text_language}"]
        return

    # method to convert text into speech
    def get_conversion(self, text_language, text) -> str:
        try:
            text_language  = text_language.strip()
            self.specify_model(text_language)
            if text_language == "en":
                parsed = self.spec_generator.parse(text)
                spectrogram = self.spec_generator.generate_spectrogram(tokens=parsed, speaker=1)
            else:
                parsed = self.spec_generator.parse(text)
                spectrogram = self.spec_generator.generate_spectrogram(tokens=parsed)
            audio = self.model.convert_spectrogram_to_audio(spec=spectrogram)
            
            audio_file_path = self.data_dir+"/speech.wav"
            # remove the existing audio
            if os.path.exists(audio_file_path):
                os.remove(audio_file_path)

            with open(audio_file_path, "wb") as audio_file:
                sf.write(audio_file, np.ravel(audio.detach().numpy()), 22050)
        except Exception:
            # below is the traceback
            type_, value_, traceback_ = sys.exc_info()
            error_ls = traceback.format_exception(type_, value_, traceback_)
            return error_ls[-1]
        return audio_file_path


    # method which convert text into speech
    def do_tts(self) -> None:
        url = hyperlink.parse(u"https://github.com/DFKI-NLP/tohyve-services/tree/master/text_to_speech_conversion")
        css_code = 'div {\
            margin-left:auto;\
            margin-right:auto;\
            width:100%;\
            background-image:url("https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs");\
            background-repeat: no-repeat;\
            background-size: auto;\
            background-position: relative;\
            }'
        title = "Text to Speech Conversion Demonstrator"
        description = (
                f"""\n\nThis is the demonstrator for ToHyVe text to speech conversion. To use the online demo please specify the text language. It only supports English(en) and German(de) languages. 
                \nMore information can be found in the technical documentation ({url.to_text()})."""
            )
        demo = gr.Blocks(css=".gradio-container {background-image:url('https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs'); background-repeat: no-repeat; background-attachment:absolute; background-position: 30px 40px; background-size: 150px 75px;}")
        
        # interface for microphone
        text_conversion = gr.Interface(
            fn=self.get_conversion,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="Input Language e.g., de or en", type="text"),
                gr.components.Textbox(placeholder="Input Text", type="text")
            ],
            outputs=gr.components.Audio(type="filepath"), #[] missing!!!
            title=title,
            css=css_code,
            description=description,
            # auto_submit_duration=20,
            allow_flagging="never" 
        )

        with demo:
            gr.TabbedInterface([text_conversion], ["Text Conversion"])

        global app 
        app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)
        # demo.launch(server_name="0.0.0.0", server_port=8000)# to change port number, we can change "server_port" 
        # # demo.launch(server_name="0.0.0.0", server_port=8000, share=True)# to launch it to gradio public server
        
        # uvicorn.run("convert:app", host="0.0.0.0", port=8003, reload=True) # this command will use for development purposes only
        uvicorn.run("convert:app", host="0.0.0.0", port=8003)
        return