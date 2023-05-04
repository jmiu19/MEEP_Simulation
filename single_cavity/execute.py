import os
import sys
import numpy as np


## submit the simulation jobs to cluster
Lam_us = np.round(0.8,2)
Lam_ss = np.round(0.65,2)
width = [1.4, 1.45, 1.5]
radius = [0.34, 0.35, 0.345]
for i in range(len(width)):
    for j in range(len(radius)):
        os.system('sbatch task3_automated.sh '+str(Lam_us)+' '+str(Lam_ss)+' '+str(width[i])+' '+str(radius[j]))
        print('Job for Lam_u = '+str(width[i])+' has been submitted.')
