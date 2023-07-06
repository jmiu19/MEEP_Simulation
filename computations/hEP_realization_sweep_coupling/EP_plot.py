import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit

########################################
##                                    ##
##       Setting up the model         ##
##                                    ##
########################################
def expFit(x, alpha, kappa):
    return alpha * np.exp(-kappa*x)


## Default constants
Ecm = 1.3712-0.00009j
XC = 1.3712-0.00009j
delGamma = 0.003166247j
presetW = 0.462

########################################
##                                    ##
##          Simulation data           ##
##                                    ##
########################################
df = pd.read_csv('coupling.csv')
dplusW = df['d+w']
C = df['C']

expParam, expCov = curve_fit(expFit, dplusW, C, p0=[0.005,0.005], maxfev=10000)
alpha, kappa = expParam[0], expParam[1]

sim_df = pd.read_csv('sim_data.csv')
minC = min(sim_df['C'].values.tolist())
maxC = max(sim_df['C'].values.tolist())
C_range = np.linspace(0.95*minC, 1.05*maxC, 300)
d_range = [-np.log(targetC/alpha)/kappa-presetW for targetC in C_range]

df_Eigen = pd.DataFrame(columns=['eigVal_lossDiff_applied',
                                 'eigVec_lossDiff_applied',
                                 'eigVal_lossless',
                                 'eigVec_lossless',
                                 'Coupling C',
                                 'Coupling Omega/2'
                                 'Ecm',
                                 'detuning',
                                 'Ecm-XC'])

for C in C_range:
    M = np.array([[ Ecm-delGamma,          C,                    Omega/2],
                  [ C,                   Ecm,                    Omega/2],
                  [ Omega/2,         Omega/2,    Ecm+detuning-delGamma/2]])
    H = np.array([[ Ecm,                   C,         Omega/2],
                  [ C,                   Ecm,         Omega/2],
                  [ Omega/2,         Omega/2,    Ecm+detuning]])
    MeigVal, MeigVec = np.linalg.eig(M)
    HeigVal, HeigVec = np.linalg.eig(H)
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal, 
                                         MeigVec, 
                                         HeigVal, 
                                         HeigVec, 
                                         C, Omega/2,
                                         Ecm, 
                                         detuning, 
                                         Ecm-XC]

########################################
##                                    ##
##          Extracting data           ##
##                                    ##
########################################
## loss difference applied eigenvals
realEigVal = np.real(df_Eigen['eigVal_lossDiff_applied'].values.tolist())
compEigVal = np.imag(df_Eigen['eigVal_lossDiff_applied'].values.tolist())
realEigVal1 = [vals[0] for vals in realEigVal]
realEigVal2 = [vals[1] for vals in realEigVal]
compEigVal1 = [vals[0] for vals in compEigVal]
compEigVal2 = [vals[1] for vals in compEigVal]
realCompEigVals = [[realEigVal1, realEigVal2], [compEigVal1, compEigVal2]]

## lossless eigvals
HrealEigVal = np.real(df_Eigen['eigVal_lossless'].values.tolist())
HcompEigVal = np.imag(df_Eigen['eigVal_lossless'].values.tolist())
HrealEigVal1 = [vals[0] for vals in HrealEigVal]
HrealEigVal2 = [vals[1] for vals in HrealEigVal]
HcompEigVal1 = [vals[0] for vals in HcompEigVal]
HcompEigVal2 = [vals[1] for vals in HcompEigVal]
HrealCompEigVals = [[HrealEigVal1, HrealEigVal2], [HcompEigVal1, HcompEigVal2]]



########################################
##                                    ##
##            Generate plots          ##
##                                    ##
########################################
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)

for j in range(2):
    for i in range(len(realCompEigVals[j])):
        ax[j].plot(d_range, realCompEigVals[j][i], 
                   color='orange', alpha=0.3)
        ax[j].plot(d_range, HrealCompEigVals[j][i], 
                   color='blue', alpha=0.3)


ax[0].scatter(sim_df['d'], sim_df['freq_lossy'], 
              label='lossy with high-Q', color='orange')
ax[0].scatter(sim_df['d'], sim_df['freq_lossless'], 
              label='two high-Q', color='blue')
ax[0].set_ylabel('Re(freq.) (Meep unit)', fontsize='x-large')
ax[0].axvspan (0.51, 0.5603, color='red', alpha =0.1, lw =0)
ax[0].axvspan (0.5603, 0.605, color='green', alpha =0.1, lw =0)
ax[0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[1].scatter(sim_df['d'], sim_df['decay_lossy'], 
              label='lossy with high-Q', color='orange')
ax[1].scatter(sim_df['d'], sim_df['decay_lossless'], 
              label='two high-Q', color='blue')
ax[1].set_ylabel('Im(freq.)', fontsize='x-large')
ax[1].axvspan (0.51, 0.561, color='red', alpha =0.1, lw =0)
ax[1].axvspan (0.561, 0.605, color='green', alpha =0.1, lw =0)
ax[1].ticklabel_format(axis='y',style='sci',scilimits=(0,0))

plt.legend(prop={'size': 'large'})
plt.xlabel("separation distance (nm)",fontsize='x-large')
plt.tight_layout()
plt.show()








