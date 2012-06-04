#!/usr/bin/env python

import subprocess
import json
import math

import numpy as np
import matplotlib.pyplot as plt

json_data = subprocess.Popen(['bo-data', '-i', 'AndreasW_20120528.bor', '-l', '-j', '--start=-1'], stdout=subprocess.PIPE).communicate()[0]
data = json.loads(json_data)
dt = data[0][6]/1e6 # time in ms
data_array = data[0][10]

n = len(data_array[0])

times = np.arange(0.0, n*dt, dt)
x_array = np.fromiter(data_array[0], np.float32)
y_array = np.fromiter(data_array[1], np.float32)

plt.figure(1)
plt.subplot(211)
plt.plot(times, x_array)
plt.plot(times, y_array)

time_array= x_array + 1j * y_array

frequency_array = np.fft.fft(time_array)

frequencies = np.fft.fftfreq(n) / dt

amplitudes = np.absolute(frequency_array)
phases = np.unwrap(np.angle(frequency_array))

plt.subplot(212)
plt.plot(frequencies, amplitudes)
plt.plot(frequencies, phases)
plt.show()

