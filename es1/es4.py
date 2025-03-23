'''
Sintetizzare l'onda quadra usando i seguenti parametri:
1) numero di armoniche 4
2) coefficienti: a0=0.5, a1=-1j/pi, a2=0, a3=-1j/3pi
3) F0=25Hz
'''

import numpy as np
import matplotlib.pyplot as plt

def compute_coeffs(N=4):
    coeffs = {}
    coeffs[0] = 0.5
    for i in range(1, N):
        if i % 2 == 0:
            coeffs[i] = 0.0
        else:
            coeffs[i] = -1j / (i * np.pi)
    return coeffs


def synthesize_square_wave(t, F0, coeffs):
    """
    Sintetizza un'onda quadra con le armoniche date.

    Parametri:
    - t: array di tempi
    - F0: frequenza fondamentale
    - coeffs: dizionario {indice: coefficiente complesso}
    
    Ritorna:
    - Segnale ricostruito

    x(t) = a0 + 2 Re{ sum (k=1,N) a_k e^{j2pikf0t} }
    Quindi prima genero un certo numero di valori temporali, più fitti sono più il valore
    sembra quasi continuo.
    a0 è la componente in continua del segnale periodico
    """
    wave = np.full_like(t, np.real(coeffs[0]), dtype=np.float64)  # Componente DC (a0)
    # print(wave)
    cum_sum = 0
    for n, a_n in coeffs.items():
        # sommo ogni componente di ogni armonica, scorrendo i coefficienti
        # la prima armonica è già stata sommata
        # dopodiché moltiplico per t che in realtà sarebbe un valore discreto
        if n == 0:
            continue
        cum_sum += np.real(a_n * np.exp(1j * 2 * np.pi * n * F0 * t))
    wave = wave + 2 * cum_sum # prendendo solo la parte reale, devo moltiplicare per due questa
    return wave

def plot_square_wave(t, y, F0):
    """
    Plotta l'onda quadra sintetizzata e l'onda quadra ideale.

    Parametri:
    - t: array dei tempi
    - y: segnale sintetizzato con la serie di Fourier
    - F0: frequenza fondamentale dell'onda quadra
    """
    # Generazione dell'onda quadra ideale tra 0 e 1
    square_wave = 0.5 * (np.sign(np.sin(2 * np.pi * F0 * t)) + 1)

    plt.figure(figsize=(8, 5))
    plt.plot(t, y, label="Onda quadra sintetizzata", color='b', linestyle='-')
    plt.plot(t, square_wave, label="Onda quadra ideale", color='r', linestyle='--', alpha=0.7)
    
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ampiezza")
    plt.title("Sintesi di un'onda quadra con serie di Fourier")
    plt.grid(True)
    plt.legend()
    plt.show()

# Parametri
F0 = 25  # Frequenza fondamentale
T = 1 / F0  # Periodo fondamentale
t = np.linspace(0, 2*T, 1000)  # 2 periodi con 500 campioni
N = 16 # numero armoniche

### se volessi invece avere 8 armoniche, dovrei considerare che sono complesse e coniugate
# Coefficienti armonici
coeffs = compute_coeffs(N=N)
# Generazione dell'onda quadra sintetizzata
y = synthesize_square_wave(t, F0, coeffs)

plot_square_wave(t,y,F0)
