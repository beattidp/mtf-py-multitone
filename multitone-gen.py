import sounddevice as sd    # https://python-sounddevice.readthedocs.io/en/
import numpy as np          # https://numpy.org/doc/stable/reference/
import soundfile as sf      # https://python-soundfile.readthedocs.io/
from typing import Type
import math


class Tone:
    def __init__(self,hertz,seconds=1,amplitude_pct = 80):
        self.seconds = seconds
        self.hertz = hertz
        self.amplitude = amplitude_pct / 100

d1 = Tone(880.,0.5) #A5
d2 = Tone(1046.5,0.5) #C6
d3 = Tone(1244.51,0.5) # E6♭
d3 = Tone(1174.66,0.5) # D6

input_device, output_device = sd.default.device
output_defaults = sd.query_devices(device=output_device)
sd.default.samplerate = output_defaults["default_samplerate"]
sr = int(sd.default.samplerate)

def generate_tone(d: Type[Tone]):
    sample_set = np.arange(d.seconds * sr)
    tone = np.sin(2 * np.pi * sample_set * d.hertz / sr)
    tone = tone * d.amplitude
    return tone


t1 = generate_tone(d1)
t2 = generate_tone(d2)
t3 = generate_tone(d3)

final_tone = np.average(np.array([t1,t2,t3]),axis=0)

sf.write('tone-t1.ogg', t1, sr, 'VORBIS')

sf.write('tone-t2.ogg', t2, sr, 'VORBIS')

sf.write('tone-t3.ogg', t3, sr, 'VORBIS')

sf.write('tone-final.ogg', final_tone, sr, 'VORBIS')

sd.play(final_tone)
