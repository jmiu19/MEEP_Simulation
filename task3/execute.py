import os
import sys
import numpy as np


## submit the simulation jobs to cluster
Lam_us = np.round(np.arange(0.75,0.80+0.01,0.01),2)
Lam_ss = np.round(np.arange(0.72,0.77+0.01,0.01),2)
for i in range(len(Lam_us)):
    os.system('sbatch task3_automated.sh '+str(Lam_us[i])+' '+str(Lam_ss[i]))
    print('Job for Lam_u = '+str(Lam_us[i])+' has been submitted.')
