import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
name = sys.argv[1]
df_flux = pd.read_csv('output/FLUX'+name+'.dat', header=None, sep=',', engine='python')
df_res = pd.read_csv('output/sim_result_data.csv')
df_flux.columns = ['name', 'freq', 
                   'transmission_upper', 
                   'transmission_lower', 
                   'transmission_between', 
                   'transmission_below', 
                   'transmission_above']


df_flux['lam'] = 1/df_flux['freq'].values
# df_flux = df_flux[(1/df_flux['freq']>0.7)]
# df_flux = df_flux[(1/df_flux['freq']<0.78)]
df_res_of_interest = df_res[(df_res['names'] == name)]

## plot resonant wavelength over source freq
plt.figure(figsize=(5,3))
plt.plot(df_flux['freq'], df_flux['transmission_upper'], alpha=0.3, label="upper cavity", color="red")
plt.plot(df_flux['freq'], df_flux['transmission_lower'], alpha=0.3, label="lower cavity", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt_cav/fluxPlt'+name+'.png', bbox_inches='tight')


## plot resonant wavelength over source freq
plt.figure(figsize=(5,3))
plt.plot(df_flux['freq'], df_flux['transmission_between'], alpha=0.3, label="between cavities", color="red")
plt.plot(df_flux['freq'], df_flux['transmission_below'], alpha=0.3, label="lower region", color="blue")
plt.plot(df_flux['freq'], df_flux['transmission_above'], alpha=0.3, label="upper region", color="orange")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt_reg/fluxPlt'+name+'.png', bbox_inches='tight')






## plot resonant wavelength over source lam
plt.figure(figsize=(5,3))
for freq in df_res_of_interest['freq'].values.tolist():
    if (0.6<=1/freq) and (1/freq<=0.85):
        plt.axvline(x=1/freq, color='gray', alpha=0.2)
        plt.annotate(round(1/freq,3), size=5, alpha=0.2,
                     xy=(1/freq, max(df_flux['transmission_upper'].values.tolist())/2))
plt.plot(df_flux['lam'], df_flux['transmission_upper'], alpha=0.5, label="upper cavity", color="red")
plt.plot(df_flux['lam'], df_flux['transmission_lower'], alpha=0.5, label="lower cavity", color="blue")
df_res_of_interest = df_res[(df_res['names'] == name)]
plt.legend()
plt.xlabel(r"wavelength (um)", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt_cav/wvlength/fluxPlt'+name+'.png', bbox_inches='tight')


## plot resonant wavelength over source lam
plt.figure(figsize=(5,3))
for freq in df_res_of_interest['freq'].values.tolist():
    if (0.6<=1/freq) and (1/freq<=0.85):
        plt.axvline(x = 1/freq, color='gray', alpha=0.2)
        plt.annotate(round(1/freq,3), size=5, alpha=0.2,
                     xy=(1/freq, max(df_flux['transmission_upper'].values.tolist())/2))
plt.plot(df_flux['lam'], df_flux['transmission_between'], alpha=0.5, label="between cavities", color="red")
plt.plot(df_flux['lam'], df_flux['transmission_below'], alpha=0.5, label="lower region", color="blue")
plt.plot(df_flux['lam'], df_flux['transmission_above'], alpha=0.5, label="upper region", color="orange")
plt.legend()
plt.xlabel(r"wavelength (um)", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt_reg/wvlength/fluxPlt'+name+'.png', bbox_inches='tight')