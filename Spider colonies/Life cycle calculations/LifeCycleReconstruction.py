#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:01:02 2019

@author: pichugin
"""

import numpy as np
from copy import deepcopy as deepcopy
#import matplotlib.pyplot as plt
import CM6_1_2 as CM
import sys

def CreateFreeformProfile(N_points):
	"""
	Function creating a random freeform profile
	"""
	
	log10Xmax = 4

	log10Xlist = np.zeros(N_points+2)
	log10Xlist[-1] = log10Xmax
	log10Xlist[1:(N_points+1)] = np.sort(np.random.uniform(low = 0.0, high = log10Xmax, size = N_points))
	Xlist = np.power(10, log10Xlist)
	
	
	Ylist = np.zeros(N_points+2)
	Ylist[0:(N_points+1)] = np.random.uniform(0,1,size = N_points+1)
	Ylist[-1] = 1e-6
	
	Output = np.asarray([Xlist, Ylist])
	
	return Output

def PerturbateFreeformProfile(Xlist, Prod_list, var_log10X, var_log10Prod):
	
	logProdlist = np.log10(Prod_list)
	New_logProdlist = logProdlist + np.random.normal(loc = 0.0, scale = var_log10Prod, size = len(Prod_list))
	New_Prod_list = np.power(10.0, New_logProdlist)
	
	logXlist = np.log10(Xlist)
	New_logXlist = np.zeros(len(logXlist))
	New_logXlist[0] = logXlist[0]
	New_logXlist[-1] = logXlist[-1]
	New_logXlist[1:-1] = logXlist[1:-1] + np.random.normal(loc = 0.0, scale = var_log10X, size = len(Xlist)-2) 

	""" reset log10X went over the borders """
	for elem in np.arange(len(New_logXlist)):
		if (New_logXlist[elem] < logXlist[0]):
			New_logXlist[elem] = np.random.uniform(low = logXlist[0], high = logXlist[-1])
		if (New_logXlist[elem] > logXlist[-1]):
			New_logXlist[elem] = np.random.uniform(low = logXlist[0], high = logXlist[-1])
	
	New_Xlist = np.power(10.0, New_logXlist)
	Output = np.asarray([New_Xlist, New_Prod_list])
	
	Output_sorted = Output [:, Output[0].argsort()]
	
	return Output_sorted

#def PerturbateFreeformProfile(Xlist, Prod_list, var_log10X, var_Prod):
#	
#	New_Prod_list = Prod_list* np.abs( np.random.normal(loc = 1.0, scale = var_Prod, size = len(Prod_list)) )
#	
#	New_Xlist = np.zeros(len(Xlist))
##	New_Xlist[1:-1] = Xlist[1:-1] + np.random.normal(loc = 0.0, scale = var_log10X, size = len(Xlist)-2)
#	New_Xlist[1:-1] = Xlist[1:-1] * np.abs( np.random.normal(loc = 1.0, scale = var_log10X, size = len(Xlist)-2) )
#	New_Xlist[-1] = Xlist[-1]
#	
#	""" wrap the log10X values around the borders """
#	for elem in np.arange(len(New_Xlist)):
#		if New_Xlist[elem] < 0:
#			New_Xlist[elem] = Xlist[-1] + New_Xlist[elem]
#		if New_Xlist[elem] > Xlist[-1]:
#			New_Xlist[elem] = New_Xlist[elem] - Xlist[-1]
#	
#	
#	Output = np.asarray([New_Xlist, New_Prod_list])
#	
#	Output_sorted = Output [ :, Output[0].argsort()]
#	
#	return Output_sorted	


def CompareDistributions(XParams, Xlist, ProductivityList, XBorders, DataFreqs):
	"""
	Compute the deviation between distribution of colony sizes in a tested and 
	experimentally observed populations
	
	Arguments:
		(list) XParams - the set of parameters to generate X-array
		(list) Xlist - the list of x-values of nodes at which the productivity is defined
		(list) ProductivityList - the list of productivities at these nodes
		(list) XBorders - the set of coarse grains, each class contain groups of size
						between lower border (excluded) and upper border (included).
		(list) DataFreqs - the set of frequencies of groups of given class observed in nature
	Return:
		(float) Deviation - the discrepancy between two sets
		(list) Freqs2Test - the coarse grained distribution of given LC
		(list) BestLifeCycle - the evolutionary optimal fragmentation mode
		(list) TrueFreqs - actual distribution of given LC

	"""
	
	
	GParams = [23, Xlist, ProductivityList]
	
	""" optimize life cycle """
	PreResult = CM.OptimizeGrowth_seeded(XParams, GParams, 0, 100.0, 2, [2000,1])
	PreResult = CM.OptimizeGrowth_seeded(XParams, GParams, 0, 10.0, 2, PreResult[1])
	Result = CM.OptimizeGrowth_seeded(XParams, GParams, 0, 1.0, 2, PreResult[1])
	BestLifeCycle = Result[1]
	BestGRate = Result[2]
	
	
	""" find true group size distribution """
	[X, G, T] = CM.XGT_generate(XParams, GParams, 1)
	TrueFreqs = np.zeros(len(X))
	
	IndParent = sum(X < sum(BestLifeCycle))
	for Offspring in BestLifeCycle:
		IndOff = sum(X < Offspring)
		GOff = G[IndOff]
		ind = sum(X < Offspring)
		while ind < IndParent:
			TrueFreqs[ind] += GOff / G[ind] * np.exp( - BestGRate * (T[ind] - T[IndOff]))
			ind+=1
	
	""" coarse grain to compare with the data """	
	IndsBorders = np.zeros(len(XBorders))
	Freqs2Test = np.zeros(len(XBorders))
	for i in np.arange(len(XBorders)):
		IndsBorders[i] = sum(X < XBorders[i])
	IndsBorders = np.append(0, IndsBorders)
	for i in np.arange(len(XBorders)):
		Ind1=int(IndsBorders[i])
		Ind2 = int(IndsBorders[i+1])+1
		Freqs2Test[i] = sum(TrueFreqs[Ind1:Ind2])
	Freqs2Test = Freqs2Test/sum(Freqs2Test)
	
	""" find a deviation """
	Deviation = sum(np.power(Freqs2Test-DataFreqs,2))	
	return([Deviation, Freqs2Test, BestLifeCycle, TrueFreqs])

def FitWProfile(XParams, X0, XBorders, DataFreqs, N_points):
	"""
	Calculates the growth rate profile vs ecDNA copynumbers, which corresponds the best to the 
	given copynumber distribution.
	
	Arguments:
		(np.vector) EV_base - the distribution to fit, where the first element 
							corresponds to the fraction of 1-copy cells as
							0-copy cells are invisible.
	"""
	
	SeedFreeform = CreateFreeformProfile(N_points)
	Xlist = SeedFreeform[0]
	ProductivityList = SeedFreeform[1]
	
	[Err_best, Freqs2Test, BestLC, TrueFreqs_Best] = CompareDistributions(XParams, Xlist, ProductivityList, XBorders, DataFreqs)
	print(Err_best)
	""" criteria to stop fitting either by high accuracy of found solution, or 
	by low scale of annealing perturbations """
	Err_accept = 0.00
	Scale_accept = 0.01
	DevScale = 1.0
	Accepts = 0.0
	Rejects = 0.0

	
	""" optimization """
	while (Err_best > Err_accept)and(DevScale > Scale_accept):
		
		TestFreeform = PerturbateFreeformProfile(Xlist, ProductivityList, DevScale, DevScale)
		[Err_test, Freqs2Test, TestLC, TrueFreqs_Test] = CompareDistributions(XParams, TestFreeform[0], TestFreeform[1], XBorders, DataFreqs)
#		print("try: ", Err_test)
		if Err_test < Err_best:
			Accepts += 1.0
			Err_best = Err_test
			Xlist = deepcopy(TestFreeform[0])
			ProductivityList = deepcopy(TestFreeform[1])
			BestLC = deepcopy(TestLC)
			print(Err_best)

		else:
			Rejects += 1.0
		if Accepts+Rejects>30:
			if (Accepts/(Accepts+Rejects) < 0.1):
				DevScale = DevScale*0.75
				
			Accepts=0.0
			Rejects=0.0
	
	Output = np.zeros(2*len(Xlist)+3)
	Output[0:len(Xlist)] = deepcopy(Xlist)
	Output[len(Xlist):(2*len(Xlist))] = deepcopy(ProductivityList)
	Output[2*len(Xlist)] = min(BestLC)
	Output[2*len(Xlist)+1] = max(BestLC)
	Output[2*len(Xlist)+2] = Err_best
	
	return Output



JobID = int(sys.argv[1]) 
#JobID = 0

""" Data read """
Data = np.loadtxt("SpiderData.txt", delimiter=",", skiprows=1)
XBorders = np.asarray([1, 9, 49, 149, 499, 999, 1999, 10000])
X0 = np.asarray([1, 5, 30, 100, 275, 750, 1500, 2500, 7000])
dX0 = np.asarray([1, 8, 40, 100, 350, 500, 1000, 2000, 6000])
DataFreqs = Data[:,2]/sum(Data[:,2])
DataProds = Data[:,3]/sum(Data[:,3])

""" calc parameters initialization """
XParams = [1, 10000, 0.5]

N_points = 5

""" data set to save """
Repeats = 10
Data2Save = np.zeros((Repeats, 2*(N_points+2)+3))


#TEST = CreateFreeformProfile()
#TEST2 = PerturbateFreeformProfile(TEST[0], TEST[1], 1, 0.0)
#
#print(TEST)
#print(TEST2)

for run in np.arange(Repeats):
	print(run)
	
	""" calculation """
	Result = FitWProfile(XParams, X0, XBorders, DataFreqs, N_points)
	
	Data2Save[run,:] = Result

	np.savetxt("Results/FittedWProfiles_power_law"+str(JobID)+".csv", Data2Save, delimiter=', ')

