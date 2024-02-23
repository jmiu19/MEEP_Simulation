import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = sys.argv[1]
df = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df.columns = ['detector', 'freq', 'flux']
lam = 1/df['freq'].values
df['lam'] = lam


detectors = list(set(df['detector'].values.tolist()))
dfs_by_detectors = []
for i in range(len(detectors)):
    dfs_by_detectors.append(df.loc[df['detector'] == detectors[i]])
    

## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(10,6))
for i in range(len(detectors)):
    plt.plot(dfs_by_detectors[i]['freq'], dfs_by_detectors[i]['flux'],
             alpha=0.3, label="detector"+str(i))
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('output/fluxPlt/'+name+'.png', bbox_inches='tight')
