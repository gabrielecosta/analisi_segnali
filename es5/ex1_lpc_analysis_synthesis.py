# Initialization
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy
import numpy as np
import librosa
import scipy.signal as sig
import scipy.signal.windows as windows
from scipy.io.wavfile import write


def lpc_analysis_synthesis(s, frame_length=480, hop_size=240, lpc_order=12, window_type='hamming'):
    
    if window_type == 'rectangular':
        window = np.ones(frame_length)
    elif window_type == 'hamming':
        window = windows.hamming(frame_length)
    elif window_type == 'hann':
        window = windows.hann(frame_length)
    else:
        raise ValueError("Unsupported window type. Choose 'rectangular' or 'hamming'.")
    Buffer = np.zeros(hop_size)
    num_frames =  int(np.floor((len(s)-frame_length)/hop_size)+1)
    synthesized_signal = np.zeros_like(s) # buffer contaning the synthesized signal
    tosave = np.arange(0,hop_size,1)
    # analysis frame-by-frame
    for i in range(num_frames):
        start = i * hop_size
        end = min(start + frame_length, len(s))
        frame = np.zeros(frame_length)
        frame[:end-start] = s[start:end]  # Zero-padding if needed
        sigLPC = frame * window
        en = np.sum(sigLPC**2) # short-time energy of the input
        # LPC analysis
        a = librosa.lpc(sigLPC, order=lpc_order)
        # Compute the Gain
        corr = np.correlate(sigLPC, sigLPC, mode='full')
        pos_corr = corr[corr.size // 2:] # positive axes only
        G  = np.sqrt(np.sum(a*pos_corr[:lpc_order+1]))

        # Compute residual (prediction error signal)
        ex = scipy.signal.lfilter(a, [1.0], sigLPC)  # exitation obtained through inverse filtering

        # Synthesis
        s_recon = scipy.signal.lfilter(G, a, ex)
        ens = np.sum(s_recon**2) # get the short-time energy of the output
        g = np.sqrt(en/ens) # normalizing factor
        s_recon = s_recon*g # energy compensation
        s_recon[:hop_size] = s_recon[:hop_size] + Buffer # overalp and add
        synthesized_signal[tosave] = s_recon[:hop_size] # save the first part of the frame
        Buffer = s_recon[hop_size:frame_length] # buffer the rest of the frame
        tosave = tosave+hop_size

    return synthesized_signal





# Load the waveform and plot it
filename = 'speechsample.wav'

data, fs = librosa.load(filename, sr=16000)

'''
#Scipy wav.read reads wav files as 16 bit integers from -32768 to 32767. We need to transform it into floats from -1 to 1.
fs, data = wavfile.read(filename=filename)

if type(data[0]) == np.int16:
    data = np.divide(data,32768,dtype=np.float32)
# 1.2. Make sure the sampling rate is 16kHz. Resample if not 16kHz
if not (fs == 16000):
    data = sig.resample_poly(data,16000,fs)
    fs = 16000
'''

lpc_order = 24
reconstructed_signal = lpc_analysis_synthesis(data, 
                                              frame_length=480, 
                                              hop_size=240, 
                                              lpc_order=lpc_order, 
                                              window_type='hann')

# Save as WAV file
out_filename = 'synthesized_speechsample_lpc' + str(lpc_order) + '.wav'
write(out_filename, fs, (reconstructed_signal * 32767).astype(np.int16))

t = np.linspace(0, len(data)/fs, len(data))
plt.figure(figsize=(10, 4))
plt.subplot(2, 1, 1)
plt.plot(t, data)
plt.xlabel('time (in sec)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.title('Original Signal')

plt.subplot(2, 1, 2)
plt.plot(t, reconstructed_signal, 'r')
plt.xlabel('time (in sec)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.title('Synthetized Signal - LPC order 24')

plt.show()

mse = np.sum((data-reconstructed_signal)**2,axis=0)/data.shape[0]
print(f'MSE: ', mse)




