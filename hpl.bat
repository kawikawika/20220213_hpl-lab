#!/bin/bash
#SBATCH -N 1
#SBATCH -p hpl
#SBATCH --ntasks-per-node=128
#SBATCH --exclusive
#SBATCH -t 0:30:00
#SBATCH -o slurm-output.log

cd $SLURM_SUBMIT_DIR

export OMP_NUM_THREADS=1
export OMP_PLACES=cores
export OMP_PROC_BIND=close

python xhpl.py | tee hpl.out
