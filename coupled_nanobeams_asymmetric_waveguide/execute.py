import os
import sys
import numpy as np
import pandas as pd

## submit the simulation jobs to cluster
Resolution = [80]
Seps = [0.1+i*0.005 for i in range(3)]
Lam_us = [0.85]
Lam_ss = [0.60]
NULL = ['True']
Animate = ['True']
Times = [300]
Nwvg_ups = [10]
Nwvg_los = [10]


def configGen(depth, params):
    """
    generates a configuration of parameters in a string
    in order to sweeps all combinations of the parameters in lists
    depth: int, if depth = number of parameters required for one setting
                then submit the run
    params: dictionary, storing parameters for a single run
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
        os.system('sbatch task3_automated.sh ' + str(name))
    else:
        for param in parameters[parameter_names[depth]]:
            params[parameter_names[depth]] = param
            configGen(depth + 1, params)

## parameter disctionary
parameters = {
    'Resolution': Resolution,
    'Seps': Seps,
    'Lam_ss': Lam_ss,
    'Lam_us': Lam_us,
    'NULL': NULL,
    'Animate': Animate,
    'Times': Times,
    'Nwvg_ups': Nwvg_ups,
    'Nwvg_los': Nwvg_los,
}


parameter_names = []
for param_name in parameters:
    parameter_names.append(param_name)
num_params = len(parameter_names)
params_0 = {}
df = pd.DataFrame()

## sweep the parameters
configGen(0, params_0)
