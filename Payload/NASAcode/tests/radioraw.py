import os
import pickle
import math

import numpy as np
import pandas as pd
import scipy.signal as sig
import matplotlib.pyplot as plt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAWDIR = os.path.join(SCRIPT_DIR, "raw1.iq")

CENTERFREQ = 145e6
FREQDEVI = 0.1e6
BANDWIDTH = 2 * FREQDEVI
NYQUIST = 2e6
demod_freq = 20e3
freq_deviation = 5e3

# load the IQ data from the file
iq_data = np.fromfile(RAWDIR, dtype=np.complex64)
print(iq_data)

# demodulation parameters
f_offset = 0  # frequency offset
mod_index = FREQDEVI / NYQUIST  # modulation index

# NFM demodulation filter
n_taps = 51
taps = sig.firwin(n_taps, BANDWIDTH / NYQUIST, window="hamming")

# mix the signal to baseband
t = np.arange(len(iq_data)) / NYQUIST
mixer = np.exp(-1j * 2 * np.pi * (CENTERFREQ + f_offset) * t)
bb_data = iq_data * mixer

# apply the NFM demodulation filter
audio_data = sig.lfilter(taps, 1, np.abs(bb_data))  # take the absolute value to demodulate the signal

plt.plot(audio_data)
plt.autoscale() 
plt.show()


"""# Load the IQ file into a numpy array
samples = np.fromfile(RAWDIR, np.complex64)
print("raw IQ as comp 64")
print(samples, "\n")

I = [ele.real for ele in samples]
Q = [ele.imag for ele in samples]
x = np.empty(len(I))

plt.plot(samples, 'ro')
plt.title('Demodulated Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.autoscale() 
plt.show()"""

"""# extract real part
x = [ele.real for ele in samples]
# extract imaginary part
y = [ele.imag for ele in samples]
  
# plot the complex numbers
plt.scatter(x, y)
plt.ylabel('Imaginary')
plt.xlabel('Real')
plt.show()"""