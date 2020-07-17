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


	
PointsNum = 100
logXlist = np.linspace(0, 4, num = PointsNum, endpoint=False)
Xlist = np.power(10, logXlist)

""" rescale to the scale appropriate for linear interpolation """
Profiles2Itpl = deepcopy(ProfilesData)
#""" !NORMALIZATION! as the model is insensituve to scale """
#for solution in np.arange(len(Profiles2Itpl)):
#	YNodes = Profiles2Itpl.iloc[solution, Length_focal:(2*Length_focal)]
#	Profiles2Itpl.iloc[solution, Length_focal:(2*Length_focal)] = YNodes / sum(YNodes)
##	Profiles2Itpl.iloc[solution, Length_focal:(2*Length_focal)] = YNodes / max(YNodes)
	
if Flag_Log_X == 1:
	for i in np.arange(Length_focal):
		Profiles2Itpl.iloc[:, i] = np.log10(Profiles2Itpl.iloc[:, i])
if Flag_Log_Y == 1:
	for i in np.arange(Length_focal):
		Profiles2Itpl.iloc[:, i+Length_focal] = np.log10(Profiles2Itpl.iloc[:, i+Length_focal] + 1e-6)



""" perform interpolation """
Itpl_result = np.zeros( ( len(Profiles2Itpl) ,  2*len(logXlist) ) )
if Flag_Log_X == 1:
	Itpl_result[:,0:len(logXlist)] = logXlist
else:
	Itpl_result[:,0:len(Xlist)] = Xlist

for solution in np.arange(len(Profiles2Itpl)):
	XNodes = Profiles2Itpl.iloc[solution, 0:Length_focal]
	YNodes = Profiles2Itpl.iloc[solution, Length_focal:(2*Length_focal)]
	
	Interpolation = interp1d(XNodes, YNodes)
	
	Y_interpolated = Interpolation(Itpl_result[0, 0:len(Xlist)])
	
	Itpl_result[solution, len(logXlist):(2*len(logXlist))] = Y_interpolated

Scale = np.ones(len(Profiles2Itpl))
#""" !NORMALIZATION! as the model is insensituve to scale """
#Scale = np.zeros(len(Profiles2Itpl))
#Scale[0] = 1.0
#for solution in np.arange(1, len(Profiles2Itpl)):
#	Y_current = Itpl_result[solution, len(logXlist):(2*len(logXlist))]
#	Y_base = Itpl_result[0, len(logXlist):(2*len(logXlist))]
#	Term1 = sum(np.multiply( Y_current, Y_base ))
#	Term2 = sum(np.multiply( Y_current, Y_current ))
#	Scale[solution] = Term1 / Term2
#	Itpl_result[solution, len(logXlist):(2*len(logXlist))] = Scale[solution] * Y_current
#""" !NORMALIZATION! as the model is insensituve to scale """
#Scale = np.ones(len(Profiles2Itpl))
#Scale[0] = 1.0
#for solution in np.arange(1, len(Profiles2Itpl)):
#	Y_current = np.log10(Itpl_result[solution, len(logXlist):(2*len(logXlist))])
#	Y_base = np.log10(Itpl_result[0, len(logXlist):(2*len(logXlist))])
#	LogScale = 1.0/len(logXlist) * sum( Y_current -  Y_base)
#	Scale[solution] = np.power(10, LogScale)
#	Itpl_result[solution, len(logXlist):(2*len(logXlist))] = Scale[solution] * np.power(10, Y_current)

""" Average across solutions """
QuantilesList = [0.05, 0.25, 0.5, 0.75, 0.95]
QuantilesData = np.quantile(Itpl_result, QuantilesList, axis = 0)


""" find the average location of nodes """
AverageXNodes = np.zeros(Length_focal)
AverageYNodes = np.zeros(Length_focal)
for i in np.arange(Length_focal):
	AverageXNodes[i] = np.median( Profiles2Itpl.iloc[:,i] )
	AverageYNodes[i] = np.median( np.multiply(Profiles2Itpl.iloc[:,i + Length_focal], Scale[i]) )

""" cast all the outcomes into the log-scale on Y """
if Flag_Log_Y == 0:
	QuantilesData[:, len(logXlist):(2*len(logXlist))] = np.log10(QuantilesData[:, len(logXlist):(2*len(logXlist))] )
	AverageYNodes = np.log10(AverageYNodes)
if Flag_Log_X == 0:
	AverageXNodes = np.log10(AverageXNodes)


""" plot the result """
#	CLR_90 = '#f7fcb9'
#	CLR_50 = '#addd8e'
#	CLR_MD = '#31a354'

CLR_90 = '#b2e2e2'
CLR_50 = '#2ca25f'
CLR_MD = '#006d2c'

Yinds = np.arange(len(logXlist), (2*len(logXlist)))

plt.style.use('default')
fig, ax = plt.subplots(1,1)

plt.fill_between(logXlist, QuantilesData[0, Yinds], QuantilesData[-1, Yinds], color = CLR_90)
plt.fill_between(logXlist, QuantilesData[1, Yinds], QuantilesData[-2, Yinds], color = CLR_50)
plt.plot(logXlist, QuantilesData[2, Yinds], color = CLR_MD)
plt.scatter(AverageXNodes, AverageYNodes, marker = 'x', s = 70, color = 'black')


YLim = [-3, 3]
plt.ylim(YLim[0], YLim[1])
plt.xlim(0,4)
ax.set_aspect(1.0/ax.get_data_ratio())

Yticks_pos = np.arange(YLim[0], YLim[1]+0.1)
Yticks_lab = []
for position in Yticks_pos:
	Yticks_lab.append(r'$10^{'+str(int(position))+'}$')

LabelsFontSize = 20
TicksFontSize = 15
plt.xticks([0,1,2,3,4], [r'$10^0$', r'$10^1$', r'$10^2$', r'$10^3$', r'$10^4$'], fontsize = TicksFontSize)
#plt.yticks([ -3, -2, -1, 0, 1, 2, 3], [r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^0$', r'$10^1$', r'$10^2$',  r'$10^3$'], fontsize = TicksFontSize)	
plt.yticks(Yticks_pos, Yticks_lab, fontsize = TicksFontSize)
plt.xlabel('Colony size, m', fontsize = LabelsFontSize)
plt.ylabel('Productivity, '+r'$g(m)/m$', fontsize = LabelsFontSize)

if WriteFigures == 1:
	plt.savefig('Profiles_statistics_'+FileName_focal+'_v4.png', dpi=300, bbox_inches='tight')
plt.show()

