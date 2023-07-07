import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## read in data
df = pd.read_csv('nanobeam_cavity_varylength.dat', header=None, sep=',', engine='python')
df.columns = ['Nwvg', 'freq', 'decay', 'Q-factor']
df['lambda'] = np.round(1/df['freq'].values, 8)
df.to_csv('output/nanobeam_cavity_varylength.csv')

## plot Q-factor over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.scatter(df['Nwvg'], df['decay'], s=55, marker="o", color="darkorange")
plt.xlabel(r"number of waveguide holes", fontsize='x-large')
plt.ylabel("decay", fontsize='x-large')
plt.savefig('output/Nwvg_decay.png', bbox_inches='tight')
