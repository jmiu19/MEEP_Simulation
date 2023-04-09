import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt



## clean the dataframe
def name_rows(index_0, row_0, row_name_0):
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



df = pd.read_csv('output/cavity_resonances.dat', header=None, delimiter=', ', engine='python', skiprows=0)
parameters = pd.read_csv('parameters.csv', index_col=0)


row_name = ''
row_names = []
for index, row in df.iterrows():
    name_rows(index, row, row_name)
    df.loc[index, 'sep'] = parameters.loc[row_name]['Seps']

df.columns = ['freq', 'decay', 'Q', 'abs_amp', 'comp_amp', 'error', 'names', 'seps']

for col in df.columns:
    if col!='names':
        try:
            df[col] = df[col].astype(float)
        except:
            df = read_complex_in_col(df, col)
        

Q_max = max(df['Q'].values.tolist())


# freq factor plot
fig, ax = plt.subplots(figsize = (18,12), dpi = 80)
ax.errorbar(df['seps'], df['freq'], yerr=df['error_real'], fmt='o', capsize=3)
ax.set_xlabel(r'separation ($\mu$m)', size='x-large')
ax.set_ylabel(r'resonance freq.',  size='x-large')
ax.legend()
ax.invert_xaxis()
fig.savefig('output/resonancePlt/freq_plot.png')



