import os 
import logging
import torch 
from transformers import pipeline

# import whisper
# from whisper.utils import WriteVTT


# initialize openai/whisper
# def init_whisper():
#     model = whisper.load_model("medium")
#     return model


# initialize huggingface's openai/whisper model
def init_huggingface_whisper():
    MODEL_NAME = "openai/whisper-medium" #this always needs to stay in line 8 :D sorry for the hackiness
    device = 0 if torch.cuda.is_available() else "cpu"
    pipe = pipeline(
        task="automatic-speech-recognition",
        model=MODEL_NAME,
        chunk_length_s=30,
        device=device,
    )
    # pipe.model.config.forced_decoder_ids = pipe.tokenizer.get_decoder_prompt_ids(language="de", task="transcribe")
    return pipe


# extract text from a given audio
def transcribe_audio(audio_path, whisper_model, source_language, is_english):    
    if is_english:
        whisper_model.model.config.forced_decoder_ids = whisper_model.tokenizer.get_decoder_prompt_ids(language="en", task="translate")
    else:
        whisper_model.model.config.forced_decoder_ids = whisper_model.tokenizer.get_decoder_prompt_ids(language=source_language, task="transcribe")
    text = whisper_model(audio_path)
    # print(text["text"])
    return text


# extract text from a given audio
def audio_converter(audio_path, whisper_model, is_eng):
    # audio = whisper.load_audio(audio_path)
    # audio = whisper.pad_or_trim(audio)
    
    # # make log-Mel spectrogram and move to the same device as the model
    # mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

    # # detect the spoken language
    # _, probs = whisper_model.detect_language(mel)
    # language_whisper = max(probs, key=probs.get)

    # print(language_whisper)
    
    # options = dict(language=language_whisper, beam_size=5, best_of=5)
    

    if not os.path.exists(audio_path):
        logging.info("File not found!")
    else:
        if is_eng == 1:
            options = dict(beam_size=5, best_of=5)
            translate_options = dict(task="translate", **options)
            result = whisper_model.transcribe(audio_path,**translate_options)
        else:
            # options = dict(beam_size=5, best_of=5)
            # translate_options = dict(temperature=0, **options)
            # translate_options = dict(no_speech_threshold=0.5, logprob_threshold= -1.0, compression_ratio_threshold=0.6)
            # result = whisper_model.transcribe(audio_path, **translate_options)
            
            # transcribe_options = dict(task="transcribe", **options)
            # result = whisper_model.transcribe(audio_path, **transcribe_options)
            result = whisper_model.transcribe(audio_path, language="German")
            # load audio and pad/trim it to fit 30 seconds
            # audio = whisper.load_audio(audio_path)
            # audio = whisper.pad_or_trim(audio)

            # # make log-Mel spectrogram and move to the same device as the model
            # mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

            # # detect the spoken language
            # _, probs = whisper_model.detect_language(mel)
            # print(f"Detected language: {max(probs, key=probs.get)}")

            # # decode the audio
            # # options = whisper.DecodingOptions()
            # result = whisper.decode(whisper_model, mel)
        # print(result["text"])
       
    return result


# add subtitles into a video
def create_subtitle_video(audio_path, video_path, result):
    subtitle_path = audio_path.replace(".mp3", ".vtt")
    with open(subtitle_path, "w") as vtt:
    #   print(result, type(result), type(result["text"]))
      WriteVTT("./saved_audio/").write_result(result, file=vtt)

    output_video = subtitle_path.replace(".vtt", "_subtitled.mp4")
    # print(output_video, video_path, subtitle_path, output_video)
    os.system(f"ffmpeg -y -i {video_path} -vf subtitles={subtitle_path} {output_video}")

    return output_video
