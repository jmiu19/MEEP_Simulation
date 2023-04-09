import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

seps = [1 ,0.5, 0.2, 0.1, 0.075, 0.006, 0.005] # unit in micron

## detected freq, 
# first and second are leaky modes, third is the even mode, fourth is odd mode
# sorted in seps
detected_freqs = [[], [], [], []] 
detected_freqs[0] = [1.23033, 1.23126, 1.24394, 1.25204, 1.25430, 1.25617, 1.25676]
detected_freqs[1] = [1.23010, 1.23316, 1.24473, 1.25240, 1.25421, 1.25590, 1.25655]
detected_freqs[2] = [1.371000, 1.368604, 1.357807, 1.341833, 1.333567, 1.327738, 1.320946]
detected_freqs[3] = [1.371000, 1.372965, 1.380948, 1.387232, 1.389046, 1.390370, 1.390821]

res_lambda = [np.round(1/np.array(detected_freqs[i]),5) for i in range(len(detected_freqs))]

Im_freq = [[], [], [], []]
Im_freq[0] = [0.005, 0.005, 0.005 ,0.0055, 0.0055, 0.0054, 0.0049]
Im_freq[1] = [0.005, 0.008, 0.005, 0.0053, 0.0053, 0.0052, 0.0055]
Im_freq[2] = [0.0001, 0.000163, 0.000263, 0.000361, 0.000412, 0.00045, 0.00050]
Im_freq[3] = [0.0001, 0.000110, 0.000114, 0.000138, 0.000145, 0.00015, 0.00015]

Im_freq_errors = [[], [], [], []]
Im_freq_errors[0] = [0.0005 for i in range(len(seps))]
Im_freq_errors[1] = [0.0005 for i in range(len(seps))]
Im_freq_errors[2] = [0.000005 for i in range(len(seps))]
Im_freq_errors[3] = [0.000005 for i in range(len(seps))]

Qs = [[], [], [], []]
Qs[0] = [100, 127 ,110 ,110, 110, 114, 126]
Qs[1] = [100, 110, 110, 110, 110, 120, 113]
Qs[2] = [4500, 4206, 2580, 1860, 1610, 1470, 1320]
Qs[3] = [4500, 6250, 6040, 5010, 4770, 4600, 4550]

Q_errors = [[], [], [], []]
Q_errors[0] = [10 for i in range(len(seps))]
Q_errors[1] = [10 for i in range(len(seps))]
Q_errors[2] = [80 for i in range(len(seps))]
Q_errors[3] = [80 for i in range(len(seps))]

# Q factor plot
fig, ax = plt.subplots(figsize = (18,12), dpi = 80)
colors = ['red', 'blue', 'green', 'orange']
names = ['leaky 1', 'leaky 2', 'even', 'odd']
for i in range(len(Qs)):
    ax.errorbar(seps, Qs[i], yerr = Q_errors[i], color = colors[i], fmt = 'o')
    ax.scatter(seps, Qs[i], color = colors[i])
    ax.plot(seps, Qs[i], color = colors[i], label = names[i])
    for j in range(len(seps)):
        ax.text(seps[j], Qs[i][j], Qs[i][j], size=10)
for sep in seps:
    ax.axvline(x = sep, color = 'gray', alpha = 0.2)
    ax.text(sep, 1000, str(sep), size=10)
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'Q-factor',  size='x-large')
ax.legend()
ax.invert_xaxis()
ax.set_xscale('log')
fig.savefig('output/Q_plot.png')


# resonance frequency plot
fig, ax = plt.subplots(figsize = (18,12), dpi = 80)
colors = ['red', 'blue', 'green', 'orange']
names = ['leaky 1', 'leaky 2', 'even', 'odd']
for i in range(len(detected_freqs)):
    ax.scatter(seps, detected_freqs[i], color = colors[i])
    ax.plot(seps, detected_freqs[i], color = colors[i], label = names[i])
    for j in range(len(seps)):
        ax.text(seps[j], detected_freqs[i][j], detected_freqs[i][j], size=10)
for sep in seps:
    ax.axvline(x = sep, color = 'gray', alpha = 0.2)
    ax.text(sep, 1.3, str(sep), size=10)
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'frequency (1/$\lambda$)',  size='x-large')
ax.legend()
ax.invert_xaxis()
ax.set_xscale('log')
fig.savefig('output/freq_plot.png')


# resonance frequency plot
fig, ax = plt.subplots(figsize = (18,12), dpi = 80)
colors = ['red', 'blue', 'green', 'orange']
names = ['leaky 1', 'leaky 2', 'even', 'odd']
for i in range(len(Im_freq)):
    ax.errorbar(seps, Im_freq[i], yerr = Im_freq_errors[i], color = colors[i], fmt = 'o')
    ax.scatter(seps, Im_freq[i], color = colors[i])
    ax.plot(seps, Im_freq[i], color = colors[i], label = names[i])
    for j in range(len(seps)):
        ax.text(seps[j], Im_freq[i][j], Im_freq[i][j], size=10)
for sep in seps:
    ax.axvline(x = sep, color = 'gray', alpha = 0.2)
    ax.text(sep, 0.002, str(sep), size=10)
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'frequency (1/$\lambda$)',  size='x-large')
ax.legend()
ax.invert_xaxis()
ax.set_xscale('log')
fig.savefig('output/Imfreq_plot.png')



# resonance wavelength plot
fig, ax = plt.subplots(figsize = (18,12), dpi = 80)
colors = ['red', 'blue', 'green', 'orange']
names = ['leaky 1', 'leaky 2', 'even', 'odd']
for i in range(len(res_lambda)):
    ax.errorbar(seps, res_lambda[i], yerr = Im_freq_errors[i], color = colors[i], fmt = 'o')
    ax.scatter(seps, res_lambda[i], color = colors[i])
    ax.plot(seps, res_lambda[i], color = colors[i], label = names[i])
    for j in range(len(seps)):
        ax.text(seps[j], res_lambda[i][j], res_lambda[i][j], size=10)
for sep in seps:
    ax.axvline(x = sep, color = 'gray', alpha = 0.2)
    ax.text(sep, 0.78, str(sep), size=10)
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'wavelength ($\mu$m)',  size='x-large')
ax.legend()
ax.invert_xaxis()
ax.set_xscale('log')
fig.savefig('output/wavelength.png')
