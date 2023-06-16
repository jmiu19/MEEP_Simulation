import os
import sys
import numpy as np


## submit the simulation jobs to cluster
Lam_us = np.round(0.8,2)
Lam_ss = np.round(0.65,2)
Res = 80
Nwvgs = [3,4,5,6,8,10,12,15]
for i in range(len(Nwvgs)):
    os.system('sbatch task_automated.sh '+str(Res)+' '+str(Lam_us)+' '+str(Lam_ss)+' '+str(Nwvgs[i]))
    print('Job '+str(i)+' has been submitted.')
