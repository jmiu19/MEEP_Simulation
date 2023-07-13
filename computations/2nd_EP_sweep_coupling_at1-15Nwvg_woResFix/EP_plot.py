import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit

####### model for fitting #################
def expFit(x, alpha, kappa, beta):
    return alpha * np.exp(-kappa*x) + beta


## Default constants
Ecm = 1.37124-0.00009j
XC = 1.37124-0.00009j
delGamma = 0.003166247j
presetW = 0.462

#######  reading data    ##################
df_coupling = pd.read_csv('coupling.csv')
df_width = pd.read_csv('width.csv')

widths = df_width['width'].values.tolist()
freqs = df_width['freq'].values.tolist()
dplusW = df_coupling['d+w']
Cs = df_coupling['C']

####### compute required width for single nanobeam with Nwvg=1 ###############
expParam_width, expCov_width = curve_fit(expFit, widths, freqs,
                                         p0=[0.005,0.005, 0.005], maxfev=10000)
alpha, kappa, beta = expParam_width[0], expParam_width[1], expParam_width[2]
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(6,3), dpi=150)
widthsForPlot = np.linspace(widths[0]*0.98, widths[-1]*1.02, 100)
ax.plot(widthsForPlot, expFit(widthsForPlot, alpha, kappa, beta),
           color='orange', alpha=0.3)
ax.scatter(widths, freqs)
plt.show()
targetFreq = 1.37124
targetWidth = np.log((targetFreq-beta)/alpha)/(-kappa)
print('computed width='+str(targetWidth)+
      ' for target freq='+str(targetFreq))

####### compute required coupling for a given loss difference ###############
targetLossDiff = 0.012456
amax = 401 # number of iteration when computing eigenvalues
Ecm = 1.371-0.00009j
ini_C = 0.0059
XC = 1.371-0.00009j
delGamma = targetLossDiff*1j

# generate 2D phase diagram displaying EP splitting around target loss diff.
df_Eigen = pd.DataFrame(columns=['eigVal_lossDiff_applied',
                                 'eigVec_lossDiff_applied',
                                 'eigVal_lossless',
                                 'eigVec_lossless',
                                 'Coupling coeff.',
                                 'Ecm',
                                 'XC',
                                 'Ecm-XC'])
for a in range(1,amax+1):
    C = ini_C + 0.0000015*(a-1)
    M = np.array([[ Ecm-delGamma, C  ],
                  [ C,            XC ]])
    H = np.array([[ Ecm, C  ],
                  [ C,   XC ]])
    MeigVal, MeigVec = np.linalg.eig(M)
    HeigVal, HeigVec = np.linalg.eig(H)
    # append eigenvals and eigenvectors to dataframe
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         HeigVal,
                                         HeigVec,
                                         C, Ecm,
                                         XC, Ecm-XC]

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
HrealEigVal1 = [vals[0] for vals in HrealEigVal]
HrealEigVal2 = [vals[1] for vals in HrealEigVal]
HrealVals = [HrealEigVal1, HrealEigVal2]

## plot the eigenvalues
Cs_eigen = df_Eigen['Coupling coeff.'].values.tolist()
names = ['Eigenval 1', 'Eigenval 2', 'Imag(', 'Re(']
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
for j in range(2):
    for i in range(len(realCompEigVals[j])):
        ax[j].plot(Cs_eigen, realCompEigVals[j][i], label=names[i])
        ax[j].set_ylabel(names[-j-1]+'E)', fontsize='x-large')
        if j==0:
            ax[j].plot(Cs_eigen, HrealVals[i],
                       label='lossless modes',
                       color='green', alpha=0.3)
plt.legend()
plt.xticks(np.linspace(Cs_eigen[0],Cs_eigen[-1],5))
plt.xlabel("coupling strength",fontsize='x-large')
plt.tight_layout()
plt.show()

## compute the target C when loss diff. is given by targetLossDiff
targetC_loss = [x for x in realCompEigVals[1][0]
                  if (abs(x)>0.0063 and abs(x)<0.0068)][0]
targetC_index = realCompEigVals[1][0].index(targetC_loss)
targetC = Cs_eigen[targetC_index]
print('computed at EP C='+str(targetC)+
      ' for target loss diff.='+str(targetLossDiff))

## compute the required separation distance when targetC is given
expParam_sep, expCov_sep = curve_fit(expFit, dplusW, Cs,
                                     p0=[0.005,0.005, 0.005], maxfev=10000)
# print('param [a, k, b] yields', expParam_sep)
# print('st. dev. [a, k, b] yields',
#       np.sqrt([expCov_sep[0][0], expCov_sep[1][1]]))

fig, ax = plt.subplots(figsize = (6,3), dpi = 150)
plt.scatter(dplusW, Cs, label='estimated coupling', color='orange')
plt.plot(dplusW,
         expFit(dplusW, expParam_sep[0], expParam_sep[1], expParam_sep[2]),
         label='exponential fit', color='blue')
plt.xlabel(r'd + width (micron)', size='x-large')
plt.ylabel(r'coupling strength',  size='x-large')
plt.legend(prop={'size':'x-large'})
plt.tight_layout()
plt.show()

alpha = expParam_sep[0]
kappa = expParam_sep[1]
beta = expParam_sep[2]
a = 0.33 # lattice constant
presetW = (1.4*a)/2+(targetWidth*a)/2
dplusW_computed = -np.log((targetC-beta)/alpha)/kappa
d_computed = dplusW_computed - presetW
print('computed sep='+str(d_computed)+' for target C='+str(targetC))




####### generate simulation results  ###############
expParam_width, expCov_width = curve_fit(expFit, dplusW, Cs, p0=[0.005,0.005, 0.005], maxfev=10000)
alpha, kappa, beta = expParam_width[0], expParam_width[1], expParam_width[2]
sim_df = pd.read_csv('sim_data.csv')
minC = min(sim_df['C'].values.tolist())*0.95
maxC = max(sim_df['C'].values.tolist())*1.05
C_range = np.linspace(0.95*minC, 1.05*maxC, 300)
d_range = [-np.log((targetC-beta)/alpha)/kappa-presetW for targetC in C_range]

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
ax[0].axvspan(1.05*sim_df['d'].values.tolist()[-1], d_computed, 
              color='red', alpha =0.1, lw =0)
ax[0].axvspan(d_computed, 0.9*sim_df['d'].values.tolist()[0], 
              color='green', alpha =0.1, lw =0)
ax[0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax[1].scatter(sim_df['d'], sim_df['decay_lossy'],
              label='lossy with high-Q', color='orange')
ax[1].scatter(sim_df['d'], sim_df['decay_lossless'],
              label='two high-Q', color='blue')
ax[1].set_ylabel('Im(freq.)', fontsize='x-large')
ax[1].axvspan(d_computed, 0.9*sim_df['d'].values.tolist()[0], 
              color='green', alpha =0.1, lw =0)
ax[1].axvspan(1.05*sim_df['d'].values.tolist()[-1], d_computed, 
              color='red', alpha =0.1, lw =0)
ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))


plt.legend(prop={'size': 'large'})
plt.xlabel("separation distance (nm)",fontsize='x-large')
plt.tight_layout()
plt.show()
