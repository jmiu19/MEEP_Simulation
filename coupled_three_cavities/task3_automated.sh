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

mpirun -np 2 python3 nanobeam.py -params $1 > output/OUTPUT$1.out;
line=$(grep harminv0: output/OUTPUT$1.out |cut -d , -f2-4 |grep -v frequency);
echo "$1, $line" >> output/cavity_resonances.dat;
grep flux1: output/OUTPUT$1.out > output/FLUX$1.dat;
mpirun -np 2 python3 flux_plot.py $1;

