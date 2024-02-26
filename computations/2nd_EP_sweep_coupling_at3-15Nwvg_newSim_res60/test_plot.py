import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import os

df = pd.read_csv('cavity_resonances.csv')
df_OEmodes = df.loc[df['wvlength']<0.76].loc[df['wvlength']>0.72]

df_old = pd.read_csv('sim_data.csv')

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
# ax1.scatter(df_old['d'], df_old['freq_lossy'], color='cyan')
# ax2.scatter(df_old['d'], df_old['decay_lossy'], color='orange')
ax1.scatter(df_OEmodes['d'], df_OEmodes['freq'], color='b')
ax2.scatter(df_OEmodes['d'], df_OEmodes['decay'], color='r')

ax1.set_xlabel('d')
ax1.set_ylabel('E', color='g')
ax2.set_ylabel('decay', color='b')

plt.show()
