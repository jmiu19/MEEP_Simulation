import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


## read in data
df = pd.DataFrame()
df['holes'] = [1,2,3,4]
df['res_odd'] = [1.3748, 1.3743, 1.3722, 1.3719]
df['res_even'] = [1.3672, 1.3692, 1.3695, 1.3705]
df['Q_odd'] = [150, 220, 420, 795]
df['Q_even'] = [80, 200, 380, 680]



# freq factor plot
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
ax.plot(df['holes'], df['res_odd'], color='orange', marker='.')
ax.plot(df['holes'], df['res_even'], color='blue', marker='.')
ax.set_xlabel(r'number of waveguide holes', size='x-large')
ax.set_ylabel(r'resonance frequency (1/$\mu$m)',  size='x-large')
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