#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 19:28:30 2019

@author: pichugin
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy as deepcopy
from sklearn.decomposition import PCA
from scipy.interpolate import interp1d


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
WriteFigures = 1


sns.set()

ErrorCutoff = 0.025
#ErrorCutoff = 0.005


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


""" read and prepare data """

SpData = pd.read_csv(FileName_focal+'.txt')
SpData = ColumnNamesUnification(SpData, [Length_focal])
SpData = DataClean(SpData, [ErrorCutoff])







ProfilesData = SpData.iloc[:, np.arange(2*Length_focal)]


#if DoLifeCyclesContours == 1:
	
CLR_50 = '#2ca25f'

plt.style.use('default')
fig, ax = plt.subplots(1,1)

plt.scatter(SpData['Small_off'], SpData['Large_off'], color = CLR_50)
sns.kdeplot(SpData['Small_off'], SpData['Large_off'])

ax.set_aspect(1.0/ax.get_data_ratio())

LabelsFontSize = 20
TicksFontSize = 15
plt.xlabel('Smaller part', fontsize = LabelsFontSize)
plt.ylabel('Larger part', fontsize = LabelsFontSize)
plt.xticks(fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)


if WriteFigures == 1:
	plt.savefig('life_cycles_linear_'+FileName_focal+'_v2.png', dpi=300, bbox_inches='tight')
plt.show()
	
	
	
	