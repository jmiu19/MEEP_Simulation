import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.cm as cm


## clean the dataframe
def name_rows(index_0, row_0, row_name_0):
    # read results from .dat 
    # and name each row based on parameters used
    if str(row_0[0])[0]=='[':
        global row_name, row_names, df
        row_name = str(row_0[0])
        for col_ind in range(6):
            df.at[index_0, col_ind] = df.loc[index_0][df.columns[col_ind+1]]
        df.at[index_0, 6] = row_name
        row_names.append(row_name)
    else:
        df.at[index_0, 6] = row_name_0

def read_complex(num):
    # read a complex number
    # break down the complex number to a real part and an imaginary part
    num = str(num)
    for i in range(1, len(num)):
        if (num[i]=='+' or num[i]=='-') and (num[i-1]!='e'):
            real_i = i
        if (num[i]=='i'):
            imag_i = i
    real_num = float(num[:real_i])    
    imag_num = float(num[real_i:imag_i])
    return real_num, imag_num

def read_complex_in_col(df, col_name):
    # read a column in df which contains complex number
    # return df with two new columns containing the real/imagionary
    # part of the complex numbers in the original column
    col_vals_real = []
    col_vals_imag = []
    for index, row in df.iterrows():
        num = df.at[index, col_name]
        real, imag = read_complex(num)
        col_vals_real.append(real)
        col_vals_imag.append(imag)
    real_col_name = col_name+'_real'
    imag_col_name = col_name+'_imag'
    df[real_col_name] = col_vals_real
    df[imag_col_name] = col_vals_imag
    return df

def determine_mode_color(freq):
    # assign color to the resonance modes
    if (freq>1.32 and freq<1.37):
        return 'orange'
    if (freq<1.395 and freq>1.37):
        return 'blue'
    else:
        return 'gray'



## reading the data
df = pd.read_csv('output/cavity_resonances.dat', 
                 header=None, delimiter=', ', engine='python')
parameters = pd.read_csv('parameters.csv', index_col=0)

## naming the rows
row_name = ''
row_names = []
for index, row in df.iterrows():
    name_rows(index, row, row_name)
    df.loc[index, 'sep'] = parameters.loc[row_name]['Seps']


df.columns = ['freq', 
              'decay', 
              'Q', 
              'abs_amp', 
              'comp_amp', 
              'error', 
              'names', 
              'seps']

## deal with the complex numbers
for col in df.columns:
    if col!='names':
        try:
            df[col] = df[col].astype(float)
        except:
            df = read_complex_in_col(df, col)

## keep only the odd and even modes
df_even_odd_modes = df[((df['freq'] < 1.395) & 
                        (df['freq'] > 1.32)  &
                        (df['Q'] > 1000))]

## keep only the leaky modes
df_leaky_modes = df[(df['Q'] < 1000) & (df['Q']>0)]
Q_max = max(df_leaky_modes['Q'].values.tolist())


# freq and Q-factor plot
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df_even_odd_modes['seps'].values.tolist())):
    ax.errorbar(df_even_odd_modes['seps'].values[i], 
                df_even_odd_modes['freq'].values[i], 
                yerr=df_even_odd_modes['error_real'].values[i], 
                fmt='.', capsize=3, 
                color=determine_mode_color(df_even_odd_modes['freq'].values[i]))
ax.plot(df_even_odd_modes['seps'], [1.3712]*len(df_even_odd_modes['seps']),
        color='gray', linewidth=0.8, linestyle='--')
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
ax.axvspan(0.2, 0.35, color='gray', alpha=0.3, lw=0)
orange_patch = mpatches.Patch(color='orange', label='even mode')
blue_patch = mpatches.Patch(color='blue', label='odd mode')
ax.legend(handles=[orange_patch, blue_patch], loc='lower left')
ax.invert_xaxis()

axQ = ax.twinx()  # instantiate a second axes that shares the same x-axis
for i in range(len(df_even_odd_modes['seps'].values.tolist())):
    axQ.errorbar(df_even_odd_modes['seps'].values[i], 
                df_even_odd_modes['Q'].values[i], 
                marker='1', capsize=3, alpha=0.5,
                color=determine_mode_color(df_even_odd_modes['freq'].values[i]))
axQ.set_ylabel('Q-factor', size='x-large') 

fig.tight_layout() 
fig.savefig('output/resonancePlt/odd_even.png')






normalize = mcolors.Normalize(vmin=np.abs((df_leaky_modes['Q'].values)).min(), 
                              vmax=np.abs((df_leaky_modes['Q'].values)).max())
colormap = cm.Greys

# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(np.abs(df_leaky_modes['Q'].values))

fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df_leaky_modes['seps'].values.tolist())):
    ax.scatter(df_leaky_modes['seps'].values[i], 
               df_leaky_modes['freq'].values[i], 
               alpha=np.abs((df_leaky_modes['Q'].values[i])/(Q_max)),
               marker='.', color='black')
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
ax.invert_xaxis()
plt.colorbar(scalarmappaple, label='Q-factor')
fig.tight_layout() 
fig.savefig('output/resonancePlt/leaky_modes.png')
df.to_csv('output/sim_result_data.csv')




