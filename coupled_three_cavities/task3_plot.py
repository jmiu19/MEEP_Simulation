import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## plot the configuration
import h5py

eps_h5file = h5py.File('nanobeam-eps-000038449.h5','r')
eps_data = np.array(eps_h5file['eps'])
ey_h5file = h5py.File('nanobeam-ey-000038449.h5','r')
ey_data = np.array(ey_h5file['ey'])
plt.figure(dpi=500)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ey_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
plt.axis('off')
plt.savefig('output/config.png', bbox_inches='tight')
