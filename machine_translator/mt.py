
import gradio as gr
import hyperlink
import uvicorn
import traceback
import sys

from fastapi import FastAPI
from translator import translate_text


app = FastAPI()


CUSTOM_PATH = "/mt"

# MT Class
class MT:
    # initialize model and model name
    def __init__(self, model_obj) -> None:
        self.model = model_obj

    
    # translation method for textbox translation
    def get_translation(self, text_language, text, target_language) -> str:
        if text_language is None:
            return "Input language is missing!!"
        elif target_language is None:
            return "Target language is missing!!"
        elif text is None:
            return "Input text is empty!!"

        try:
            translated_text, sentences = translate_text(self.model, text, text_language, target_language)
        except Exception:
            # below is the traceback
            type_, value_, traceback_ = sys.exc_info()
            error_ls = traceback.format_exception(type_, value_, traceback_)
            return error_ls
        return translated_text

    # method which launch Gradio to do MT
    def do_mt(self) -> None:
        url = hyperlink.parse(u"https://github.com/DFKI-NLP/tohyve-services/tree/master/machine_translator")
        css_code = 'div {\
            margin-left:auto;\
            margin-right:auto;\
            width:100%;\
            background-image:url("https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs");\
            background-repeat: no-repeat;\
            background-size: auto;\
            background-position: relative;\
            }'
        title = "Machine Translation Demonstrator"
        description = (
                f"""\n\nThis is the demonstrator for ToHyVe machine translation. To use the online demo please specify the source and target language. Supported languages are:
                'en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi','he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la', 'mi', 
                'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn', 'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw',  'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be', 'tg', 'sd', 
                'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn', 'mt', 'sa', 'lb', 'my', 'bo', 'tl', 'mg', 'as', 'tt', 'haw', 'ln', 'ha', 'ba', 'jw', 'su', 'my', 'ca', 'nl', 'ht', 'lb', 'ps', 'pa', 'ro', 'ro', 'si', 'es'
                \nMore information can be found in the technical documentation ({url.to_text()})."""
            )
        demo = gr.Blocks(css=".gradio-container {background-image:url('https://drive.google.com/uc?export=view&id=1OQwYvj-dxycUq_IyM1t7qlO5LjA40MTs'); background-repeat: no-repeat; background-attachment:absolute; background-position: 30px 40px; background-size: 150px 75px;}")
        
        # interface for microphone
        text_translate = gr.Interface(
            fn=self.get_translation,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="Input Language e.g., de or en", type="text"),
                gr.components.Textbox(placeholder="Input Text ", type="text"),
                gr.components.Textbox(placeholder="Target Language e.g., de or en", type="text")
            ],
            outputs=["textbox"],
            title=title,
            css=css_code,
            description=description,
            # auto_submit_duration=20,
            allow_flagging="never" 
        )

        with demo:
            gr.TabbedInterface([text_translate], ["Text Translation"])

        global app 
        app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)
        # demo.launch(server_name="0.0.0.0", server_port=8000)# to change port number, we can change "server_port" 
        # # demo.launch(server_name="0.0.0.0", server_port=8000, share=True)# to launch it to gradio public server
        
        # uvicorn.run("mt:app", host="0.0.0.0", port=8002, reload=True) # this command will use for development purposes only
        uvicorn.run("mt:app", host="0.0.0.0", port=8002)
        return


