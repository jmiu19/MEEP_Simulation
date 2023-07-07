import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit

def expFit(x, alpha, kappa, beta):
    return alpha * np.exp(-kappa*x)+beta

def polyFit(x, alpha, kappa, beta):
    return alpha*x + beta*x**3 + kappa


df = pd.read_csv('single_cav_vary_Nwvg.csv')
df.columns = ['Nwvg', 'freq', 'decay', 'Q', 'lamb', 'lossDiff']

expParam_decay, expCov_decay = curve_fit(expFit, df['Nwvg'], df['decay'],
                                         p0=[0.005,0.005, 0.005], maxfev=10000)
print('a*e^{-kx}+b')
print('param [a, k, b] yields', expParam_decay)
print('st. dev. [a, k, b] yields', np.sqrt([expCov_decay[0][0],
                                            expCov_decay[1][1],
                                            expCov_decay[2][2]]))


fit_x = np.linspace(df['Nwvg'].values.tolist()[0]*0.95,
                    df['Nwvg'].values.tolist()[-1]*1.05, 100)
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
plt.scatter(df['Nwvg'], df['decay'], color='orange')
plt.plot(fit_x, expFit(fit_x, expParam_decay[0],
                       expParam_decay[1], expParam_decay[2]),
         label='exponential fit', color='blue')
plt.xlabel(r'number of waveguide holes', size='x-large')
plt.ylabel(r'decay rate',  size='x-large')
plt.legend(prop={'size':'x-large'})
plt.tight_layout()
plt.show()


df_1to6holes = df[df['Nwvg']<=6]
polyParam_lam, polyCov_lam = curve_fit(polyFit,
                                       df_1to6holes['decay'],
                                       df_1to6holes['lamb'],
                                       p0=[0.005,0.005, 0.005], maxfev=10000)

fit_decay = np.linspace(df['decay'].values.tolist()[0]*0.95,
                        df['decay'].values.tolist()[-1]*1.05, 100)
fig, ax = plt.subplots(figsize = (6,4), dpi = 150)
plt.scatter(df['decay'], df['lamb'], color='orange')
plt.plot(fit_decay, polyFit(fit_decay, polyParam_lam[0],
                            polyParam_lam[1], polyParam_lam[2]),
         label='exponential fit', color='blue')
plt.xlabel(r'decay of waveguide', size='x-large')
plt.ylabel(r'wavelength (nm)',  size='x-large')
plt.legend(prop={'size':'x-large'})
plt.tight_layout()
plt.show()




########################################
##                                    ##
##       Setting up the model         ##
##                                    ##
########################################

## Default constants
targetC = 0.00162
highQ_decay = df[df['Nwvg']==max(df['Nwvg'])]['decay'].values[0]
lowQ_decay = df[df['Nwvg']==min(df['Nwvg'])]['decay'].values[0]
ini_gamma = abs(highQ_decay-lowQ_decay)
Ecm = 1.3712-highQ_decay*1j
XC = 1.3712-highQ_decay*1j


## Create empty dataframe for storing data
df_Eigen = pd.DataFrame(columns=['eigVal_lossDiff_applied',
                                 'eigVec_lossDiff_applied',
                                 'eigVal_lossless',
                                 'eigVec_lossless',
                                 'coupling_coeff.',
                                 'loss_diff',
                                 'Ecm',
                                 'XC',
                                 'Ecm-XC'])

########################################
##                                    ##
##         Compute Eigenvals          ##
##                                    ##
########################################
for gamma in np.linspace(1.05*lowQ_decay,
                         0.95*highQ_decay, 300):
    Ecm = 1/polyFit(gamma, polyParam_lam[0],
                    polyParam_lam[1], polyParam_lam[2])
    M = np.array([[ Ecm-gamma*1j,   targetC ],
                  [ targetC,             XC ]])
    H = np.array([[ Ecm,     targetC ],
                  [ targetC,      XC ]])
    MeigVal, MeigVec = np.linalg.eig(M)
    HeigVal, HeigVec = np.linalg.eig(H)
    idx_M = MeigVal.argsort()[::-1]
    MeigVal = MeigVal[idx_M]
    idx_H = HeigVal.argsort()[::-1]
    HeigVal = HeigVal[idx_H]
    # append eigenvals and eigenvectors to dataframe
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         HeigVal,
                                         HeigVec,
                                         targetC,
                                         gamma,
                                         Ecm, XC,
                                         Ecm-XC]

## output the dataframe
df_Eigen.to_csv('result.csv')



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
Gammas = df_Eigen['loss_diff'].values.tolist()
sim_df = pd.read_csv('couple_cav_vary_Nwvg.csv')


fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
for j in range(2):
    for i in range(len(realCompEigVals[j])):
        ax[j].plot(Gammas, realCompEigVals[j][i],
                   color='orange', alpha=0.3)
        ax[j].plot(Gammas, HrealCompEigVals[j][i],
                   color='blue', alpha=0.3)
    for decay in df['lossDiff']:
        ax[j].axvline(x=decay, color='gray', alpha=0.3)

ax[0].scatter(sim_df['lossDiff'], sim_df['freq'], color='orange')
ax[1].scatter(sim_df['lossDiff'], -sim_df['decay'], color='orange')

ax[1].set_ylabel('Im(freq.)', fontsize='x-large')
ax[0].set_ylabel('Re(freq.)', fontsize='x-large')
plt.legend(prop={'size': 'large'})
plt.xlabel("loss difference",fontsize='x-large')
plt.tight_layout()
plt.show()
