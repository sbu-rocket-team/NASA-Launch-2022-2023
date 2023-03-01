import os
import wave

import numpy as np
import aprslib as aprs
from scipy.io import wavfile as swav


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(SCRIPT_DIR, "raw1.iq")


CENTERFREQ = 145e6
FREQDEVI = 0.1e6
BANDWIDTH = 2 * FREQDEVI
NYQUIST = 2e6
demod_freq = 20e3
freq_deviation = 5e3

iq_data = np.fromfile(RAWDIR, dtype='complex64')

audio_data = np.real(iq_data).astype(np.float32)
print(audio_data)
# between 10 and 15 seconds, sample rate is either 14000, 15000, 17000, 22050, 24000, or 30000
sample_rate = 14000

swav.write('output1.wav', sample_rate, audio_data)

WAVDIR = os.path.join(SCRIPT_DIR, "output1.wav")

# Load the WAV file
samplerate, data = swav.read(WAVDIR)

print(data)
"""
# Decode the APRS packets from the audio
aprs = aprs.IS('N0CALL')
aprs.decode(audio_data, sample_rate)

# Print the decoded packets
for packet in aprs.unpack():
    print(packet)"""