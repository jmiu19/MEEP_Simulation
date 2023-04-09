#!/bin/bash
#SBATCH --job-name=coupled_cavities_chulwon
#SBATCH --account=dengh0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=2
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --mem-per-cpu=16g
#SBATCH --mail-type=FAIL
#SBATCH --time=120:00:00

JOB_NUM=$((SLURM_ARRAY_TASK_ID))

mpirun -np 2 python3 nanobeam.py -Lam_u $1 -Lam_s $2 -w $3> nanobeam_cavity_length$3.out;
line=$(grep harminv0: nanobeam_cavity_length$3.out |cut -d , -f2,4 |grep -v frequency);
echo "$1, $2, $3, $line" >> nanobeam_cavity_varylength.dat;
