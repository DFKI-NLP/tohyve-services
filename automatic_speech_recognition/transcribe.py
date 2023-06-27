import gradio as gr
import hyperlink
import time


# ASR Class
class ASR:
    # initialize model and model name
    def __init__(self, pipe, MODEL_NAME) -> None:
        self.pipe = pipe
        self.MODEL_NAME = MODEL_NAME


    # transcreibe method for microphone streaming
    def transcribe_microphone(self, Input_language, Microphone,  state=""):
        if Microphone is None:
            state =""
            return state, state
        if Input_language is None:
            return "ERROR: You didn't set transcribe language code!\n"
        
        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=Input_language, task="transcribe")
        
        # time.sleep(10)
        text = self.pipe(Microphone)["text"]
        state += text + " "
        return state, state

        
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
    def do_asr(self):
        url = hyperlink.parse(u"https://github.com/DFKI-NLP/tohyve-services/tree/master/automatic_speech_recognition")
        css_code = 'div {\
            margin-left:auto;\
            margin-right:auto;\
            width:100%;\
            background-image:url("https://www.dfki.de/fileadmin/user_upload/DFKI/Medien/Logos/Logos_DFKI/DFKI_Logo.png");\
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
        demo = gr.Blocks(css=".gradio-container {background: url('https://www.dfki.de/fileadmin/user_upload/DFKI/Medien/Logos/Logos_DFKI/DFKI_Logo.png'); background-repeat: no-repeat; background-attachment:absolute; background-position: 30px 50px; background-size: 90px 45px;}")
        
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

        demo.launch(server_name="0.0.0.0", server_port=8000)# to change port number, we can change "server_port" 
        # demo.launch(server_name="0.0.0.0", server_port=8000, share=True)# to launch it to gradio public server
        return