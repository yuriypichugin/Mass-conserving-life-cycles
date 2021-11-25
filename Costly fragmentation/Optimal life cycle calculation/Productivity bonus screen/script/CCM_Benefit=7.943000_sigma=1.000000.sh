#!/bin/sh
#Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#SBATCH --time=2-00:00:00
#Set name of job shown in squeue
#Request CPU resources
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -o ./outputs/output.LC_7.943000_5.000000_1.000000_1.000000
#SBATCH -e ./errors/error.LC_7.943000_5.000000_1.000000_1.000000
python CostlyGaussian_benefit.py 7.943000 5.000000 1.000000 1.000000
