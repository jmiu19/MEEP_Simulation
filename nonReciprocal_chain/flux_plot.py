import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = sys.argv[1]
df = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df.columns = ['name', 'freq', 
              'transmission_upper', 
              'transmission_lower', 
              'transmission_between', 
              'transmission_below', 
              'transmission_above']


lam = 1/df['freq'].values
df['lam'] = lam

## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(df['freq'], df['transmission_upper'], alpha=0.3, label="upper cavity", color="red")
plt.plot(df['freq'], df['transmission_lower'], alpha=0.3, label="lower cavity", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('output/fluxPlt/cavity_raw_freq/fluxPlt'+name+'.png', bbox_inches='tight')


## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(df['freq'], df['transmission_between'], alpha=0.3, label="between cavities", color="red")
plt.plot(df['freq'], df['transmission_below'], alpha=0.3, label="lower region", color="blue")
plt.plot(df['freq'], df['transmission_above'], alpha=0.3, label="upper region", color="orange")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('output/fluxPlt/region_raw_freq/fluxPlt'+name+'.png', bbox_inches='tight')
