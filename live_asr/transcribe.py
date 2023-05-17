import gradio as gr


# ASR Class
class ASR:
    # initialize model and model name
    def __init__(self, pipe, MODEL_NAME) -> None:
        self.pipe = pipe
        self.MODEL_NAME = MODEL_NAME

    # transcreibe method for both microphone streaming and audio file upload
    def transcribe(self, transcribe_language, microphone, file_upload):
        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(language=transcribe_language, task="transcribe")
        warn_output = ""
        if (microphone is not None) and (file_upload is not None):
            warn_output = (
                "WARNING: You've uploaded an audio file and used the microphone. "
                "The recorded file from the microphone will be used and the uploaded audio will be discarded.\n"
            )
        elif (microphone is None) and (file_upload is None):
            return "ERROR: You have to either use the microphone or upload an audio file"
        elif transcribe_language is None:
            return "ERROR: You didn't set transcribed language code!\n"

        file = microphone if microphone is not None else file_upload
        text = self.pipe(file)["text"]

        return warn_output + text


    # method which launch Gradio to do ASR
    def do_asr(self):
        demo = gr.Blocks()
        mf_transcribe = gr.Interface(
            fn=self.transcribe,
            inputs=[
                gr.components.Textbox(lines=1, placeholder="Write language code here", type="text"),
                gr.components.Audio(source="microphone", type="filepath"),
                gr.components.Audio(source="upload", type="filepath"),
            ],
            outputs="text",
            title="DFKI ASR: Transcribe Audio",
            description=(
                "Transcribe long-form microphone or audio inputs with the click of a button! Demo uses the the fine-tuned"
                f" checkpoint [{self.MODEL_NAME}](https://huggingface.co/{self.MODEL_NAME}) and 🤗 Transformers to transcribe audio files"
                " of arbitrary length."
            ),
            allow_flagging="never",
        )
        with demo:
            gr.TabbedInterface([mf_transcribe], ["Transcribe Audio"])

        demo.launch(server_name="0.0.0.0", server_port=8000) # to change port number, we can change "server_port" 

        return