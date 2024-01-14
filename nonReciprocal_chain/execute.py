import os
import sys
import numpy as np
import pandas as pd

## submit the simulation jobs to cluster
Resolution = [20]
latticeConstant = [0.33]
v = [0.3]
w = [0.3]
Lam_us = [0.85]
Lam_ss = [0.60]
NULL = ['True']
Animate = ['True']
Times = [0.1]
Nwvg_ups = [3]
Nwvg_los = [15]
numPairs = [6]
machine = 'GL'     ## 'MIC' or 'GL'


def configGen(depth, params, machine_shell_script):
    """
    generates a configuration of parameters in a string
    in order to sweeps all combinations of the parameters in lists
    depth: int, if depth = number of parameters required for one setting
                then submit the run
    params: dictionary, storing parameters for a single run
    machine_shell_script: choose which shell script to use based on device
    """
    global df
    if depth == num_params:
        name = '['
        for param_name in params:
            if (param_name != 'Animate' and param_name != 'Name'):
                name = name + str(params[param_name]) + ','
        name = name[:-1] + ']'
        params['Name'] = name
        df = pd.concat([df, pd.DataFrame(params, index = [params['Name']])])
        df.to_csv('parameters.csv')
        os.system('sbatch '+machine_shell_script+' '+str(name))
    else:
        for param in parameters[parameter_names[depth]]:
            params[parameter_names[depth]] = param
            configGen(depth + 1, params, machine_shell_script)

if machine=='GL':
    machine_shell_script='task_GL_automated.sh'
elif machine=='MIC':
    machine_shell_script='task_MIC_automated.sh'
else:
    print('check machine name')
    exit()

## parameter disctionary
parameters = {
    'Resolution': Resolution,
    'v': v,
    'w': w,
    'numPairs': numPairs,
    'Lam_ss': Lam_ss,
    'Lam_us': Lam_us,
    'NULL': NULL,
    'Animate': Animate,
    'Times': Times,
    'Nwvg_ups': Nwvg_ups,
    'Nwvg_los': Nwvg_los,
    'a': latticeConstant,
}


parameter_names = []
for param_name in parameters:
    parameter_names.append(param_name)
num_params = len(parameter_names)
params_0 = {}
df = pd.DataFrame()

## sweep the parameters
configGen(0, params_0, machine_shell_script)
