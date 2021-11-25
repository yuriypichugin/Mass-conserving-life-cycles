#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:28:55 2018

@author: pichugin
"""

import numpy as np
import CM6 as CM6
import sys
#import matplotlib.pyplot as plt

#def OptimizeGrowth(XParams, GParams, Loss, Perturbation, NumofOffspring):
#	"""
#	Find the optimal fragmentaiton mode for given environment
#	Arguments:
#		(list) XParams - the set of parameters to generate X-array
#		(list) GParams - the set of parameters to generate G-array
#		(float) Loss - the amount of biomass, lost at the fragmentation
#		(float) Perturbation - the change in the offspring size (should be greater than the step in X)
#		(int) NumofOffspring - the number of offspring (at Loss = 0, this should be 2)
#	Return:
#		(list) Output
#			Output[0] - the optimal number of offspring
#			Output[1] - the optimal life cycle, list of the offspring sizes
#			Output[2] - the maximal population growth rate
#	"""
#
##	Perturbation = 0.2
#	
#	[X,G,T] = CM5.XGT_generate(XParams, GParams, 1)
#
#	""" grid optimization of life cycle """
#	BLArray=[]
#	BFRGArray=[]
#	""" initialize life cycle """
##	bestFRG = max(GParams[1], 1.1) * np.ones(2)
#	bestFRG = 3 * np.ones(NumofOffspring)
#	bestLambda = CM5.LambdaBisect(bestFRG, Loss, X, G, T)
#	
#	""" while better neighbours on the grid are being found, continue optimization"""
#	TheBestFound = 0
#	while TheBestFound == 0:
#		CurrentBestFRG = np.array(bestFRG)
#		CurrentBestLambda = bestLambda
#		TheBestFound = 1
#		""" for each of the offspring group """
#		for index in np.arange(len(bestFRG)):
#			""" test slightly larger offspring """
#			testFRG = np.array(bestFRG)
#			testFRG[index] += Perturbation
#			testLambda = CM5.LambdaBisect(testFRG, Loss, X, G, T)
#			if testLambda > CurrentBestLambda:
#				CurrentBestFRG = np.array(testFRG)
#				CurrentBestLambda = testLambda
#				TheBestFound=0
#			
#			""" test slightly smaller offspring """
#			testFRG = np.array(bestFRG)
#			testFRG[index] -= Perturbation
#			if testFRG[index] > 1:
#				testLambda = CM5.LambdaBisect(testFRG, Loss, X, G, T)
#				if testLambda > CurrentBestLambda:
#					CurrentBestFRG = np.array(testFRG)
#					CurrentBestLambda = testLambda
#					TheBestFound=0
#		bestFRG = np.array(CurrentBestFRG)
#		bestLambda = np.array(CurrentBestLambda)
#	""" remember the best life cycle for each given fragments number """				
#	BLArray.append(bestLambda)
#	BFRGArray.append(bestFRG)
#	
#	""" optimize over fragments number """
#	""" !! Probably, unnecessary !!"""
#	BestOffNum = np.argmax(BLArray)
#	TotalBestLC = BFRGArray[BestOffNum]
#	TotalBestLambda = BLArray[BestOffNum]
#	return [BestOffNum+2, TotalBestLC, TotalBestLambda]

def Generate_random_bisect(Params):
	"""
	The random 2-D bisection for monotonic random sequencies
	Arguments:
		(float) Params[0] - X-coordinates of the first [0][0] and the last [0][1] points
		(float) Params[1] - Y-coordinates of the first [1][0] and the last [1][1] points
		(int)   Params[2] - How many levels of bisection to do
	Return:
		(list of lists of floats) - the list of nodes [X, Y]
		
	"""
	XF=Params[0][0]
	XL=Params[0][1]
	YF=Params[1][0]
	YL=Params[1][1]
	
#	Ylast = Params[0]
	Depth = Params[2]
	""" initialize node list """
	X = [XF, XL]
	Y = [YF, YL]
	
	for i in np.arange(Depth):
		X_new = []
		Y_new = []
		for k in np.arange(len(X)-1):
			X_new.append(X[k])
			Y_new.append(Y[k])
			
			x_bisect = np.random.uniform(X[k], X[k+1])
			y_bisect = np.random.uniform(Y[k+1], Y[k])
			
			X_new.append(x_bisect)
			Y_new.append(y_bisect)

		X_new.append(X[-1])
		Y_new.append(Y[-1])
		
		X = X_new
		Y = Y_new
	return [X, Y]



""" --- main --- """

JobID = int(sys.argv[1]) 


XParams = [1, 50, 0.1]

Depth = 8

Repeats = 10000

List2write=[]

for i in np.arange(Repeats):

	Xparams = [1, 20]
	Yparams = [1, 10]
	IncreasePart = Generate_random_bisect([ Xparams, Yparams, Depth ])
	
	Xparams = [20, 21]
	Yparams = [10, 0]
	DecreasePart = Generate_random_bisect([ Xparams, Yparams, Depth ])
	
	X_list = IncreasePart[0] + DecreasePart[0] + [XParams[1]]
	Y_list = IncreasePart[1] + DecreasePart[1] + [0]
	
	Gparams = [19, X_list, Y_list]
	Loss = 0
	Perturbation = 0.2
	NumofOffspring =  2
	Result = CM6.OptimizeGrowth(XParams, Gparams, Loss, Perturbation, NumofOffspring)

	List2write.append([float(Result[0])] + list(Result[1]) + [float(Result[2])] + [len(Gparams[1])] + Gparams[1]+ Gparams[2])


"""
The format of file:
	List2write[i][:] - a single calculation
	List2write[:][0] - number of offspring (A)
	List2write[:][1:A+1] - offspring sizes
	List2write[:][A+1] - population growth rate
	List2write[:][A+2] - size of X, Y sequencies (B)
	List2write[:][A+3 : A+B+3] -  X sequence
	List2write[:][A+B+3 : A+2B+3] -  Y sequence
"""
np.savetxt("RosettesLC"+str(JobID)+".txt", List2write, delimiter=",")



#plt.plot(X_list[0:-1], Y_list[0:-1])

#
#
##""" test """
##GParams = [15, 10, [5, 5], 2, 2]
##[X,G,T] = CM5.XGT_generate(XParams, GParams, 1)
##plt.plot(X, G/X)
#
#
#ke = 1
#k0 = 1
#
#
#LogListSubstrate = np.linspace(-4, 2, 10)
#ListSubstrate = np.power(10, LogListSubstrate)
##ListWidth2 = np.linspace(0.2, 1.5, 1)
#
##ListLoc = np.linspace(0, 10.0, 59)
##LogListPower = np.linspace(-1.0, 1.0, 61)
##ListPower = np.power(10, LogListPower)
#
#GrowthRates = np.zeros(len(ListSubstrate))
#AsymmetriesLow = np.zeros(len(ListSubstrate))
#AsymmetriesHigh = np.zeros(len(ListSubstrate))
#OffspringNumbers = np.zeros(len(ListSubstrate))
#CombinedOffSize = np.zeros(len(ListSubstrate))
#SmallerOffs = np.zeros(len(ListSubstrate))
#LargerOffs = np.zeros(len(ListSubstrate))
#
#
#for U in ListSubstrate:
#	U_location = abs(ListSubstrate-U).argmin()
#	print(U_location)
##	print(Loss)
##	for Width2 in ListWidth2:
##	Width2_location = abs(ListWidth2-Width2).argmin()
#	GParams = [16, ke, k0, U]
#	Results = CM6.OptimizeGrowth(XParams, GParams, 0)
#	""" logged parameters """
#	OffspringNumbers[U_location] = Results[0]
#	
#	SmallOff = min(Results[1])
#	LargeOff = max(Results[1])
#	SmallerOffs[U_location] = SmallOff
#	LargerOffs[U_location] = LargeOff
#	AverageOff = sum(Results[1])/Results[0]
#	AsymmetriesLow[U_location] = (AverageOff - SmallOff)/(AverageOff - 1.0)
#	AsymmetriesHigh[U_location] = (LargeOff - AverageOff)/(AverageOff - 1.0)/(Results[0] - 1)
#	CombinedOffSize[U_location] = sum(Results[1])
#	
#	GrowthRates[U_location] = Results[2]
#
#""" write data to file """
#np.savetxt("SubstrateList.dat", ListSubstrate, delimiter=",")
##np.savetxt("Width2List.dat", ListWidth2, delimiter=",")
##np.savetxt("LocationList_width="+str(width)+".dat", ListLoc, delimiter=",")
#
##np.savetxt("ParentSizesMap.dat", ParentSizes, delimiter=",")
##np.savetxt("OffspringNumbersMap_x0_"+str(x_0)+".dat", OffspringNumbers, delimiter=",")
#np.savetxt("SmallOffspringMap_sph_ke="+str(ke)+".dat", SmallerOffs, delimiter=",")
#np.savetxt("LargeOffspringMap_sph_ke="+str(ke)+".dat", LargerOffs, delimiter=",")
#np.savetxt("GrowthRatesMap_sph_ke="+str(ke)+".dat", GrowthRates, delimiter=",")
#np.savetxt("AsymmetriesLowMap_sph_ke="+str(ke)+".dat", AsymmetriesLow, delimiter=",")
#np.savetxt("AsymmetriesHighMap_sph_ke="+str(ke)+".dat", AsymmetriesHigh, delimiter=",")
#np.savetxt("CombinedOffspringSize_sph_ke="+str(ke)+".dat", CombinedOffSize, delimiter=",")
