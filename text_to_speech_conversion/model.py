import torch
import os

from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel, UnivNetModel



# initiate the whisper model
def init_model():
    fast_pitch_dic = {}
    model_dic = {}
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    # device = "cpu"
    path = "/app/models/"
    
    # Load FastPitch for english language    
    if os.path.exists(path+"en-spec.nemo"):
        fast_pitch_dic["spec_generator_en"] = FastPitchModel.restore_from(restore_path="./models/en-spec.nemo").to(device).eval()
    
    else:
        fast_pitch_dic["spec_generator_en"] = FastPitchModel.from_pretrained("tts_en_fastpitch_multispeaker")
        fast_pitch_dic["spec_generator_en"].save_to("./models/en-spec.nemo")
    
    # Load FastPitch for german language
    if os.path.exists(path+"de-spec.nemo"):
        fast_pitch_dic["spec_generator_de"] = FastPitchModel.restore_from(restore_path="./models/de-spec.nemo").to(device).eval()
    else:
        # fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_multispeaker_5")
        fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_singleSpeaker_thorstenNeutral_2210")
        fast_pitch_dic["spec_generator_de"].save_to("./models/de-spec.nemo")
        # fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_singleSpeaker_thorstenNeutral_2102")

    # Load vocoder for english
    if os.path.exists(path+"en-model.nemo"):
            model_dic["model_en"] = UnivNetModel.restore_from(restore_path="./models/en-model.nemo").to(device).eval()
    else:
         # model_dic["model_en"] = HifiGanModel.from_pretrained(model_name="tts_en_hifitts_hifigan_ft_fastpitch")
        model_dic["model_en"] = UnivNetModel.from_pretrained(model_name="tts_en_libritts_univnet")
        model_dic["model_en"].save_to("./models/en-model.nemo")
    
    # Load vocoder for german
    if os.path.exists(path+"de-model.nemo"):
        model_dic["model_de"] = UnivNetModel.restore_from(restore_path="./models/de-model.nemo").to(device).eval()
    else:
        # model_dic["model_de"] = HifiGanModel.From_pretrained(model_name="tts_de_hui_hifigan_ft_fastpitch_multispeaker_5")
        model_dic["model_de"] = HifiGanModel.from_pretrained(model_name="tts_de_hifigan_singleSpeaker_thorstenNeutral_2210")
        model_dic["model_de"].save_to("./models/de-model.nemo")   
        # model_dic["model_de"]  = HifiGanModel.from_pretrained(model_name="tts_de_hifigan_singleSpeaker_thorstenNeutral_2102")

    
    return fast_pitch_dic, model_dic

