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
ini_C = 0.0059
CPhase = 0.0001j
delGamma = 0.0178j

m11 = Ecm1 + intrinsicGain1 + delGamma
m22 = Ecm2 + intrinsicGain2


# generate 2D phase diagram displaying EP splitting around target loss diff.
df_Eigen = pd.DataFrame(columns=['eigVal',
                                 'eigVec',
                                 'Coupling coeff.',
                                 'Ecm',
                                 'XC',
                                 'detuning'])
for a in range(1,amax+1):
    C = ini_C + 0.000015*(a-1) + CPhase
    M = np.array([[ m11,  C   ],
                  [ C,    m22 ]])
    MeigVal, MeigVec = np.linalg.eig(M)
    # append eigenvals and eigenvectors to dataframe
    df_Eigen.loc[len(df_Eigen.index)] = [MeigVal,
                                         MeigVec,
                                         C, m11, m22,
                                         Ecm1-Ecm2]

## loss difference applied eigenvals
realEigVal = np.real(df_Eigen['eigVal'].values.tolist())
compEigVal = np.imag(df_Eigen['eigVal'].values.tolist())
realEigVal1 = [vals[0] for vals in realEigVal]
realEigVal2 = [vals[1] for vals in realEigVal]
compEigVal1 = [vals[0] for vals in compEigVal]
compEigVal2 = [vals[1] for vals in compEigVal]
# sort the eigenvalues
for i in range(len(realEigVal1)):
    if (realEigVal2[i]>realEigVal1[i]):
        val = realEigVal1[i]
        realEigVal1[i] = realEigVal2[i]
        realEigVal2[i] = val
        val = compEigVal1[i]
        compEigVal1[i] = compEigVal2[i]
        compEigVal2[i] = val
    if abs(realEigVal2[i]-realEigVal1[i])<0.00001:
        if (compEigVal2[i]>compEigVal1[i]):
            val = realEigVal1[i]
            realEigVal1[i] = realEigVal2[i]
            realEigVal2[i] = val
            val = compEigVal1[i]
            compEigVal1[i] = compEigVal2[i]
            compEigVal2[i] = val


realCompEigVals = [[realEigVal1, realEigVal2], [compEigVal1, compEigVal2]]




## plot the eigenvalues
Cs_eigen = df_Eigen['Coupling coeff.'].values.tolist()
names = ['Eigenval 1', 'Eigenval 2', 'Imag(', 'Re(']
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
for j in range(2):
    for i in range(len(realCompEigVals[j])):
        ax[j].plot(Cs_eigen, realCompEigVals[j][i], label=names[i])
        ax[j].set_ylabel(names[-j-1]+'E)', fontsize='x-large')
plt.legend()
plt.xticks(np.linspace(Cs_eigen[0],Cs_eigen[-1],5))
plt.xlabel("coupling strength",fontsize='x-large')
plt.tight_layout()
plt.show()
