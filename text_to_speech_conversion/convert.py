import soundfile as sf
import numpy as np

# TTS Class
class TTS:
    # initialize fast_pitch, model and device
    def __init__(self, spec_generator, model, data_dir,  device=None) -> None:
        self.spec_generator = spec_generator
        self.model = model
        self.device = device
        self.data_dir = data_dir


    # method which convert text into speech
    def do_tts(self, text) -> None:
        parsed = self.spec_generator.parse(text)
        spectrogram = self.spec_generator.generate_spectrogram(tokens=parsed)
        audio = self.model.convert_spectrogram_to_audio(spec=spectrogram)

        sf.write(self.data_dir+"/speech.wav", np.ravel(audio.detach().numpy()), 22050)
        return