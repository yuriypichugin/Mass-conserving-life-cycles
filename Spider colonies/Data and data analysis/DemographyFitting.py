#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:08:39 2019

@author: pichugin
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy as deepcopy
from sklearn.decomposition import PCA
from scipy.interpolate import interp1d
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



""" setup """

sns.set()

ErrorCutoff = 0.025

Write2File = 1

""" set up files options """

FileName10 = "Spiders_4c_10points"
FileName05 = "Spiders_4b_5points"
FileName03 = "Spiders_4a_3points"

Length03 = 5
Length05 = 7
Length10 = 12

DemographyFile05 = 'Demography_5_points_s500.txt'

""" choose the focal data set """

FileName_focal = "Spiders_5_4_power_law_5points"
Length_focal = Length05
DemFile = DemographyFile05

""" read and prepare simulations data """

SpData = pd.read_csv(FileName_focal+'.txt')
SpData = ColumnNamesUnification(SpData, [Length_focal])
SpData = DataClean(SpData, [ErrorCutoff])

Demography = np.loadtxt(DemFile, delimiter = ',')
Demography = Demography[0:500,:]
Demography = pd.DataFrame(Demography)

""" read experimental data """
ExprData = np.loadtxt("SpiderData.txt", delimiter=",", skiprows=1)
XBorders = np.asarray([1, 9, 49, 149, 499, 999, 1999, 10000])
X0 = np.asarray([1, 5, 30, 100, 275, 750, 1500, 2500, 7000])
dX0 = np.asarray([1, 8, 40, 100, 350, 500, 1000, 2000, 6000])
ExprDataFreqs = ExprData[:,2]/sum(ExprData[:,2])
ExprDataProds = ExprData[:,3]/sum(ExprData[:,3])

""" plot the figure """
LabelsFontSize = 20
TicksFontSize = 12
CLR_50 = '#2ca25f'

XTicksLabels = ['1', '2 - 9', '10 - 49', '50 - 149', '150 - 499', '500 - 999', '1000 - 1999', '> 2000']

plt.style.use('default')
fig, ax = plt.subplots(1,1)

LWD = 2
boxprops = dict(linewidth=LWD, color = 'dimgrey')
medianprops = dict(linewidth=LWD, color = CLR_50)
whiskerprops = dict(linewidth=LWD, color = 'dimgrey')
capprops = dict(linewidth=LWD, color = 'dimgrey')
plt.boxplot(np.transpose(Demography), whis = 'range', boxprops=boxprops, medianprops=medianprops, whiskerprops = whiskerprops, capprops = capprops)

plt.plot(np.arange(1,9),ExprDataFreqs, 'ok', markersize = 10)

ax.set_aspect(1.0/ax.get_data_ratio())

plt.xticks(np.arange(1,9), XTicksLabels, rotation = 45, fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)

plt.xlabel('Colony size', fontsize = LabelsFontSize)
plt.ylabel('Frequency', fontsize = LabelsFontSize)

if Write2File == 1:
	plt.savefig('Demography_fit_power_law_v3.png', dpi=300, bbox_inches='tight')
plt.show()