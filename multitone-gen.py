import sounddevice as sd    # https://python-sounddevice.readthedocs.io/en/
import numpy as np          # https://numpy.org/doc/stable/reference/
import soundfile as sf      # https://python-soundfile.readthedocs.io/
from typing import Type



class Tone:
    def __init__(self,hertz,seconds=1,amplitude_pct = 80):
        self.seconds = seconds
        self.hertz = hertz
        self.amplitude = amplitude_pct / 100

d = Tone(880.,0.5)
d2 = Tone(2*523.25,0.5)

input_device, output_device = sd.default.device
output_defaults = sd.query_devices(device=output_device)
sr = sd.default.samplerate = output_defaults["default_samplerate"]

def generate_tone(d: Type[Tone]):
    sample_set = np.arange(d.seconds * sr)
    tone = np.sin(2 * np.pi * sample_set * d.hertz / sr)
    tone = tone * d.amplitude
    return tone


tone1 = generate_tone(d)
tone2 = generate_tone(d2)

sr = int(sr)
sf.write('tone1.ogg', tone1, sr, 'VORBIS')
sd.play(tone1)

sf.write('tone2.ogg', tone2, sr, 'VORBIS')
sd.play(tone2)

sf.write('tone3.ogg', tone1+tone2, sr, 'VORBIS')
sd.play(tone1+tone2)
