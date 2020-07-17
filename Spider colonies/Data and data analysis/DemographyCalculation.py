#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:08:39 2019

@author: pichugin
"""

import numpy as np
import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt
#from copy import deepcopy as deepcopy
#from sklearn.decomposition import PCA
#from scipy.interpolate import interp1d
import CM6_1_2 as CM



def ColumnNamesUnification(Data, Pars):
	""" 
	Unify the similar column names across different datasets
	Data - dataset to process
	Pars[0] - LengthXX - the lenght of productivity profile
	"""
	LengthXX = Pars[0]
	BaseNameSmallOffspring = 'V'+str(2*LengthXX+1)
	BaseNameLargeOffspring = 'V'+str(2*LengthXX+2)
	BaseNameError = 'V'+str(2*LengthXX+3)
	Data = Data.rename(columns = {BaseNameSmallOffspring : "Small_off",
							   BaseNameLargeOffspring : "Large_off",
							   BaseNameError : "Error"})

	return Data

def DataClean(Data, Pars):
	"""
	Clean the data
	"""
	Cutoff = Pars[0]
	Data = Data[Data['Error']>0]
	Data = Data[Data['Error']< Cutoff]
	Data = Data.reset_index(drop=True)
	
	return Data

def FindDemography(XParams, log10Xlist, ProductivityList, XBorders, BestLifeCycle):
	
	""" find true group size distribution """
	GParams = [23, log10Xlist, ProductivityList]
	[X, G, T] = CM.XGT_generate(XParams, GParams, 1)
	BestGRate = CM.LambdaBisect(BestLifeCycle, 0, X, G, T)
	
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
	
	return Freqs2Test

""" setup """

#sns.set()

ErrorCutoff = 0.025

""" set up files options """

ModelIndex = 4
if ModelIndex == 1:
	FileName = "Spiders_5_1_linear_5points"
	Flag_Log_X = 0
	Flag_Log_Y = 0
elif ModelIndex == 2:
	FileName = "Spiders_5_2_exponential_5points"
	Flag_Log_X = 0
	Flag_Log_Y = 1
elif ModelIndex == 3:
	FileName = "Spiders_5_3_logarithmic_5points"
	Flag_Log_X = 1
	Flag_Log_Y = 0
elif ModelIndex == 4:
	FileName = "Spiders_5_4_power_law_5points"
	Flag_Log_X = 1
	Flag_Log_Y = 1

#FileName_02 = "Spiders_5_2_exponential_5points"
#FileName_03 = "Spiders_5_3_logarithmic_5points"
#FileName_04 = "Spiders_5_4_power_law_5points"

#Length03 = 5
Length05 = 7
#Length10 = 12


""" choose the focal data set """

FileName_focal = FileName
Length_focal = Length05


#""" set up files options """
#
#FileName10 = "Spiders_4c_10points"
#FileName05 = "Spiders_4b_5points"
#FileName03 = "Spiders_4a_3points"
#
#Length03 = 5
#Length05 = 7
#Length10 = 12
#
#
#""" choose the focal data set """
#
#FileName_focal = FileName05
#Length_focal = Length05

""" read and prepare data """

SpData = pd.read_csv(FileName_focal+'.txt')
SpData = ColumnNamesUnification(SpData, [Length_focal])
SpData = DataClean(SpData, [ErrorCutoff])

""" Data read """
ExprData = np.loadtxt("SpiderData.txt", delimiter=",", skiprows=1)
XBorders = np.asarray([1, 9, 49, 149, 499, 999, 1999, 10000])
X0 = np.asarray([1, 5, 30, 100, 275, 750, 1500, 2500, 7000])
dX0 = np.asarray([1, 8, 40, 100, 350, 500, 1000, 2000, 6000])
ExprDataFreqs = ExprData[:,2]/sum(ExprData[:,2])
ExprDataProds = ExprData[:,3]/sum(ExprData[:,3])

XParams = [1, 10000, 0.5]


OutputDemographics = np.zeros((len(SpData), len(ExprDataFreqs)))

for SubDataInd in np.arange(len(SpData)):
#for SubDataInd in np.arange(2):
	print(SubDataInd)
	log10Xlist = np.asarray(SpData.iloc[SubDataInd, 0:Length_focal])
	ProductivityList = np.asarray(SpData.iloc[SubDataInd, Length_focal:(2*Length_focal)])
	BestLifeCycle = np.asarray(SpData.iloc[SubDataInd, (2*Length_focal):(2*Length_focal+2)])
	
	FitFreqs = FindDemography(XParams, log10Xlist, ProductivityList, XBorders, BestLifeCycle)
	OutputDemographics[SubDataInd, :] = FitFreqs

np.savetxt('Demography_'+str(Length_focal-2)+'_points_s500.txt', OutputDemographics, delimiter = ',')

#plt.plot(ExprDataFreqs)
#plt.plot(OutputDemographics)
#plt.show()
