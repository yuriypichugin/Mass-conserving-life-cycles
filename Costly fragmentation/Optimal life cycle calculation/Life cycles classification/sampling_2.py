# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Tue Aug 18

@author: Hyejin Park
"""


import numpy as np
import sys
def WriteFile(MB, X0, Loss):
	jobname = ("LC_%f_%f_%f" %(MB, X0, Loss))
	fp = open(file, "w")
	fp.write("#!/bin/sh\n")
	fp.write("#Set your minimum acceptable walltime, format: day-hours:minutes:seconds\n")
	fp.write("#SBATCH --time=2-00:00:00\n")
	fp.write("#Set name of job shown in squeue\n")
	fp.write("#Request CPU resources\n")
	fp.write("#SBATCH --ntasks=1\n")
	fp.write("#SBATCH --ntasks-per-node=1\n")
	fp.write("#SBATCH --cpus-per-task=1\n")
	fp.write("#SBATCH -o ./outputs/output.%s\n" %jobname)
	fp.write("#SBATCH -e ./errors/error.%s\n" %jobname)
	fp.write("python CostlyGaussian_loss_sigma_v4.py %f %f %f\n" %(MB, X0, Loss))
	fp.close()



""" 4. write simulation codes """
ofp = open("run.sh", "w")
ofp.write("module load python/3.7.4 \n")

MB = 1.0
X0 = 5.0
LossList = np.round(np.arange(0.0, 3.01, 0.05), decimals = 2)

for Loss in LossList:
	file = ( "script/CCM_Loss=%f.sh" % Loss)
	ofp.write("sbatch %s\n" % file )
	WriteFile(MB, X0, Loss)
ofp.close()
