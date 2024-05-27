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
def exp(x, alpha, kappa):
    return alpha * np.exp(-kappa*x)

def twoLevelEigVal(delGamma, C, selfCoupAdjust):
    Ecm = Ecm0-delGamma+selfCoupAdjust
    Ex = XC+selfCoupAdjust
    b = -(Ecm+Ex)
    a = 1
    c = (Ecm*Ex - C**2)
    E1 = (-b+np.sqrt((b**2)-4*a*c))/(2*a)
    E2 = (-b-np.sqrt((b**2)-4*a*c))/(2*a)
    return [E1, E2]

def realEigValFromDists(dists, alphaE, kappaE, alphaC, kappaC, delGamma):
    selfCoupAdjust = np.array(exp(dists, alphaE, kappaE))
    C = np.array(exp(dists, alphaC, kappaC))
    EigVals = twoLevelEigVal(delGamma, C, selfCoupAdjust)
    EigVals = np.transpose(EigVals)
    RealEigVals = np.sort(np.real(EigVals))
    return RealEigVals

def compEigValFromDists(dists, alphaE, kappaE, alphaC, kappaC, delGamma):
    selfCoupAdjust = np.array(exp(dists, alphaE, kappaE))
    C = np.array(exp(dists, alphaC, kappaC))
    EigVals = twoLevelEigVal(delGamma, C, selfCoupAdjust)
    EigVals = np.transpose(EigVals)
    compEigVals = np.sort(np.imag(EigVals))
    return compEigVals

def fitSelfCoupAdjust(dists):
    dfs = [df[df['d+w']==d] for d in dists]
    avgVals = np.array([np.sum(df_d['freq'].values) for df_d in dfs])/2-np.real(Ecm0)
    expParam, expCov = curve_fit(exp, dists, avgVals,
                                 p0=[-8,13], maxfev=10000)
    return expParam, expCov

def diffAnaSim_EfromDist(dists, alphaC, kappaC):
    expParams_E, _ = fitSelfCoupAdjust(dists)
    anaVals = realEigValFromDists(dists, *expParams_E, alphaC, kappaC, 0)
    dfs_dists = [df[df['d+w']==d] for d in dists]
    simVals = np.array([np.sort(df['freq'].values) for df in dfs_dists])
    errors = anaVals-simVals
    sum_error_sqred = [sum(error**2) for error in errors]
    return sum_error_sqred


########################################
##                                    ##
##          Simulation data           ##
##                                    ##
########################################
df = pd.read_csv('coupling_data.csv')
dists = np.array(list(dict.fromkeys(df['d+w'].values.tolist())))

df_EP = pd.read_csv('EP_sweep_data.csv')
dists_EP = np.array(list(dict.fromkeys(df_EP['d+w'].values.tolist())))


dfs = [df[df['d+w']==d] for d in dists]
avgVals = np.array([np.sum(df_d['freq'].values) for df_d in dfs])/2

## Default constants
intrinsicLoss = -0.00000j
Ecm0 = 1.37124+intrinsicLoss
XC   = 1.37124+intrinsicLoss
delGamma = 0.003366247j
presetW = 0.462


expParams_E, _ = fitSelfCoupAdjust(dists)
expParams_C, cov = curve_fit(diffAnaSim_EfromDist, dists,
                             [0.0]*len(dists), p0=[0.36,5.32], maxfev=10000)


dists_linspace = np.linspace(0.9,1.15,100)
lossLessVals = realEigValFromDists(dists_linspace,
                                   *expParams_E, *expParams_C, 0)
lossLessVals = np.transpose(lossLessVals).tolist()
avgLossLessVals = (np.array(lossLessVals[0])+np.array(lossLessVals[1]))/2
lossyVals = realEigValFromDists(dists_linspace,
                                *expParams_E, *expParams_C, delGamma)
lossyVals_imag = compEigValFromDists(dists_linspace,
                                    *expParams_E, *expParams_C, delGamma)
lossyVals = np.transpose(lossyVals).tolist()
lossyVals_imag = np.transpose(lossyVals_imag).tolist()

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(5,4.5), dpi=150)
ax.plot(dists_linspace, np.array(lossLessVals[0]), color='red', alpha=0.2)
ax.plot(dists_linspace, np.array(lossLessVals[1]), color='blue', alpha=0.2)
ax.plot(dists_linspace, np.array(lossyVals[0]), color='r', linestyle='--')
ax.plot(dists_linspace, np.array(lossyVals[1]), color='b', linestyle='--')
DpW = df['d+w'].values.tolist()
DpW_EP = df_EP['d+w'].values.tolist()
# for i in range(len(DpW)):
#     if DpW[i]>0.9:
#         f = df['freq'].values.tolist()[i]
#         plt.errorbar(DpW[i], f, xerr = 1/160, color='orange')
for i in range(len(DpW_EP)):
    f = df_EP['freq'].values.tolist()[i]
    fErr = df_EP['freqError'].values.tolist()[i]
    ax.errorbar(DpW_EP[i], f, yerr = fErr, color='orange',
                 fmt='o', markersize=1, capsize=5)
# ax.set_xticks([0.66,0.73,0.8])
# ax.set_yticks([1/0.724,1/0.728,1/0.732,1/0.736])
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.ylabel(r"frequency [meep unit]",fontsize='x-large')
plt.xlabel(r"$d+w$ [$\mu$m]",fontsize='x-large')
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(1, 1, sharex=True, figsize=(5,4.5), dpi=150)
ax.plot(dists_linspace, np.array(lossyVals_imag[0]), color='red', linestyle='--')
ax.plot(dists_linspace, np.array(lossyVals_imag[1]), color='blue', linestyle='--')
# ax.plot(dists_linspace, np.array(lossyVals[0]), color='r', linestyle='--')
# ax.plot(dists_linspace, np.array(lossyVals[1]), color='b', linestyle='--')
for i in range(len(DpW_EP)):
    f = df_EP['decay'].values.tolist()[i]
    fErr = df_EP['decayError'].values.tolist()[i]
    ax.errorbar(DpW_EP[i], f, yerr = fErr, color='orange',
                 fmt='o', markersize=1, capsize=5)
# ax.set_xticks([0.66,0.73,0.8])
# ax.set_yticks([1/0.724,1/0.728,1/0.732,1/0.736])
# ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.ylabel(r"decay [meep unit]",fontsize='x-large')
plt.xlabel(r"$d+w$ [$\mu$m]",fontsize='x-large')
plt.tight_layout()
plt.show()



dists = np.array(list(dict.fromkeys(df[df['d+w']<=0.85]['d+w'].values.tolist())))
dfs = [df[df['d+w']==d] for d in dists]
avgVals = np.array([np.sum(df_d['freq'].values) for df_d in dfs])/2

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(3.5,4.5), dpi=150)
df_toplot = df[df['d+w']<=0.85]
ax.scatter(df_toplot['d+w'], df_toplot['freq'], s=19, label='modes', color='b')
ax.scatter(dists, avgVals, s=19, label='average', color='orange')
# ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.set_xticks([0.66,0.73,0.8])
ax.set_yticks([1/0.724,1/0.728,1/0.732,1/0.736])
ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
plt.ylabel(r"frequency [meep unit]",fontsize='x-large')
plt.xlabel(r"$d+w$ [$\mu$m]",fontsize='x-large')
plt.legend(fontsize='large')
plt.tight_layout()
plt.show()


avgValsNormalized = Ecm0 - np.array([np.sum(df_d['freq'].values) for df_d in dfs])/2
coupling = np.array([np.max(dfs[i]['freq'].values)-(Ecm0+avgValsNormalized[i]) for i in range(len(dfs))])
expParamMu, expCovMu = curve_fit(exp, dists, avgValsNormalized,
                                 p0=[8,13], maxfev=10000)
expParamC, expCovC = curve_fit(exp, dists, coupling,
                               p0=[8,13], maxfev=10000)
distsForPlot = np.linspace(dists[0], dists[-1],100)
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(3.5,4.5), dpi=150)
ax.scatter(dists, avgValsNormalized, color='b', s=19)
ax.scatter(dists, coupling, color='orange', s=19)
ax.plot(distsForPlot, exp(distsForPlot, *expParamMu), label=r'$\mu$', color='b')
ax.plot(distsForPlot, exp(distsForPlot, *expParamC), label=r'$c$', color='orange')
ax.set_xticks([0.66,0.73,0.8])
# ax.set_yticks([0.724,0.728,0.732, 0.736])
# plt.ylabel(r"frequency [mp unit]",fontsize='x-large')
plt.xlabel(r"$d+w$ [$\mu$m]",fontsize='x-large')
plt.legend(fontsize='large')
plt.tight_layout()
plt.show()
