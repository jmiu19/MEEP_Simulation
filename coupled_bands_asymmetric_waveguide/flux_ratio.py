import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = '[80,0.337,0.6,0.85,True,300,10,10]'
name0 = '[80,0.337,0.6,0.85,False,300,10,10]'
df = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df0 = pd.read_csv('output/FLUX'+name0+'.dat', header=None, sep=',', engine='python')

df.columns = ['name', 'freq', 'transmission_upper', 'transmission_lower']
df0.columns = ['name', 'freq', 'transmission_upper', 'transmission_lower']


wavelengths = 1/df['freq'].values
flux_up = [df['transmission_upper'][i]/(df0['transmission_upper'][i]*7) for i in range(len(df['transmission_upper']))]
flux_low = [df['transmission_lower'][i]/(df0['transmission_upper'][i]*7) for i in range(len(df['transmission_lower']))]


## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(df['freq'], flux_up, alpha=0.3, label="upper cavity", color="red")
plt.plot(df['freq'], flux_low, alpha=0.3, label="lower cavity", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize='x-large')
plt.ylabel(r"transmission", fontsize='x-large')
plt.savefig('output/fluxPlt/fluxPltRatio.png', bbox_inches='tight')
