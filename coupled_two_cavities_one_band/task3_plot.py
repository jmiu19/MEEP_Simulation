import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.cm as cm


## read in data
df = pd.DataFrame()
df['holes'] = [1,2,3,4]
df['res_odd'] = [1.3748, 1.3743, 1.3722, 1.3719]
df['res_even'] = [1.3672, 1.3692, 1.3695, 1.3705]
df['Q_odd'] = [150, 220, 420, 795]
df['Q_even'] = [80, 200, 380, 680]

df0 = pd.read_csv('cavity_resonances.csv')

# freq factor plot
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
ax.plot(df['holes'], df['res_odd'], color='orange', marker='.')
ax.plot(df['holes'], df['res_even'], color='blue', marker='.')
ax.set_xlabel(r'number of waveguide holes', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
orange_patch = mpatches.Patch(color='orange', label='even mode')
blue_patch = mpatches.Patch(color='blue', label='odd mode')
ax.legend(handles=[orange_patch, blue_patch], loc='lower left')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.invert_xaxis()

axQ = ax.twinx()  # instantiate a second axes that shares the same x-axis
axQ.plot(df['holes'], df['Q_odd'], color='orange', marker='1', linestyle='dashdot')
axQ.plot(df['holes'], df['Q_even'], color='blue', marker='1', linestyle='dashdot')
axQ.set_ylabel('Q-factor', size='x-large') 

fig.tight_layout() 
fig.savefig('output/odd_even.png')




df0 = df0[df0['freq']>1.36]
Q_max = max(df0['Q'].values.tolist())
normalize = mcolors.Normalize(vmin=np.abs((df0['Q'].values)).min(), 
                              vmax=np.abs((df0['Q'].values)).max())
colormap = cm.Greys

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(np.abs(df0['Q'].values))

fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df0['holes'].values.tolist())):
    ax.scatter(df0['holes'].values[i], 
               df0['freq'].values[i], 
               alpha=np.abs((df0['Q'].values[i])/(Q_max)),
               marker='.', color='black')
ax.set_xlabel(r'number of waveguide holes in each cavity', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
ax.plot([1,4], [1.3712]*len([1,4]),
        color='gray', linewidth=0.8, linestyle='--')
ax.set_xticks([1, 2, 3, 4])
ax.invert_xaxis()
plt.colorbar(scalarmappaple, label='Q-factor')
fig.tight_layout() 
fig.savefig('output/all_modes.png')


