## caricare la forma d'onda sentence.wav, usare scipy.io
import scipy 
import scipy.io
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

# lettura
wav_name = 'sentence.wav'
samplerate, data = wavfile.read(wav_name)

# contenuti
print(f"numero di campioni = {data.shape[0]}")
print(f"frequenza di campionamento: {samplerate}")
length = data.shape[0] / samplerate
print(f"length (durata)= {length}s")

# procediamo a normalizzare la traccia audia per includerla tra -1 ed 1
max = np.max(np.abs(data))
data = data / max

# # plotting
time = np.linspace(0, length, data.shape[0])   # genera
plt.figure(figsize=(8, 5))
plt.plot(time, data, label="Waveform")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
