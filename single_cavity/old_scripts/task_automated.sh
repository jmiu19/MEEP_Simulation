#!/bin/bash
#SBATCH --job-name=single_cavity
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=12g
#SBATCH --time=24:00:00

JOB_NUM=$((SLURM_ARRAY_TASK_ID))

mpirun python3 nanobeam.py -Res $1 -Lam_u $2 -Lam_s $3 -Nwvg $4> nanobeam_cavity_Nwvg$4.out;
line=$(grep harminv0: nanobeam_cavity_Nwvg$4.out |cut -d , -f2,3,4 |grep -v frequency);
echo "$4, $line" >> nanobeam_cavity_varylength.dat;
