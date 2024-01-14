import pandas as pd
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from matplotlib.ticker import FormatStrFormatter
from scipy.optimize import curve_fit


##############################################################
###########         Simulation reading          ##########3#3#
##############################################################
def find_odd_even_modes(df_used, sweep_param_val):
    # find the odd/even modes for a sweeping parameter val
    global sweep_param
    warn_modes = ('WARNING: detected high-Q mode '+
                  'that cannot be identified odd/even, '+
                  'need to be mannually identified '+
                  'or reset mode frequency threshold')
    modes_df = df_used[(df_used[sweep_param] == sweep_param_val)]
    for freq in modes_df['freq']:
        if any([freq>=1.42, freq<=1.30]):
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
df = pd.read_csv('sim_result_data.csv', engine='python')
## keep only the odd and even modes
df_even_odd_modes = df[(df['Q'] > 1000)]
sweep_param = 'seps'

##############################################################
###########         Theoretical Fitting         ##########3#3#
##############################################################
def expFit(x, alpha, kappa):
    return alpha * np.exp(-kappa*x)

df_fit = pd.read_csv('fitting_coupling.csv')
dplusW = df_fit['d+w']
C = df_fit['C']
presetW = 0.462
expParam, expCov = curve_fit(expFit, dplusW, C, p0=[0.005,0.005], maxfev=10000)
alpha, kappa = expParam[0], expParam[1]

minC = min(df_fit['C'].values.tolist())
maxC = max(df_fit['C'].values.tolist())
C_range = np.linspace(0.7*minC, 2.5*maxC, 300)
d_range = [-np.log(targetC/alpha)/kappa-presetW for targetC in C_range]


####### compute required coupling for a given loss difference ###############
amax = 401 # number of iteration when computing eigenvalues
intrinsicGain1 = -0.00009j
intrinsicGain2 = -0.00009j
Ecm = 1.371
detuning = 0.00
EX = 1.371 + detuning
ini_C = 0.001141
ini_CIFS = 0
CPhase = 0j
delEcmGamma = 0#-0.003166247j

m11 = Ecm + intrinsicGain1 + delEcmGamma
m22 = EX + intrinsicGain2

# generate 2D phase diagram displaying EP splitting around target loss diff.
df_Eigen = pd.DataFrame(columns=['eigVal',
                                 'eigVec',
                                 'Coupling coeff.',
                                 'Ecm',
                                 'XC',
                                 'detuning'])
for C in C_range:
    c12 = C + C*0.005j
    c21 = C + C*0.005j
    c11 = -C*0.35-C*0.007j
    c22 = -C*0.35-C*0.007j
    C_real = C
    E = np.array([[ m11,   0 ],
                  [ 0,   m22 ]])
    C = np.array([[ c11, c12 ],
                  [ c21, c22 ]])
    M = E+C
    MeigVal, MeigVec = np.linalg.eig(M)
    # append eigenvals and eigenvectors to dataframe
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         C_real,
                                         m11, m22,
                                         Ecm-EX]

## loss difference applied eigenvals
realEigVal = np.real(df_Eigen['eigVal'].values.tolist())
compEigVal = np.imag(df_Eigen['eigVal'].values.tolist())
realEigVal1 = []
realEigVal2 = []
compEigVal1 = []
compEigVal2 = []


# sort the eigenvalues
for i in range(len(realEigVal)):
    realVals = realEigVal[i]
    compVals = compEigVal[i]
    for j in range(len(realVals)):
        for k in range(len(realVals)-j-1):
            if (compVals[k]-compVals[k+1])>0.000001:
                val = realVals[k]
                realVals[k] = realVals[k+1]
                realVals[k+1] = val
                val = compVals[k]
                compVals[k] = compVals[k+1]
                compVals[k+1] = val
            elif abs(compVals[k]-compVals[k+1])<=0.000001:
                if (realVals[k]-realVals[k+1])>0.000001:
                    val = realVals[k]
                    realVals[k] = realVals[k+1]
                    realVals[k+1] = val
                    val = compVals[k]
                    compVals[k] = compVals[k+1]
                    compVals[k+1] = val
    realEigVal1.append(realVals[0])
    realEigVal2.append(realVals[1])
    compEigVal1.append(compVals[0])
    compEigVal2.append(compVals[1])


realCompEigVals = [[realEigVal1, realEigVal2],
                   [compEigVal1, compEigVal2]]





## plot the eigenvalues
Cs_eigen = df_Eigen['Coupling coeff.'].values.tolist()
names = ['Eigenval 1', 'Eigenval 2', 'Imag(', 'Re(']
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
for i in range(len(realCompEigVals[0])):
    ax[0].plot(d_range, np.array(realCompEigVals[0][i]),
               alpha=0.8) #, label=names[i])
    ax[0].set_ylabel(r'Re($\omega$) [nm]', fontsize='x-large')
ax[0].plot(d_range,
           (np.array(realCompEigVals[0][0])+np.array(realCompEigVals[0][1]))/2,
           ls='--', alpha=0.3, label='Ecm')
for i in range(len(realCompEigVals[1])):
    ax[1].plot(d_range, realCompEigVals[1][i],
               alpha=0.65) #, label=names[i])
    ax[1].set_ylabel(r'Im($\omega$)', fontsize='x-large')
ax[0].legend()
ax[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
plt.xticks(np.linspace(d_range[0],d_range[-1],5))
plt.xlabel("nanobeams separation [nm]",fontsize='x-large')
plt.tight_layout()


## freq and Q-factor plot
for i in range(len(df_even_odd_modes[sweep_param].values.tolist())):
    ax[0].errorbar(df_even_odd_modes[sweep_param].values[i],
                   df_even_odd_modes['freq'].values[i],
                   yerr=df_even_odd_modes['error_real'].values[i],
                   fmt='.', capsize=3,
                   color=determine_mode_color(df_even_odd_modes,
                                              df_even_odd_modes[sweep_param].values[i],
                                              df_even_odd_modes['freq'].values[i]))
# delete duplicates in the list of sweeping param vals
all_sweep_param_vals = [*set(df_even_odd_modes[sweep_param].values.tolist())]
all_sweep_param_vals.sort()
ax[0].plot(all_sweep_param_vals,
           estimate_single_cav_resonance(df_even_odd_modes, all_sweep_param_vals),
           color='gray', linewidth=0.8, linestyle='--')

for i in range(len(df_even_odd_modes[sweep_param].values.tolist())):
    ax[1].errorbar(df_even_odd_modes[sweep_param].values[i],
                   df_even_odd_modes['decay'].values[i],
                   marker='1', capsize=3, alpha=0.25,
                   color=determine_mode_color(df_even_odd_modes,
                                              df_even_odd_modes[sweep_param].values[i],
                                              df_even_odd_modes['freq'].values[i]))
ax[1].set_ylabel('decay rate', size='x-large')

orange_patch = mpatches.Patch(color='orange', label='even mode')
blue_patch = mpatches.Patch(color='blue', label='odd mode')
circ_mark = Line2D([0], [0], marker='o', color='gray', label='frequency', lw=0)
tri_mark = Line2D([0], [0], marker='1', color='gray', label='Q-factor', lw=0)
plt.legend(handles=[orange_patch, blue_patch, circ_mark, tri_mark])
fig.tight_layout()
plt.show()
