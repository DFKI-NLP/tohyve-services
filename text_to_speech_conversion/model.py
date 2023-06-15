# import torch

from nemo.collections.tts.models import FastPitchModel
from nemo.collections.tts.models import HifiGanModel, UnivNetModel



# initiate the whisper model
def init_model():
    fast_pitch_dic = {}
    model_dic = {}
    
    # Load FastPitch
    fast_pitch_dic["spec_generator_en"] = FastPitchModel.from_pretrained("tts_en_fastpitch_multispeaker")

    # fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_multispeaker_5")
    fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_singleSpeaker_thorstenNeutral_2210")
    # fast_pitch_dic["spec_generator_de"] = FastPitchModel.from_pretrained("tts_de_fastpitch_singleSpeaker_thorstenNeutral_2102")

    # Load vocoder
    # model_dic["model_en"] = HifiGanModel.from_pretrained(model_name="tts_en_hifitts_hifigan_ft_fastpitch")
    model_dic["model_en"] = UnivNetModel.from_pretrained(model_name="tts_en_libritts_univnet")


    # model_dic["model_de"] = HifiGanModel.From_pretrained(model_name="tts_de_hui_hifigan_ft_fastpitch_multispeaker_5")
    model_dic["model_de"] = HifiGanModel.from_pretrained(model_name="tts_de_hifigan_singleSpeaker_thorstenNeutral_2210")
    # model_dic["model_de"]  = HifiGanModel.from_pretrained(model_name="tts_de_hifigan_singleSpeaker_thorstenNeutral_2102")

    # device = 0 if torch.cuda.is_available() else "cpu"
    device = None
    
    return fast_pitch_dic, model_dic, device

