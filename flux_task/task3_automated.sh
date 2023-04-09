#!/bin/bash
#SBATCH --job-name=coupled_cavities_high_Q
#SBATCH --account=dengh0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=2
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=16g
#SBATCH --mail-type=FAIL


JOB_NUM=$((SLURM_ARRAY_TASK_ID))

python holey-wvg-cavity.py | tee holey-wvg-cavity.out
h5topng holey-wvg-cavity-eps-000000.00.h5
h5topng -Zc dkbluered holey-wvg-cavity-hz-slice.h5


python holey-wvg-cavity.py -N 0 | tee holey-wvg-cavity0.out
grep flux1: holey-wvg-cavity.out > flux.dat
grep flux1: holey-wvg-cavity0.out > flux0.dat
