import pyaudio
import numpy as np

# Set parameters
center_freq = 100e6
sample_rate = 2e6
audio_rate = 48e3

# Load IQ samples from file
samples = np.fromfile('input_file.iq', dtype='uint16')

# Convert to complex samples
samples = samples.astype('float32') - 2**15
samples = samples[::2] + 1j*samples[1::2]

# Downconvert to audio frequency range
t = np.arange(samples.size) / sample_rate
samples *= np.exp(-1j*2*np.pi*center_freq*t)

# Decimate to audio sample rate
n = int(sample_rate / audio_rate)
samples = samples[::n]

# Extract audio signal
signal = np.abs(samples)

# Normalize to range [-1, 1]
signal /= np.max(signal)

# Create PyAudio object
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=int(audio_rate), output=True)

# Write audio data to stream
stream.write(signal.tobytes())

# Close audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio object
p.terminate()
