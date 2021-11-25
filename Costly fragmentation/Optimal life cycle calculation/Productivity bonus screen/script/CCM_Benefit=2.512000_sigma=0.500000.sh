#!/bin/sh
#Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#SBATCH --time=2-00:00:00
#Set name of job shown in squeue
#Request CPU resources
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -o ./outputs/output.LC_2.512000_5.000000_1.000000_0.500000
#SBATCH -e ./errors/error.LC_2.512000_5.000000_1.000000_0.500000
python CostlyGaussian_benefit.py 2.512000 5.000000 1.000000 0.500000
