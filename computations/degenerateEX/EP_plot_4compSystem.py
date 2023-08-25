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
detuning = -0.52*0.012438968/2
EXl = 1.371 + detuning
EXr = 1.371 + detuning
ini_C = 0.000
CPhase = 0j
delEcmGamma = -0.012438968j
delExGamma = -0.012438968j/2
Omega = 0.72*0.012438968/2

m11 = Ecm1 + intrinsicGain1 + delEcmGamma
m22 = Ecm2 + intrinsicGain2
m33 = EXl  + intrinsicGain2 + delExGamma
m44 = EXr  + intrinsicGain2 + delExGamma

# generate 2D phase diagram displaying EP splitting around target loss diff.
df_Eigen = pd.DataFrame(columns=['eigVal',
                                 'eigVec',
                                 'Coupling coeff.',
                                 'Ecm1',
                                 'Ecm2',
                                 'XC',
                                 'detuning'])
for a in range(1,amax+1):
    C = ini_C + 0.000008*(a-1) + CPhase
    M = np.array([[ m11,   C,     Omega/2, Omega/2 ],
                  [ C,     m22,   Omega/2, Omega/2 ],
                  [ Omega/2, Omega/2, m33,   0     ],
                  [ Omega/2, Omega/2, 0,     m44   ]])
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
realEigVal4 = []
compEigVal1 = []
compEigVal2 = []
compEigVal3 = []
compEigVal4 = []


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
    for m in range(len(realVals)):
        if abs(realVals[m]-EXl)<0.00000001:
            realVal = realVals[m]
            compVal = compVals[m]
            for n in range(len(realVals)-m-1):
                realVals[m+n] = realVals[m+n+1]
                compVals[m+n] = compVals[m+n+1]
            realVals[-1] = realVal
            compVals[-1] = compVal
    realEigVal1.append(realVals[0])
    realEigVal2.append(realVals[1])
    realEigVal3.append(realVals[2])
    realEigVal4.append(realVals[3])
    compEigVal1.append(compVals[0])
    compEigVal2.append(compVals[1])
    compEigVal3.append(compVals[2])
    compEigVal4.append(compVals[3])



realCompEigVals = [[realEigVal1, realEigVal2, realEigVal3, realEigVal4],
                   [compEigVal1, compEigVal2, compEigVal3, compEigVal4]]



## plot the eigenvalues
Cs_eigen = df_Eigen['Coupling coeff.'].values.tolist()
Cs_nm = [1000/(Ecm1-c)-1000/Ecm1 for c in Cs_eigen]
Cex_nm = 1000/(Ecm1-(Omega/2))-1000/Ecm1
Detuning_nm = 1000/(Ecm1+detuning)-1000/Ecm1
print('cav-Ex coupling = '+str(Cex_nm)+' nm')
print('detuning = '+ str(Detuning_nm)+' nm')
names = ['Eigenval 1', 'Eigenval 2', 'Eigenval 3', 'Eigenval 4', 'Imag(', 'Re(']
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(6,6), dpi=150)
ax[0].plot([Cs_nm[0], Cs_nm[-1]], [1000/EXl, 1000/EXl], ls='--', alpha=0.3)
for i in range(len(realCompEigVals[0])):
    ax[0].plot(Cs_nm, 1000/np.array(realCompEigVals[0][i]),
               alpha=0.5, label=names[i])
    ax[0].set_ylabel(r'Re($\lambda$) [nm]', fontsize='x-large')
for i in range(len(realCompEigVals[1])):
    ax[1].plot(Cs_nm, realCompEigVals[1][i],
               alpha=0.5, label=names[i])
    ax[1].set_ylabel(r'Im($\omega$)', fontsize='x-large')
ax[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
plt.legend()
plt.xticks(np.linspace(Cs_nm[0],Cs_nm[-1],5))
plt.xlabel("cavities coupling [nm]",fontsize='x-large')
plt.tight_layout()
plt.show()
