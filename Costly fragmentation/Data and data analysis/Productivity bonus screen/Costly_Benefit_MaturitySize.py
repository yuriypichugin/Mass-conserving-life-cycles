#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:23:23 2020

@author: pichugin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap
from matplotlib.colors import to_rgba


def Classification(LC_array):
	ClassValue = 'other'
	if max(LC_array) == 1.0:
		if len(LC_array) == 2:
			ClassValue = 'minimal binary [1, 1]'
		elif len(LC_array) > 2:
			ClassValue = 'minimal fission [1, ..., 1]'
	else:
		Discrepancy = max(LC_array) - min(LC_array)
		if Discrepancy < 0.05:
			if len(LC_array) == 2:
				ClassValue = 'equal binary [x, x]'
			elif len(LC_array) > 2:
				ClassValue = 'equal fission [x, ..., x]'
		else:
			if len(LC_array) == 2:
				ClassValue = 'non-equal binary [x, y]'
			elif len(LC_array) > 2:
				LC_sorted = np.sort(LC_array)
				if LC_sorted[-2] == LC_sorted[0]:
					ClassValue = 'seeding [X, y, ..., y]'
				elif LC_sorted[-1] == LC_sorted[1]:
					ClassValue = 'reminder [X, ..., X, y]'
				else:
					ClassValue = 'other non-equal fission [x, y, ...]'
	return ClassValue

def OutputClasses(LC_array):
	MatSize = 0
	MatSize = sum(LC_array)+1.0

	
	return MatSize

def ExtractPlotData(Data_focal):
	LC_strings_series = Data_focal['OffspringSet']
	LC_array_series = []
	for entry in LC_strings_series:
		LC_array_series.append([float(i) for i in entry.split(';')[:-1]])
	LC_array_series = pd.Series(LC_array_series, index = LC_strings_series.index)
	dfLC = LC_array_series.to_frame(name = 'set')
	dfLC['MaturitySize'] = dfLC['set'].transform(OutputClasses)
	
	Benefit_out = Data_focal['MaxBenefit']
	MaturitySize_out = dfLC['MaturitySize']
	
	idx_benefit = np.argsort(Benefit_out)
	Benefit_out = np.asarray(Benefit_out)[idx_benefit]
	MaturitySize_out = np.asarray(MaturitySize_out)[idx_benefit]
	
	return [Benefit_out, MaturitySize_out]


FlagSave2Fig = 0

Loss = '0.5'
X0 = '5.0'

FolderName = 'Data/'
FileName = 'Costly_Gauss_Benefit_screen_calc1.txt'
Data = pd.read_csv(FolderName+FileName)
Data = Data.drop(['dummy'], axis = 1)

Data_S3 = Data[Data['sigma']==3]
Data_S10 = Data[Data['sigma']==10]

X3, Y3 = ExtractPlotData(Data_S3)
X10, Y10 = ExtractPlotData(Data_S10)


""" Plot Data """

LabelsFontSize = 20
TicksFontSize = 15

plt.style.use('default')
fig, ax = plt.subplots(1,1)

plt.plot(X3, Y3, '-o', color = '#8dd3c7')
plt.plot(X10, Y10, '-o', color = '#fb8072')

plt.ylim(-1.0, 25.0)

#plt.xlim(-0.5, 10.5)
ax.set_aspect(1.0/ax.get_data_ratio())

plt.xticks(fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)

plt.xlabel('Maximal productivity bonus, '+r'$H$', fontsize = LabelsFontSize)
plt.ylabel('Maturity size, '+r'$m^*$', fontsize = LabelsFontSize)


if FlagSave2Fig == 1:
	plt.savefig('Maturity sizes.png', dpi=300, bbox_inches='tight')

plt.show()