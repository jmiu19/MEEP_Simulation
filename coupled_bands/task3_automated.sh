#!/bin/bash
#SBATCH --job-name=task3
#SBATCH --mem-per-cpu=32g
#SBATCH --account=dengh0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --array=1
#SBATCH --mail-type=FAIL

JOB_NUM=$((SLURM_ARRAY_TASK_ID))

mpirun -np 2 python3 nanobeam.py -Lam_u $1 -Lam_s $2 > nanobeam_cavity_length$1.out;
line=$(grep harminv0: nanobeam_cavity_length$1.out |cut -d , -f2,4 |grep -v frequency);
echo "$1, $2, $line" >> nanobeam_cavity_varylength.dat;
