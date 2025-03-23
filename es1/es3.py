# caricare la forma d'onda con librosa
import scipy 
import scipy.io
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import librosa

# 1. Get the file path to an included audio example
filename = 'sentence.wav'
# 2. Load the audio as a waveform `y`, Store the sampling rate as `sr`
signal, sr = librosa.load(filename)
# 3. stampa dei valori
# contenuti
print(f"numero di campioni = {signal.shape[0]}")
print(f"frequenza di campionamento: {sr}")
length = signal.shape[0] / sr
print(f"length (durata)= {length}s")

# procediamo a normalizzare la traccia audia per includerla tra -1 ed 1
max = np.max(np.abs(signal))
data = signal / max

# # plotting
time = np.linspace(0, length, data.shape[0])   # genera
plt.figure(figsize=(8, 5))
plt.plot(time, data, label="Waveform")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()