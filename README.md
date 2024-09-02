# tohyve-services

This project contains individual modules created for the ToHyve-project. 
All modules are also provided as docker containers for higher usability. 

The individual models encompass:

* Multilingual ***Automatic Speech Recognition (ASR)*** *(automatic_speech_recognition)*
* Multilingual ***Bitext Alignment*** *(DFKI_NLU_DOCKER/bi_text_alignment)*
* Multilingual ***Text to Text*** translation / ***Text to Speech*** translation *(DFKI_NLU_DOCKER/machine_translator)*
* Multilingual ***Text To Speech conversion (TTS)***  *(text_to_speech_conversion)*
* Multilingual ***ASR (Video (without caption) -> Extract Audio -> Extract Text from Audio -> Translate that Text into English, German -> Add Translated Texts as a caption of inserted Video)*** *(DFKI_NLU_DOCKER/dfki_asr)*
* **Bite Cutter**: Tool to support the TTS service. It accepts longer input than the TTS service does, cuts them in smaller peaces and resends them to the service. Functions as a wrapper container.

## Example Usage

To use the stream capabilities of ASR and then integrate with other services we created a small python script [`request_stream_demo.py`](./request_stream_demo.py).

To use it:
```
python -m request_stream_demo
```
N.B: Plase open the script and change the variable values with your actual values and to use TTS audio don't forget to uncomment `tts_audio_encodings`(line 85). The TTS encodings are commented out for better visibility.
