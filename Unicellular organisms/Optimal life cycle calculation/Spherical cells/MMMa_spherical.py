#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:28:55 2018

@author: pichugin
"""

import numpy as np
import CM5_3_1 as CM5
#import sys
#import matplotlib.pyplot as plt

def OptimizeGrowth(XParams, GParams, Loss):
	"""
	Find the optimal fragmentaiton mode for given environment
	"""

	Perturbation = 0.2
	
	[X,G,T] = CM5.XGT_generate(XParams, GParams, 1)

	""" grid optimization of life cycle """
	BLArray=[]
	BFRGArray=[]
	""" initialize life cycle """
#	bestFRG = max(GParams[1], 1.1) * np.ones(2)
	bestFRG = 3 * np.ones(2)
	bestLambda = CM5.LambdaBisect(bestFRG, Loss, X, G, T)
	
	""" while better neighbours on the grid are being found, continue optimization"""
	TheBestFound = 0
	while TheBestFound == 0:
		CurrentBestFRG = np.array(bestFRG)
		CurrentBestLambda = bestLambda
		TheBestFound = 1
		""" for each of the offspring group """
		for index in np.arange(len(bestFRG)):
			""" test slightly larger offspring """
			testFRG = np.array(bestFRG)
			testFRG[index] += Perturbation
			testLambda = CM5.LambdaBisect(testFRG, Loss, X, G, T)
			if testLambda > CurrentBestLambda:
				CurrentBestFRG = np.array(testFRG)
				CurrentBestLambda = testLambda
				TheBestFound=0
			
			""" test slightly smaller offspring """
			testFRG = np.array(bestFRG)
			testFRG[index] -= Perturbation
			if testFRG[index] > 1:
				testLambda = CM5.LambdaBisect(testFRG, Loss, X, G, T)
				if testLambda > CurrentBestLambda:
					CurrentBestFRG = np.array(testFRG)
					CurrentBestLambda = testLambda
					TheBestFound=0
		bestFRG = np.array(CurrentBestFRG)
		bestLambda = np.array(CurrentBestLambda)
	""" remember the best life cycle for each given fragments number """				
	BLArray.append(bestLambda)
	BFRGArray.append(bestFRG)
	
	""" optimize over fragments number """
	BestOffNum = np.argmax(BLArray)
	TotalBestLC = BFRGArray[BestOffNum]
	TotalBestLambda = BLArray[BestOffNum]
	return [BestOffNum+2, TotalBestLC, TotalBestLambda]

""" --- main --- """
XParams = [1, 1000, 0.1]

#""" test """
#GParams = [15, 10, [5, 5], 2, 2]
#[X,G,T] = CM5.XGT_generate(XParams, GParams, 1)
#plt.plot(X, G/X)


ke = 1
k0 = 1


LogListSubstrate = np.linspace(-4, 3, 100)
ListSubstrate = np.power(10, LogListSubstrate)
#ListWidth2 = np.linspace(0.2, 1.5, 1)

#ListLoc = np.linspace(0, 10.0, 59)
#LogListPower = np.linspace(-1.0, 1.0, 61)
#ListPower = np.power(10, LogListPower)

GrowthRates = np.zeros(len(ListSubstrate))
AsymmetriesLow = np.zeros(len(ListSubstrate))
AsymmetriesHigh = np.zeros(len(ListSubstrate))
OffspringNumbers = np.zeros(len(ListSubstrate))
CombinedOffSize = np.zeros(len(ListSubstrate))
SmallerOffs = np.zeros(len(ListSubstrate))
LargerOffs = np.zeros(len(ListSubstrate))


for U in ListSubstrate:
	U_location = abs(ListSubstrate-U).argmin()
	print(U_location)
#	print(Loss)
#	for Width2 in ListWidth2:
#	Width2_location = abs(ListWidth2-Width2).argmin()
	GParams = [16, ke, k0, U]
	Results = OptimizeGrowth(XParams, GParams, 0)
	""" logged parameters """
	OffspringNumbers[U_location] = Results[0]
	
	SmallOff = min(Results[1])
	LargeOff = max(Results[1])
	SmallerOffs[U_location] = SmallOff
	LargerOffs[U_location] = LargeOff
	AverageOff = sum(Results[1])/Results[0]
	AsymmetriesLow[U_location] = (AverageOff - SmallOff)/(AverageOff - 1.0)
	AsymmetriesHigh[U_location] = (LargeOff - AverageOff)/(AverageOff - 1.0)/(Results[0] - 1)
	CombinedOffSize[U_location] = sum(Results[1])
	
	GrowthRates[U_location] = Results[2]

""" write data to file """
np.savetxt("SubstrateList.dat", ListSubstrate, delimiter=",")
#np.savetxt("Width2List.dat", ListWidth2, delimiter=",")
#np.savetxt("LocationList_width="+str(width)+".dat", ListLoc, delimiter=",")

#np.savetxt("ParentSizesMap.dat", ParentSizes, delimiter=",")
#np.savetxt("OffspringNumbersMap_x0_"+str(x_0)+".dat", OffspringNumbers, delimiter=",")
np.savetxt("SmallOffspringMap_sph_ke="+str(ke)+".dat", SmallerOffs, delimiter=",")
np.savetxt("LargeOffspringMap_sph_ke="+str(ke)+".dat", LargerOffs, delimiter=",")
np.savetxt("GrowthRatesMap_sph_ke="+str(ke)+".dat", GrowthRates, delimiter=",")
np.savetxt("AsymmetriesLowMap_sph_ke="+str(ke)+".dat", AsymmetriesLow, delimiter=",")
np.savetxt("AsymmetriesHighMap_sph_ke="+str(ke)+".dat", AsymmetriesHigh, delimiter=",")
np.savetxt("CombinedOffspringSize_sph_ke="+str(ke)+".dat", CombinedOffSize, delimiter=",")
