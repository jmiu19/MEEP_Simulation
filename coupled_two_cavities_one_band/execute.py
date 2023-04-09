import os
import sys
import numpy as np
import pandas as pd

## submit the simulation jobs to cluster
Resolution = [60]
Lam_us = [0.85]
Lam_ss = [0.6]
NULL = ['True']
Animate = ['True']
Times = [300]
Nwvg = [1,2,3,4]


def configGen(depth, params):
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



parameters = {
    'Resolution': Resolution,
    'Lam_ss': Lam_ss,
    'Lam_us': Lam_us,
    'NULL': NULL,
    'Animate': Animate,
    'Times': Times,
    'Nwvg': Nwvg,
}

parameter_names = []
for param_name in parameters:
    parameter_names.append(param_name)
num_params = len(parameter_names)
params_0 = {}
df = pd.DataFrame()

configGen(0, params_0)
