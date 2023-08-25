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
Ecm = 1.3715-0.00009j
XC = 1.3715-0.00009j
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
print(minC)
C_range = np.linspace(0.95*minC, 1.05*maxC, 300)
d_range = [-np.log(targetC/alpha)/kappa-presetW for targetC in C_range]

df_Eigen = pd.DataFrame(columns=['eigVal_lossDiff_applied',
                                 'eigVec_lossDiff_applied',
                                 'eigVal_lossless',
                                 'eigVec_lossless',
                                 'Coupling coeff.',
                                 'Ecm',
                                 'XC',
                                 'Ecm-XC'])

for C in C_range:
    M = np.array([[ Ecm-delGamma, C  ],
                  [ C,            XC ]])
    H = np.array([[ Ecm, C  ],
                  [ C,   XC ]])
    MeigVal, MeigVec = np.linalg.eig(M)
    HeigVal, HeigVec = np.linalg.eig(H)
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         HeigVal,
                                         HeigVec,
                                         C, Ecm,
                                         XC, Ecm-XC]

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
fig, ax = plt.subplots(3, 1, sharex=True, figsize=(6,9), dpi=100)

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
ax[0].set_ylabel('Re(freq.)', fontsize='x-large')
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
ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[2].scatter(sim_df['d'], 1/sim_df['freq_lossy'].values,
              label='lossy with high-Q', color='orange')
for i in range(len(realCompEigVals[0])):
    ax[2].plot(d_range, 1/np.array(realCompEigVals[0][i]),
               color='orange', alpha=0.3)
ax[2].set_ylabel('Wavelength [um]', fontsize='x-large')
ax[2].axvspan (0.51, 0.561, color='red', alpha =0.1, lw =0)
ax[2].axvspan (0.561, 0.605, color='green', alpha =0.1, lw =0)
ax[2].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
ax[2].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[1].legend(prop={'size': 'large'})
plt.xlabel("separation distance (um)",fontsize='x-large')
plt.tight_layout()
plt.show()
