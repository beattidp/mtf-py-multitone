#!/usr/bin/env python3
#
import os
import sys
import sounddevice as sd    # https://python-sounddevice.readthedocs.io/en/
import numpy as np          # https://numpy.org/doc/stable/reference/
import soundfile as sf      # https://python-soundfile.readthedocs.io/
from typing import Type
from functools import singledispatchmethod
import json

OUTPUT_DIR = "./output"

class Tone:
    @singledispatchmethod
    def __init__(self,hertz,seconds=1,amplitude=0.80):
        self.seconds = seconds
        self.hertz = hertz
        self.amplitude = amplitude

    @__init__.register(tuple)
    def _(self,arg):
        if not len(arg) == 3:
            sys.exit("Tuple not 3 items.")
        self.hertz, self.amplitude, self.seconds = arg

#raise Exception
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
        print([i for i in mtf_tone])
        tt = []
        # construct as tuples of 3 as (frequency, amplitude, duration)
        for i in mtf_tone:
            if type(i) is list:
                i.append(x['duration']); t = tuple(i)
            else:
                t = tuple([i,x['amplitude'],x['duration']])
            tt.append(t)
        # build the list of tones
        mt = [ Tone(i) for i in tt ]
        # construct file name from frequency values
        ss = [ str(t.hertz) for t in mt ]
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_filename = f"{OUTPUT_DIR}/mt_{'-'.join(ss)}.ogg"
        # generate each tone separately then combine
        audio_tones = [ generate_tone(t) for t in mt ]
        final_tone = np.average(np.asanyarray(audio_tones),axis=0)
        # write mixed tones as multitone frequency to filename
        sf.write(output_filename, final_tone, sr, 'VORBIS')
        print(f'Wrote file "{output_filename}"...', file=sys.stderr)


















