import sys
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks


input = sys.stdin.read().split()
data = []
for i in range(len(input) // 2):
    data.append((input[i * 2], input[i * 2 + 1]))
timestamps = []
signal = []
for x, y in data:
    timestamps.append(x)
    signal.append(y)


fft = rfft(signal)
frequencies = rfftfreq(len(signal), d=1/8000)
peaks, _ = find_peaks(np.abs(fft), height=1)
transmitter_frequencies = frequencies[peaks]


for freq in transmitter_frequencies:
    print(f"{freq:.2f}", end=" ")