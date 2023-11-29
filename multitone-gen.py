#!/usr/bin/env python3
#
import sys
import sounddevice as sd    # https://python-sounddevice.readthedocs.io/en/
import numpy as np          # https://numpy.org/doc/stable/reference/
import soundfile as sf      # https://python-soundfile.readthedocs.io/
from typing import Type
import json

class Tone:
    def __init__(self,hertz,seconds=1,amplitude_pct = 80):
        self.seconds = seconds
        self.hertz = hertz
        self.amplitude = amplitude_pct / 100

input_device, output_device = sd.default.device
output_defaults = sd.query_devices(device=output_device)
sd.default.samplerate = output_defaults["default_samplerate"]
sr = int(sd.default.samplerate)

def generate_tone(d: Type[Tone]):
    sample_set = np.arange(d.seconds * sr)
    tone = np.sin(2 * np.pi * sample_set * d.hertz / sr)
    tone = tone * d.amplitude
    return tone

with open('tones.json','r') as json_file:
    data = json.load(json_file)

for x in data['tone_data']:
    mtf_data = x['mtf_data']
    for mtf_tone in mtf_data:
        mt = [ Tone(i,x['duration'],x['amplitude_pct']) for i in mtf_tone ]
        # construct file name from frequency values
        ss = [ str(t.hertz) for t in mt ]
        output_filename = f"./oup/mt_{'-'.join(ss)}.ogg"
        # generate each tone separately then combine
        audio_tones = [ generate_tone(t) for t in mt ]
        final_tone = np.average(np.asanyarray(audio_tones),axis=0)
        # write mixed tones as multitone frequency to filename
        sf.write(output_filename, final_tone, sr, 'VORBIS')
        print(f'Wrote file "{output_filename}"...', file=sys.stderr)


















