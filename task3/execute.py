import os
import sys
import numpy as np

"""
first argument: starting s_cav (microns)
second argument: step of s_cav (microns)
third argument: ending s_cav (microns)
"""
try:
    start = sys.argv[0]
    end = sys.argv[2]
    step = sys.argv[1]
except:
    start = 0.11
    step = 0.05
    end = 0.180 + step

s_cavs = np.arange(start,end+step,step)
for s_cav in s_cavs:
    os.system('sbatch task3_automated.sh '+str(s_cav))

for s_cav in s_cavs:
    print('Job for scav = '+str(s_cav)+' has been submitted.')
