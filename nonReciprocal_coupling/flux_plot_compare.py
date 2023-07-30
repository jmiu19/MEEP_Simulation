import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

## read in data
names_df = pd.read_csv('parameters.csv')
names = names_df['Name'].values.tolist()
print('==================================================')
print('==================================================')
print('Tagnames inputs: ')
print(names_df.columns.values.tolist()[1:])
label_name = input('sweeping parameter (one of the tag inputs listed):')
print(' ')
print('Tag of the simulations:')
n=0
for name_tag in names:
   print(str(n)+'. '+str(name_tag))
   n=n+1
print(' ')
keep_reading = 'Y'
names_interest = []
names_normalization = []
labels_interest = []
m=1
while keep_reading=='Y':
    try:
        name_ind = input('tag of the simulation_'+str(m)+' of interest (integer input): ')
        name0_ind = input('tag of the simulation_'+str(m)+' for normalization (integer input): ') 
        names_interest.append(names[int(name_ind)])
        names_normalization.append(names[int(name0_ind)])
        labels_interest.append(names_df[label_name].values.tolist()[int(name_ind)])
        keep_reading = input('add another simulation of interset (Y/N)? ')
        m=m+1
    except:
        keep_reading = 'N'
        print('input error, try again')
        exit()
    
plot_res = input('plot resonance of the modes (Y/N): ')

upper_cav_flux = []
lower_cav_flux = []
above_reg_flux = []
below_reg_flux = []
between_flux = []
fluxes = []
lams = []
res_freqs = []
for m in range(len(names_interest)):
    name = names_interest[m]
    name0 = names_normalization[m]
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

    ## truncate flux spectrum
    # df_flux = df_flux[(1/df_flux['freq']>0.7)]
    # df_flux = df_flux[(1/df_flux['freq']<0.78)]
    
    trans_names = ['transmission_upper',
                   'transmission_lower',
                   'transmission_between',
                   'transmission_below',
                   'transmission_above']
    df_flux_normalized = df_flux
    for trans_name in trans_names:
        df_flux_normalized[trans_name] = df_flux[trans_name] - df_flux0[trans_name]
    
    if plot_res == 'Y':
        df_res = pd.read_csv('output/sim_result_data.csv')
        df_res_of_interest = df_res[(df_res['names'] == name)]
        res_freqs.append(df_res_of_interest['freq'].values.tolist())
    
    upper_cav_flux.append(df_flux_normalized['transmission_upper'])
    lower_cav_flux.append(df_flux_normalized['transmission_lower'])
    above_reg_flux.append(df_flux_normalized['transmission_above'])
    below_reg_flux.append(df_flux_normalized['transmission_below'])
    between_flux.append(df_flux_normalized['transmission_between'])
    fluxes.append(df_flux_normalized['freq'])
    lams.append(df_flux_normalized['lam'])
    

## plot flux over source freq
pltNames = ['upperCav', 'lowerCav']
cav_fluxs = [upper_cav_flux, lower_cav_flux]
for i in range(len(cav_fluxs)):
    plt.figure(figsize=(5,3))
    for m in range(len(names_interest)):
        plt.plot(fluxes[m], cav_fluxs[i][m],
                 alpha=0.3, label=labels_interest[m])
    plt.legend()
    plt.grid()
    plt.xlabel(r"frequency", fontsize=14)
    plt.ylabel(r"flux", fontsize=14)
    plt.savefig('output/fluxPlt/cavity_compare/freq/'+pltNames[i]+'.png', 
                bbox_inches='tight')


## plot flux over source freq
pltNames = ['aboveeReg', 'belowReg', 'betweenReg']
reg_fluxs = [above_reg_flux, below_reg_flux, between_flux]
for i in range(len(reg_fluxs)):
    plt.figure(figsize=(5,3))
    for m in range(len(names_interest)):
        plt.plot(fluxes[m], reg_fluxs[i][m],
                 alpha=0.3, label=labels_interest[m])
    plt.legend()
    plt.grid()
    plt.xlabel(r"frequency", fontsize=14)
    plt.ylabel(r"flux", fontsize=14)
    plt.savefig('output/fluxPlt/region_compare/freq/'+pltNames[i]+'.png', 
                bbox_inches='tight')





## plot flux over source lam
pltNames = ['upperCav', 'lowerCav']
cav_fluxs = [upper_cav_flux, lower_cav_flux]
for i in range(len(cav_fluxs)):
    plt.figure(figsize=(5,3), dpi=300)
    for m in range(len(names_interest)):
        if plot_res == 'Y':
            for freq in res_freqs[m]:
                if (0.6<=1/freq) and (1/freq<=0.85):
                    plt.axvline(x=1/freq, color='gray', alpha=0.1)
                    plt.annotate(round(1/freq,3), size=3, alpha=0.1,
                                 xy=(1/freq,
                        max(cav_fluxs[i][m].values.tolist())*(0.95-0.1*m)))
        plt.plot(lams[m], cav_fluxs[i][m],
                 alpha=0.3, label=labels_interest[m])
    plt.legend()
    plt.xlabel(r"wavelength (um)", fontsize=14)
    plt.ylabel(r"flux", fontsize=14)
    plt.savefig('output/fluxPlt/cavity_compare/wvlength/'+pltNames[i]+'.png', 
                bbox_inches='tight')




## plot flux over source lam
pltNames = ['aboveeReg', 'belowReg', 'betweenReg']
reg_fluxs = [above_reg_flux, below_reg_flux, between_flux]
for i in range(len(reg_fluxs)):
    plt.figure(figsize=(5,3), dpi=300)
    for m in range(len(names_interest)):
        if plot_res == 'Y':
            for freq in res_freqs[m]:
                if (0.6<=1/freq) and (1/freq<=0.85):
                    plt.axvline(x=1/freq, color='gray', alpha=0.1)
                    plt.annotate(round(1/freq,3), size=3, alpha=0.1,
                                 xy=(1/freq,
                        max(reg_fluxs[i][m].values.tolist())*(0.95-0.15*m)))
        plt.plot(lams[m], reg_fluxs[i][m],
                 alpha=0.3, label=labels_interest[m])
    plt.legend()
    plt.xlabel(r"wavelength (um)", fontsize=14)
    plt.ylabel(r"flux", fontsize=14)
    plt.savefig('output/fluxPlt/region_compare/wvlength/'+pltNames[i]+'.png', 
                bbox_inches='tight')















