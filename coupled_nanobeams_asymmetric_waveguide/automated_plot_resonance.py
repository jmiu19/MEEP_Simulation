import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
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
        # 6 output numbers from .dat
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

def find_odd_even_modes(df_used, sweep_param_val):
    # find the odd/even modes for a sweeping parameter val
    global sweep_param
    warn_modes = ('WARNING: detected high-Q mode '+
                  'that cannot be identified odd/even, '+
                  'need to be mannually identified '+
                  'or reset mode frequency threshold')
    modes_df = df_used[(df_used[sweep_param] == sweep_param_val)]
    for freq in modes_df['freq']:
        if any([freq>=1.45, freq<=1.35]):
            print(warn_modes)
            return 0, 0
    odd_mode_freq = max(modes_df['freq'].values.tolist())
    even_mode_freq = min(modes_df['freq'].values.tolist())
    return odd_mode_freq, even_mode_freq

def determine_mode_color(df_used, sweep_param_val, freq):
    # assign color to the resonance modes
    odd_mode, even_mode = find_odd_even_modes(df_used, 
                                              sweep_param_val)
    splitting_too_small = [abs(freq-even_mode)<=0.0005, 
                           abs(freq-odd_mode)<=0.0005]
    if (odd_mode)==0:
        return 'gray'
    if all(splitting_too_small):
        print('WARNING: '+
              'mode frequency splitting not resolvable')
        return 'gray'
    if (abs(freq-even_mode)<=0.0005):
        return 'orange'
    if (abs(freq-odd_mode)<=0.0005):
        return 'blue'
    else:
        return 'gray'

def compute_spliting(df_used, sweep_param_val):
    # compute the spliting of a given sweeping parameter val
    odd_freq, even_freq = find_odd_even_modes(df_used, 
                                              sweep_param_val)
    return abs(odd_freq-even_freq)
    
def estimate_single_cav_resonance(df_used, all_sweep_param_vals):
    # estimate the resonance frequency of a single cavity
    # based on the odd and even mode of a given 
    # sweeping parameter value
    estimated_freqs = []
    for val in all_sweep_param_vals:
        odd_freq, even_freq = find_odd_even_modes(df_used, val)
        estimated_freqs.append((odd_freq+even_freq)/2)
    return estimated_freqs
        

## reading the data
df = pd.read_csv('output/cavity_resonances.dat', 
                 header=None, delimiter=', ', engine='python')
parameters = pd.read_csv('parameters.csv', index_col=0)

## naming the rows
row_name = ''
row_names = []
sweep_param = input('sweeping parameter name'+ 
                    '(should be a name '+
                    'listed in the file parameters.csv): ')
unit = input('unit of the sweeping parameter: ')
for index, row in df.iterrows():
    name_rows(index, row, row_name)
    df.loc[index, sweep_param] = parameters.loc[row_name][sweep_param]


df.columns = ['freq', 
              'decay', 
              'Q', 
              'abs_amp', 
              'comp_amp', 
              'error', 
              'names', 
              str(sweep_param)]

## deal with the complex numbers
for col in df.columns:
    if col!='names':
        try:
            df[col] = df[col].astype(float)
        except:
            df = read_complex_in_col(df, col)

## keep only the odd and even modes
df_even_odd_modes = df[(df['Q'] > 1000)]

## keep only the leaky modes
df_leaky_modes = df[(df['Q'] < 1000) & (df['Q']>0)]
Q_max = max(df_leaky_modes['Q'].values.tolist())


## freq and Q-factor plot
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df_even_odd_modes[sweep_param].values.tolist())):
    ax.errorbar(df_even_odd_modes[sweep_param].values[i], 
                df_even_odd_modes['freq'].values[i], 
                yerr=df_even_odd_modes['error_real'].values[i], 
                fmt='.', capsize=3, 
                color=determine_mode_color(df_even_odd_modes,
                                           df_even_odd_modes[sweep_param].values[i],
                                           df_even_odd_modes['freq'].values[i]))
# delete duplicates in the list of sweeping param vals
all_sweep_param_vals = [*set(df_even_odd_modes[sweep_param].values.tolist())]
all_sweep_param_vals.sort()
ax.plot(all_sweep_param_vals,
        estimate_single_cav_resonance(df_even_odd_modes, all_sweep_param_vals),
        color='gray', linewidth=0.8, linestyle='--')
ax.set_xlabel(sweep_param+' ('+unit+')', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')

axQ = ax.twinx()  # initiate a second axes that shares the same x-axis
for i in range(len(df_even_odd_modes[sweep_param].values.tolist())):
    axQ.errorbar(df_even_odd_modes[sweep_param].values[i], 
                df_even_odd_modes['Q'].values[i], 
                marker='1', capsize=3, alpha=0.5,
                color=determine_mode_color(df_even_odd_modes,
                                           df_even_odd_modes[sweep_param].values[i],
                                           df_even_odd_modes['freq'].values[i]))
axQ.set_ylabel('Q-factor', size='x-large') 

orange_patch = mpatches.Patch(color='orange', label='even mode')
blue_patch = mpatches.Patch(color='blue', label='odd mode')
circ_mark = Line2D([0], [0], marker='o', color='gray', label='frequency', lw=0)
tri_mark = Line2D([0], [0], marker='1', color='gray', label='Q-factor', lw=0)
plt.legend(handles=[orange_patch, blue_patch, circ_mark, tri_mark])
fig.tight_layout() 
fig.savefig('output/resonancePlt/odd_even.png')

## leaky mode plot
normalize = mcolors.Normalize(vmin=np.abs((df_leaky_modes['Q'].values)).min(), 
                              vmax=np.abs((df_leaky_modes['Q'].values)).max())
colormap = cm.Greys
# setup the colorbar
scalarmappaple = cm.ScalarMappable(norm=normalize, cmap=colormap)
scalarmappaple.set_array(np.abs(df_leaky_modes['Q'].values))

fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
for i in range(len(df_leaky_modes[sweep_param].values.tolist())):
    ax.scatter(df_leaky_modes[sweep_param].values[i], 
               df_leaky_modes['freq'].values[i], 
               alpha=np.abs((df_leaky_modes['Q'].values[i])/(Q_max)),
               marker='.', color='black')
ax.set_xlabel(sweep_param+' ('+unit+')', size='x-large')
ax.set_ylabel(r'resonance frequency',  size='x-large')
ax.invert_xaxis()
plt.colorbar(scalarmappaple, label='Q-factor')
fig.tight_layout() 
fig.savefig('output/resonancePlt/leaky_modes.png')


## saving files
df.to_csv('output/sim_result_data.csv')
df_even_odd_modes.to_csv('output/odd_even_modes.csv')




