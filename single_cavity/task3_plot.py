import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## read in data
df = pd.read_csv('nanobeam_cavity_varylength.dat', header=None, sep=',', engine='python')
df.columns = ['lam_up', 'lam_low', 'w', 'nu', 'Q-factor']
lam_ups = df['lam_up'].values.tolist()
df['lambda'] = np.round(1/df['nu'].values, 8)
df = np.round(df.sort_values('lam_up', axis=0),8)
df.to_csv('output/nanobeam_cavity_varylength.csv')

## plot Q-factor over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.scatter(df['w'], df['Q-factor'], s=55, label="Q-factor", marker="+", color="darkorange")
plt.plot(df['w'], df['Q-factor'], alpha=0.3, color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"width (in unit of lattice constant)", fontsize=14)
plt.ylabel("Q-factor", fontsize=14)
plt.savefig('output/Q_sCav.png', bbox_inches='tight')

## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.scatter(df['w'], df['lambda'], s=55, label="lambda", marker="+", color="darkorange")
plt.plot(df['w'], df['lambda'], alpha=0.3, color="red")
plt.legend()
plt.grid()
plt.xlabel(r"width (in unit of lattice constant)", fontsize=14)
plt.ylabel(r"resonant $\lambda$ ($\mu$m)", fontsize=14)
plt.savefig('output/lambda_sCav.png', bbox_inches='tight')



## plot the configuration
import h5py

eps_h5file = h5py.File('nanobeam-eps-000613.88.h5','r')
eps_data = np.array(eps_h5file['eps'])
ey_h5file = h5py.File('nanobeam-ey-000613.88.h5','r')
ey_data = np.array(ey_h5file['ey'])
plt.figure(dpi=100)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ey_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.savefig('output/config.png', bbox_inches='tight')
