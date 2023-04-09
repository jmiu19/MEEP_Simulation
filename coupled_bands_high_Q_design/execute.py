import os
import sys
import numpy as np


## submit the simulation jobs to cluster
Resolution = 60
Seps = [0.075]
Lam_us = [1.59, 1.56, 1.59]
Lam_ss = [1.55, 1.53, 1.53]
NULL = ['True']
Animate = 'True'
Times = [500, 800]

for i in range(len(Lam_us)):
    for sep in Seps:
        for null in NULL:
            for time in Times:
                name = ('['+str(Resolution)+','
                           +str(Lam_us[i]) +','
                           +str(Lam_ss[i]) +','
                           +str(sep)       +','
                           +str(time)      +','
                           +str(null)      +']')
                os.system('sbatch task3_automated.sh '+str(Lam_us[i]) +' '
                                                      +str(Lam_ss[i]) +' '
                                                      +str(Resolution)+' '
                                                      +str(sep)       +' '
                                                      +str(null)      +' '
                                                      +str(Animate)   +' '
                                                      +str(time)      +' '
                                                      +name)
                print('Job for ('+str(Resolution)+','
                                 +str(Lam_us[i]) +','
                                 +str(Lam_ss[i]) +','
                                 +str(sep)       +','
                                 +str(time)      +','
                                 +str(null)      +') has been submitted.')
