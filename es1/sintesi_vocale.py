import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# I poli forniti
p1 = 0.963 + 0.116j
p2 = 0.619 + 0.719j
p3 = 0.370 + 0.874j

# Aggiungo i coniugati complessi per avere un filtro con coefficienti reali
poles = [p1, np.conjugate(p1), p2, np.conjugate(p2), p3, np.conjugate(p3)]

# Parametri del segnale
f0 = 80  # frequenza fondamentale in Hz
fs = 16000  # frequenza di campionamento in Hz
duration = 2.0  # durata in secondi

# nella modalità corretta

# Creo il filtro dai poli
def create_filter_from_poles(poles, gain=1.0):
    # Costruisco il polinomio del denominatore dai poli
    a = np.real(np.poly(poles))
    # Per un filtro solo-poli, il numeratore è semplicemente il guadagno
    b = [gain]
    return b, a

b, a = create_filter_from_poles(poles)

# Genera l'eccitazione (treno di impulsi per la voce vocalizzata)
t = np.arange(0, duration, 1/fs)
n_samples = len(t)
pitch_period = int(fs / f0)  # periodo in campioni
excitation = np.zeros(n_samples)
for i in range(0, n_samples, pitch_period):
    if i < n_samples:
        excitation[i] = 1.0

# Applica il filtro all'eccitazione
output = signal.lfilter(b, a, excitation)

# Normalizza l'output
output = output / np.max(np.abs(output))

# Visualizza i risultati
plt.figure(figsize=(12, 10))

plt.subplot(4, 1, 1)
plt.plot(t[:500], excitation[:500])
plt.title('Segnale di eccitazione (primi 500 campioni)')
plt.grid(True)

plt.subplot(4, 1, 2)
plt.plot(t[:500], output[:500])
plt.title('Segnale sintetizzato (primi 500 campioni)')
plt.grid(True)

plt.subplot(4, 1, 3)
plt.plot(t[:2000], output[:2000])
plt.title('Segnale sintetizzato (primi 2000 campioni)')
plt.grid(True)

plt.subplot(4, 1, 4)
w, h = signal.freqz(b, a, worN=1024)
plt.plot(w/np.pi*fs/2, 20*np.log10(np.abs(h)))
plt.title('Risposta in frequenza del filtro')
plt.xlabel('Frequenza (Hz)')
plt.ylabel('Ampiezza (dB)')
plt.grid(True)
plt.xlim(0, fs/2)

plt.tight_layout()
plt.show()

# Salva il segnale audio
from scipy.io import wavfile
wavfile.write('segnale_vocale_sintetizzato.wav', fs, (output*32767).astype(np.int16))

# Stampa i coefficienti del filtro
print("Coefficienti del numeratore (b):", b)
print("Coefficienti del denominatore (a):", a)


### da qui manca andare a calcolare la FFT
'''
Pipeline:
- per ogni polo calcolare la funzione di trasferimento
- per ogni funzione di trasfermento fare poi il prodotto tra i filtri
- quindi generare un treno di impulsi
- infine andare a creare il filtro con i coefficienti ottenuti dalla convoluzione dei singoli filtri
- quindi dare in input il treno di impulsi al filtro
- il risultato poi andrebbe portato nel dominio della frequenza tramite dft


Se avessi le formanti anziché i poli:
- trovo r
- trovo theta
- p = [r * np.exp(1j*theta), r * np.exp(-1j*theta)]
'''