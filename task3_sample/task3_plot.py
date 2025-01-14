import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## read in data
df = pd.read_csv('nanobeam_cavity_varylength.dat', header=None, sep=',', engine='python')
df.columns = ['cavityLength', 'nu', 'Q-factor']
cavityLengths = df['cavityLength'].values.tolist()
df['lambda'] = 1/df['nu'].values
df = df.sort_values('cavityLength', axis=0)
df.to_csv('output/nanobeam_cavity_varylength.csv')

## plot Q-factor over cavityLength
plt.figure(figsize=(5,3))
plt.scatter(df['cavityLength'], df['Q-factor'], s=55, label="Q-factor", marker="+", color="darkorange")
plt.plot(df['cavityLength'], df['Q-factor'], alpha=0.3, color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"cavity length ($\mu$m)", fontsize=14)
plt.ylabel("Q-factor", fontsize=14)
plt.savefig('output/Q_sCav.png', bbox_inches='tight')

## plot resonant wavelength over cavityLength
plt.figure(figsize=(5,3))
plt.scatter(df['cavityLength'], df['lambda'], s=55, label="lambda", marker="+", color="darkorange")
plt.plot(df['cavityLength'], df['lambda'], alpha=0.3, color="red")
plt.legend()
plt.grid()
plt.xlabel(r"cavity length ($\mu$m)", fontsize=14)
plt.ylabel(r"resonant $\lambda$ ($\mu$m)", fontsize=14)
plt.savefig('output/lambda_sCav.png', bbox_inches='tight')



## plot the configuration
import h5py

eps_h5file = h5py.File('nanobeam-eps-000621.19.h5','r')
eps_data = np.array(eps_h5file['eps'])
ey_h5file = h5py.File('nanobeam-ey-000621.19.h5','r')
ey_data = np.array(ey_h5file['ey'])
plt.figure(dpi=100)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ey_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.savefig('output/config.png', bbox_inches='tight')
