import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.cm as cm


## read in data
df0 = pd.read_csv('nanobeam_cavity_varylength.csv')
df0 = df0[df0['Q']>2000]
Q_max = max(df0['Q'].values.tolist())
Q_min = min(df0['Q'].values.tolist())
normalize = mcolors.Normalize(vmin=np.abs((df0['Q'].values)).min()-1000, 
                              vmax=np.abs((df0['Q'].values)).max())
colormap = cm.Greys

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(np.abs(df0['Q'].values))

fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df0['w'].values.tolist())):
    ax.scatter(df0['w'].values[i]*0.33, 
               df0['freq'].values[i], 
               alpha=np.abs((df0['Q'].values[i]-Q_min+1000)/(Q_max-Q_min+1000)),
               marker='.', color='black')
ax.set_xlabel(r'width of nanobeam ($\mu$m)', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
ax.plot([df0['w'].values[0]*0.33, df0['w'].values[-1]*0.33], [1.3712]*2,
        color='gray', linewidth=0.8, linestyle='--')
plt.colorbar(scalarmappaple, label='Q-factor')
fig.tight_layout() 
fig.savefig('output/all_modes.png')


