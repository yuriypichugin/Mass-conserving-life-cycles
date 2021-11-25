#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:58:55 2020

@author: pichugin
"""

import numpy as np
import CM7 as CM
import sys

def RecordResults(File2Write, Parameters):
	
	String2Write = ""
	for elem in Parameters[:-1]:
		String2Write += str(elem) + ', '
	for offspring in Parameters[-1]:
		String2Write += str(offspring) + '; '
	String2Write += '\n'
	File2Write.write(String2Write)
	File2Write.flush()
	return 0

def MonteCarlo_Sampling(XParams, GParams, Loss, Parts, Repeats):
	"""
	Randomly sample life cycles, to get the best starting point for the gradient optimization
	Arguments:
		(list) XParams 	- parameters of the X set for calculation
		(list) GParams 	- parameters of the growth model
		(float) Loss 	 	- amount of biomass lost at the fragmentation
		(int) Parts 	 	- number of offspring groups in the reproduction
		(int) Repeats 	- how many random LCs to try
	Return:
		(list) LC 	 	- list of offspring sizes which deliver the maximal
							 growth rate
	"""
	
	""" initialize """
	[X,G,T] = CM.XGT_generate(XParams, GParams, 1)
	BestLC = Parts*[1.0]
	BestGR = CM.LambdaBisect(BestLC, Loss, X, G, T)
	
	""" test a number of random LCs """
	for i in np.arange(Repeats):
		TestLC = list(np.random.uniform(low = 1.0, high = 5.0, size = Parts))
		TestGR = CM.LambdaBisect(TestLC, Loss, X, G, T)
		""" record the better LC """
		if TestGR > BestGR:
			BestGR = TestGR
			BestLC = list(TestLC)
			
	return BestLC



MaxBenefit = float(sys.argv[1])
x0 = float(sys.argv[2])
Loss = float(sys.argv[3])

XParams = [1, 60, 0.01]
Perturbation = 0.02
NumofOffspring = 0
MaxOffspring = 15


#SigmaList = np.round(np.arange(0.1, 2.12, 0.02), decimals = 2)
SigmaList = np.round(np.arange(0.1, 5.10, 0.05), decimals = 2)
#LossList = np.round(np.arange(0.0, 5.1, 0.05), decimals = 2)
OffspringList = np.arange(2, MaxOffspring+1)

#""" debug """
#MaxBenefit = 1
#X0 = 5.0
#SigmaList = [1.0]
#LossList = [2.0]
#MaxBenefit = 1e-1
#x0=5.0

FileName = "Results/CostlyGaussian_MaxBenefit="+str(MaxBenefit)+'_x0='+str(x0)+'_Loss='+str(Loss)+".txt"
File2Write = open(FileName, "w")
String2Write = "MaxBenefit, x0, sigma, MassLoss, GrowthRate, OffspringNum, Symmetry, OffspringSet, dummy"+'\n'
File2Write.write(String2Write)

for sigma in SigmaList:
#	for Loss in LossList:
	GParams = [6, x0, sigma, MaxBenefit]
	
#	Result = len(OffspringList)*[[0,0,0]]
	Result = []
	
	for Offspring in OffspringList:		
		Repeats = 1000
		StartFRG = MonteCarlo_Sampling(XParams, GParams, Loss, Offspring, Repeats)
		Result.append(CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG))
#	StartFRG_3 = MonteCarlo_Sampling(XParams, GParams, Loss, 3, Repeats)
#	StartFRG_4 = MonteCarlo_Sampling(XParams, GParams, Loss, 4, Repeats)
#	StartFRG_5 = MonteCarlo_Sampling(XParams, GParams, Loss, 5, Repeats)
#	StartFRG_6 = MonteCarlo_Sampling(XParams, GParams, Loss, 6, Repeats)

#	Result[0] = CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG_2)
#	Result[1] = CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG_3)
#	Result[2] = CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG_4)
#	Result[3] = CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG_5)
#	Result[4] = CM.OptimizeGrowth_seeded(XParams, GParams, Loss, Perturbation, NumofOffspring, StartFRG_6)
	
	GrowthRatesSet = []
	for entry in Result:
		GrowthRatesSet.append(entry[2])
	GrowthRatesSet = np.asarray(GrowthRatesSet)
#	
#	GrowthRatesSet = np.asarray([Result[0][2],
#					Result[1][2],
#					Result[2][2],
#					Result[3][2],
#					Result[4][2],
#					])
	OptimalOffNum = GrowthRatesSet.argmax()
	
	
	m_min = min(Result[OptimalOffNum][1])
	m_max = max(Result[OptimalOffNum][1])
	Symmetry = (m_min-1.0)/((m_min+m_max)/2.0 - 1.0 + 1e-6)
	Symmetry = np.round(Symmetry, decimals = 4)
	
	Record = [MaxBenefit, x0, sigma, Loss, Result[OptimalOffNum][2], OptimalOffNum+2, Symmetry, np.round(Result[OptimalOffNum][1], decimals = 2)]
	
	RecordResults(File2Write, Record)

File2Write.close()
