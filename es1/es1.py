'''
Usando le librerie matplotlib e numpy, generare e rapresentare graficmente
la funzione coseno con i seguenti parrametri:
- periodo di campionamento 0.005 s
- numero di punti per i quali calcolare la forma d'onda: 15
- inizio temporale -6
- fine temporale: 9
- frequenza fondamentale: 40 Hz ---> 0.025 s 

Per poter fare l'esercizio quello che devo fare è generare campioni con frequenza di campionamento 1/ts=200Hz
a partire da -6 a 9. Dopo aver generato questi punti moltiplico per Ts ottenendo la frequenza
normalizzata nTs. Ottengo tutti i valori da -6 a 9 con passo di campionamento.
Dopodiché devo andare a generare i punti, andando a selezionare 15 punti dall'intervallo selezionato
considerando: cos(2*pi*f0*t), dove t varia da -6 a 9 prendendo esattamente N punti
'''

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def sampling_values(ts=0.005, N=15, start=-6, stop=-9):
    '''
    ritorna i valori campionati a partire da start ad end, con un determinato numero
    ed una frequenza di campionamento
    '''
    t = np.linspace(start, stop, N, endpoint=False)
    t = t * ts # tempo normalizzato
    return t

def cos_f(vals, f=40):
    '''
    poi prendo i valori di t
    '''
    # cos(2pift*Ts)
    ts = np.array(vals)
    y = np.cos(2*np.pi*f*ts)
    return y


def plot_cos(x, y):
    """
    Funzione per plottare una serie di valori.

    Parametri:
    - x: array-like, valori sull'asse X
    - y: array-like, valori sull'asse Y
    """
    # Valori predefiniti
    title = "Grafico dei valori"
    xlabel = "Frequenze"
    ylabel = "Valori coseno"
    color = 'b'          # Colore della linea (blu)
    marker = 'o'         # Marker per i punti
    linestyle = '-'      # Stile della linea

    # Creazione del grafico
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color=color, marker=marker, linestyle=linestyle, label="Dati")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


# x = sampling_values(ts=0.005, N=15, start=-6, stop=9)
x = sampling_values(ts=0.005, N=150, start=-6, stop=9)
y = cos_f(vals=x, f=40)
plot_cos(x=x, y=y)


'''
pipeline:
    - prima genero i campioni tramite np.linspace da start ad end, un certo numero di campioni
      N, ciò implica andaer a campionare con la frequenza di campionamento (specificata dall'utente fs)
    - calcolo i valori della funzione coseno con la frequenza fondamentale come cos(2pif0*nTs), dove i valori
      di nTs sono calcolati come la funzione cno numpy
'''
