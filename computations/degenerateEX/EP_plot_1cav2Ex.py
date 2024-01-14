import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit

####### compute required coupling for a given loss difference ###############
amax = 401 # number of iteration when computing eigenvalues
intrinsicGain1 = -0.00009j
intrinsicGain2 = -0.00009j
Ecm1 = 1.371
Ecm2 = 1.371
detuning = -0.0007
EXl = 1.371 + detuning
ini_C = 0
CPhase = 0j
delEcmGamma = 0 #0.003166247j
delExGamma = 0 #0.003166247j/2

m11 = Ecm1 + intrinsicGain1 + delEcmGamma
m22 = Ecm2 + intrinsicGain2
m33 = EXl + intrinsicGain2 + delExGamma

# generate 2D phase diagram displaying EP splitting around target loss diff.
df_Eigen = pd.DataFrame(columns=['eigVal',
                                 'eigVec',
                                 'Coupling coeff.',
                                 'Ecm1',
                                 'Ecm2',
                                 'XC',
                                 'detuning'])
for a in range(1,amax+1):
    C = ini_C + 0.000015*(a-1) + CPhase
    M = np.array([[ m11,   C,     C     ],
                  [ C,     m33,   0     ],
                  [ C,     0,     m33   ]])
    MeigVal, MeigVec = np.linalg.eig(M)
    # append eigenvals and eigenvectors to dataframe
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         C, m11, m22, m33,
                                         Ecm1-EXl]

## loss difference applied eigenvals
realEigVal = np.real(df_Eigen['eigVal'].values.tolist())
compEigVal = np.imag(df_Eigen['eigVal'].values.tolist())
realEigVal1 = []
realEigVal2 = []
realEigVal3 = []
compEigVal1 = []
compEigVal2 = []
compEigVal3 = []


# sort the eigenvalues
for i in range(len(realEigVal)):
    realVals = realEigVal[i]
    compVals = compEigVal[i]
    for j in range(len(realVals)):
        for k in range(len(realVals)-j-1):
            if (realVals[k]-realVals[k+1])>0.00001:
                val = realVals[k]
                realVals[k] = realVals[k+1]
                realVals[k+1] = val
                val = compVals[k]
                compVals[k] = compVals[k+1]
                compVals[k+1] = val
            elif abs(realVals[k]-realVals[k+1])<=0.00001:
                if (compVals[k]-compVals[k+1])>0.00001:
                    val = realVals[k]
                    realVals[k] = realVals[k+1]
                    realVals[k+1] = val
                    val = compVals[k]
                    compVals[k] = compVals[k+1]
                    compVals[k+1] = val
    realEigVal1.append(realVals[0])
    realEigVal2.append(realVals[1])
    realEigVal3.append(realVals[2])
    compEigVal1.append(compVals[0])
    compEigVal2.append(compVals[1])
    compEigVal3.append(compVals[2])



realCompEigVals = [[realEigVal1, realEigVal2, realEigVal3],
                   [compEigVal1, compEigVal2, compEigVal3]]




## plot the eigenvalues
Cs_eigen = df_Eigen['Coupling coeff.'].values.tolist()
names = ['Eigenval 1', 'Eigenval 2', 'Eigenval 3', 'Eigenval 4', 'Imag(', 'Re(']
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
for j in range(2):
    for i in range(len(realCompEigVals[j])):
        ax[j].plot(Cs_eigen, realCompEigVals[j][i], label=names[i], alpha=0.5)
        ax[j].set_ylabel(names[-j-1]+'E)', fontsize='x-large')
ax[0].plot(Cs_eigen, [EXl for i in range(len(Cs_eigen))],
           label='Ex', alpha=0.2, ls='--')
ax[0].legend()
plt.xticks(np.linspace(Cs_eigen[0],Cs_eigen[-1],5))
plt.xlabel("coupling strength",fontsize='x-large')
plt.tight_layout()
plt.show()
