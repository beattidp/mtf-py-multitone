import sounddevice as sd
import numpy as np



class Tone:
    def __init__(self,hertz,seconds=1,amplitude_pct = 80):
        self.seconds = seconds
        self.hertz = hertz
        self.amplitude = amplitude_pct / 100

d = Tone(880,0.5)

input_device, output_device = sd.default.device
output_defaults = sd.query_devices(device=output_device)
sr = sd.default.samplerate = output_defaults["default_samplerate"]

sample_set = np.arange(d.seconds * sr)
tone = np.sin(2 * np.pi * sample_set * d.hertz / sr)
tone = tone * d.amplitude

sd.play(tone,sr)
