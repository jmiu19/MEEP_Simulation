import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## read in data
df = pd.read_csv('nanobeam_cavity_varylength.dat', header=None, sep=',', engine='python')
df.columns = ['Nwvg', 'freq', 'decay', 'Q-factor']
df['lambda'] = np.round(1/df['freq'].values, 8)

## plot Q-factor over source wavelength (lower bound)
plt.figure(figsize=(6,4), dpi=150)
plt.scatter(df['Nwvg'], df['decay'], marker="o", color="darkorange")
plt.xlabel(r"number of waveguide holes", fontsize='x-large')
plt.ylabel("decay", fontsize='x-large')
plt.tight_layout()
plt.show()
