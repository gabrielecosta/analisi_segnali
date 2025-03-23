import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import signal
import sounddevice as sd

#Parameters
T0 = 1      # Signal Period
Ts = 0.001  # Sampling period
t1 = 0    # start time
t2 = 2      # end time
maxK = 500  # Maximum number of harmonics to use for synth


#T0 = 0.0125  # Fundamental period
#Ts = 1/16e3  # Sampling period
#t1 = 0    # Start time
#t2 = 100*T0  # End time
#maxK = 5    # Number of sinusoidal components in the expansion


t = np.arange(t1, t2, Ts)
t = np.arange(t1, t2+Ts, Ts)

# Generate square signal
x = np.zeros(len(t))
ix = np.remainder(np.arange(1,len(t)+1,1),T0/Ts) < np.round(T0/2/Ts)
x[ix] = 1

# Reconstruct the signal
y = 0.5
for k in range(1,maxK,2):
    y = y + 2/np.pi/k * np.cos(2*np.pi/T0 * k * t - np.pi/2)

    plt.plot(t, x, color='red')
    plt.plot(t, y, 'b')
    plt.show(block=False)
    if(k<25):
        plt.pause(1)
    else:
        plt.pause(0.01)
    
    plt.close()

sd.play(y, 1/Ts)
sd.wait()
    



