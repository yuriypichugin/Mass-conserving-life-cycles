#!/bin/sh
#Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#SBATCH --time=1-00:00:00
#Set name of job shown in squeue
#Request CPU resources
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -o ./outputs/output.LC_1.000000_5.000000_0.950000
#SBATCH -e ./errors/error.LC_1.000000_5.000000_0.950000
python CostlyGaussian_loss_sigma_v3.py 1.000000 5.000000 0.950000
