import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
df = pd.read_csv('flux.dat', header=None, sep=',', engine='python')
df0 = pd.read_csv('flux0.dat', header=None, sep=',', engine='python')
df.columns = ['name', 'freq', 'transmission']
df0.columns = ['name', 'freq', 'transmission']

flux = [df['transmission'][i] for i in range(len(df['transmission']))]




## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(df['freq'], flux, alpha=0.3, label="transmission", color="red")
plt.legend()
plt.grid()
plt.xlabel(r"wavelength", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('fluxPlt.png', bbox_inches='tight')
