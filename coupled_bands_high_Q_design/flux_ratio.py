import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
resolution = 20
lambda_max = 1.8
lambda_min = 1.5
sep = 0.075

df = pd.read_csv('output/FLUX['+str(resolution)+','
                               +str(lambda_max)+','
                               +str(lambda_min)+','
                               +str(sep)+','
                               +'True].dat', 
                 header=None, 
                 sep=',', 
                 engine='python')
df0 = pd.read_csv('output/FLUX['+str(resolution)+','
                                +str(lambda_max)+','
                                +str(lambda_min)+','
                                +str(sep)+','
                                +'False].dat', 
                  header=None, 
                  sep=',', 
                  engine='python')
                  
df.columns = ['name', 'freq', 'transmission']
df0.columns = ['name', 'freq', 'transmission']

wavelengths = 1/df['freq'].values
flux = [df['transmission'][i]/df0['transmission'][i] for i in range(len(df['transmission']))]


## plot resonant wavelength over source wavelength (lower bound)
plt.figure(figsize=(5,3))
plt.plot(wavelengths, flux, alpha=0.3, label="transmission", color="red")
plt.legend()
plt.grid()
plt.xlabel(r"wavelength", fontsize=14)
plt.ylabel(r"transmission", fontsize=14)
plt.savefig('fluxPlt.png', bbox_inches='tight')
