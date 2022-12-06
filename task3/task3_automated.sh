#!/bin/bash
#SBATCH --job-name=task3
#SBATCH --mem-per-cpu=8g
#SBATCH --account=dengh0
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --array=1
#SBATCH --mail-type=FAIL

for scav in `seq 0.110 0.005 0.180`; do
    mpirun -np 2 python3 nanobeam.py -s_cav ${scav} > nanobeam_cavity_length${scav}.out;
    grep harminv0: nanobeam_cavity_length${scav}.out |cut -d , -f2,4 |grep -v frequency >> nanobeam_cavity_varylength.dat;
done;
