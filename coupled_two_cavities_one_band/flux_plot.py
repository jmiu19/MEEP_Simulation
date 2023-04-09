import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = sys.argv[1]
df = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df.columns = ['name', 'freq', 'transmission_right', 'transmission_left']

rslt_df = df.loc[(df['freq'] > 1.34) & (df['freq'] < 1.44)]


lam = 1/df['freq'].values
df['lam'] = lam

## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(rslt_df['freq'], rslt_df['transmission_right'], alpha=0.3, label="right detector", color="red")
plt.plot(rslt_df['freq'], rslt_df['transmission_left'], alpha=0.3, label="left detector", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"wavelength", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('output/fluxPlt'+name+'.png', bbox_inches='tight')
