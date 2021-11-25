# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Tue Aug 18

@author: Hyejin Park
"""


import numpy as np
import sys
def WriteFile(MB, X0, Loss, sigma):
	jobname = ("LC_%f_%f_%f_%f" %(MB, X0, Loss, sigma))
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
	fp.write("python CostlyGaussian_benefit.py %f %f %f %f\n" %(MB, X0, Loss, sigma))
	fp.close()



""" 4. write simulation codes """
ofp = open("run.sh", "w")
ofp.write("module load python/3.7.4 \n")

#MB = 1.0
X0 = 5.0
Loss = 1.0
LogBenefitList = np.arange(-1.0, 1.02, 0.02)
BenefitList = np.round(np.power(10.0, LogBenefitList), decimals = 3)
SigmaList = [0.5, 1.0, 3.0, 10.0]

for sigma in SigmaList:
	for MB in BenefitList:
		file = ( "script/CCM_Benefit=%f_sigma=%f.sh" % (MB, sigma))
		ofp.write("sbatch %s\n" % file )
		WriteFile(MB, X0, Loss, sigma)
ofp.close()
