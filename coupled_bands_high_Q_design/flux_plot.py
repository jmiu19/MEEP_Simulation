import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = sys.argv[1]
df = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df.columns = ['name', 'freq', 'transmission_up', 'transmission_low']


lam = 1/df['freq'].values
df['lam'] = lam

## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(df['freq'], df['transmission_up'], alpha=0.3, label="upper cavity", color="red")
plt.plot(df['freq'], df['transmission_low'], alpha=0.3, label="lower cavity", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('output/fluxPlt'+name+'.png', bbox_inches='tight')
