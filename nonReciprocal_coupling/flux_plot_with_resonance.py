import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt


## read in data
names_df = pd.read_csv('parameters.csv')
names = names_df['Name'].values.tolist()
print('==================================================')
print('Tag number of the simulations:')
n=0
for name_tag in names:
   print(str(n)+'. '+str(name_tag))
   n=n+1
print(' ')
name_ind = input('tag of the simulation of interest (integer input): ')
name0_ind = input('tag fo the simulation for normalization (integer input): ')
name = names[int(name_ind)]
name0 = names[int(name0_ind)]
plot_res = input('plot resonance of the modes (True or False): ')

df_flux = pd.read_csv('output/FLUX'+name+'.dat',
                      header=None, sep=',', engine='python')
df_flux0 = pd.read_csv('output/FLUX'+name0+'.dat',
                      header=None, sep=',', engine='python')
df_flux.columns = ['name', 'freq',
                   'transmission_upper',
                   'transmission_lower',
                   'transmission_between',
                   'transmission_below',
                   'transmission_above']
df_flux0.columns = ['name', 'freq',
                    'transmission_upper',
                    'transmission_lower',
                    'transmission_between',
                    'transmission_below',
                    'transmission_above']



df_flux['lam'] = 1/df_flux['freq'].values

# truncate flux spectrum
df_flux = df_flux[(1/df_flux['freq']>0.7)]
df_flux = df_flux[(1/df_flux['freq']<0.78)]

trans_names = ['transmission_upper',
               'transmission_lower',
               'transmission_between',
               'transmission_below',
               'transmission_above']
df_flux_nomalized = df_flux
for trans_name in trans_names:
    df_flux_nomalized[trans_name] = df_flux[trans_name] - df_flux0[trans_name]

if plot_res == 'True':
    df_res = pd.read_csv('output/sim_result_data.csv')
    df_res_of_interest = df_res[(df_res['names'] == name)]



## plot resonant wavelength over source freq
plt.figure(figsize=(5,3))
plt.plot(df_flux_nomalized['freq'], df_flux_nomalized['transmission_upper'],
         alpha=0.3, label="upper cavity", color="red")
plt.plot(df_flux_nomalized['freq'], df_flux_nomalized['transmission_lower'],
         alpha=0.3, label="lower cavity", color="blue")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt/cavity_individual/freq/fluxPlt'
            +name+'.png', bbox_inches='tight')


## plot resonant wavelength over source freq
plt.figure(figsize=(5,3))
plt.plot(df_flux_nomalized['freq'], df_flux_nomalized['transmission_between'],
         alpha=0.3, label="between cavities", color="red")
plt.plot(df_flux_nomalized['freq'], df_flux_nomalized['transmission_below'],
         alpha=0.3, label="lower region", color="blue")
plt.plot(df_flux_nomalized['freq'], df_flux_nomalized['transmission_above'],
         alpha=0.3, label="upper region", color="orange")
plt.legend()
plt.grid()
plt.xlabel(r"frequency", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt/region_individual/freq/fluxPlt'
            +name+'.png', bbox_inches='tight')






## plot resonant wavelength over source lam
plt.figure(figsize=(5,3), dpi=300)
if plot_res == 'True':
    for freq in df_res_of_interest['freq'].values.tolist():
        if (0.6<=1/freq) and (1/freq<=0.85):
            plt.axvline(x=1/freq, color='gray', alpha=0.2)
            plt.annotate(round(1/freq,3), size=5, alpha=0.2,
                         xy=(1/freq,
                max(df_flux_nomalized['transmission_upper'].values.tolist())/2))
plt.plot(df_flux_nomalized['lam'], df_flux_nomalized['transmission_upper'],
         alpha=0.5, label="upper cavity", color="red")
plt.plot(df_flux_nomalized['lam'], df_flux_nomalized['transmission_lower'],
         alpha=0.5, label="lower cavity", color="blue")
plt.legend()
plt.xlabel(r"wavelength (um)", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt/cavity_individual/wvlength/fluxPlt'+
            name+'.png', bbox_inches='tight')


## plot resonant wavelength over source lam
plt.figure(figsize=(5,3), dpi=300)
if plot_res == 'True':
    for freq in df_res_of_interest['freq'].values.tolist():
        if (0.6<=1/freq) and (1/freq<=0.85):
            plt.axvline(x = 1/freq, color='gray', alpha=0.2)
            plt.annotate(round(1/freq,3), size=5, alpha=0.2,
                         xy=(1/freq,
                max(df_flux_nomalized['transmission_upper'].values.tolist())/2))
plt.plot(df_flux_nomalized['lam'], df_flux_nomalized['transmission_between'],
         alpha=0.5, label="between cavities", color="red")
plt.plot(df_flux_nomalized['lam'], df_flux_nomalized['transmission_below'],
         alpha=0.5, label="lower region", color="blue")
plt.plot(df_flux_nomalized['lam'], df_flux_nomalized['transmission_above'],
         alpha=0.5, label="upper region", color="orange")
plt.legend()
plt.xlabel(r"wavelength (um)", fontsize=14)
plt.ylabel(r"flux", fontsize=14)
plt.savefig('output/fluxPlt/region_individual/wvlength/fluxPlt'+
            name+'.png', bbox_inches='tight')
