import gradio as gr


# ASR Class
class ASR:
    # initialize model and model name
    def __init__(self, pipe, MODEL_NAME) -> None:
        self.pipe = pipe
        self.MODEL_NAME = MODEL_NAME

    # transcreibe method for both microphone streaming and audio file upload
    def transcribe(self, Input_language, Microphone, File_upload):
        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=Input_language, task="transcribe")
        warn_output = ""
        if (Microphone is not None) and (File_upload is not None):
            warn_output = (
                "WARNING: You've uploaded an audio file and used the microphone. "
                "The recorded file from the microphone will be used and the uploaded audio will be discarded.\n"
            )
        elif (Microphone is None) and (File_upload is None):
            return "ERROR: You have to either use the microphone or upload an audio file"
        elif Input_language is None:
            return "ERROR: You didn't set transcribed language code!\n"

        file = Microphone if Microphone is not None else File_upload
        text = self.pipe(file)["text"]

        return warn_output + text


    # method which launch Gradio to do ASR
    def do_asr(self):
        # demo = gr.Blocks()
        # mf_transcribe = gr.Interface(
        demo = gr.Interface(
        
            fn=self.transcribe,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="e.g. de or en", type="text"),
                gr.components.Audio(source="microphone", type="filepath"),
                gr.components.Audio(source="upload", type="filepath"),
            ],
            outputs="text",
            title="Automatic Speech Recognition Demonstrator",
            description=(
                """This is the demonstrator for multilingual automatic speech recognition for the ToHyVe project. It supports static file upload (mp3 format) and audio streaming from the local microphone. This are the supported languages:
                'en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca', 'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi','he', 'uk', 'el', 'ms', 'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la', 'mi', 
                'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn', 'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw',  'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be', 'tg', 'sd', 
                'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn', 'mt', 'sa', 'lb', 'my', 'bo', 'tl', 'mg', 'as', 'tt', 'haw', 'ln', 'ha', 'ba', 'jw', 'su', 'my', 'ca', 'nl', 'ht', 'lb', 'ps', 'pa', 'ro', 'ro', 'si', 'es'"""
            ),
            allow_flagging="never",
            # css="body {background-color: white}"
            auto_submit=True,
        )
        # with demo:
        #     gr.TabbedInterface([mf_transcribe], ["Transcribe Audio"])

        demo.launch(server_name="0.0.0.0", server_port=8000) # to change port number, we can change "server_port" 

        return