import os
import sys
import numpy as np


## submit the simulation jobs to cluster
Lam_us = np.round(np.arange(0.42,1.22+0.05,0.03),2)
Lam_ss = np.round(np.arange(0.47,1.27+0.05,0.03),2)
for i in range(len(Lam_us)):
    os.system('sbatch task3_automated.sh '+str(Lam_us[i])+' '+str(Lam_ss[i]))
    print('Job for Lam_u = '+str(Lam_us[i])+' has been submitted.')
