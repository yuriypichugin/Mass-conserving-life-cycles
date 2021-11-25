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
	ClassValue = 'other'
	OffNum = len(LC_array)
	Discrepancy = max(LC_array) - min(LC_array)
	if OffNum > 12:
		ClassValue = 'too many offspring'
	else:
		if Discrepancy > 0.06:
			if OffNum == 2:
				ClassValue = 'unequal binary'
			elif OffNum > 2:
				ClassValue = 'unequal fission'
		else:
			ClassValue = 'equal fission '+str(OffNum)

	return ClassValue



FlagSave2Fig = 1

Benefit = '1.0'
X0 = '5.0'

FolderName = 'Data/'
FileName = 'Costly_Gauss_Loss_Sigma_screen_calc5.txt'
Data = pd.read_csv(FolderName+FileName)
Data = Data.drop(['dummy'], axis = 1)


""" convert data """
LC_strings_series = Data['OffspringSet']
LC_array_series = []
for entry in LC_strings_series:
	LC_array_series.append([float(i) for i in entry.split(';')[:-1]])

LC_array_series = pd.Series(LC_array_series, index = LC_strings_series.index)

dfLC = LC_array_series.to_frame(name = 'set')
dfLC['sigma'] = Data['sigma']
dfLC['loss'] = Data['MassLoss']

""" perform classification """
dfLC['class'] = dfLC['set'].transform(OutputClasses)



""" plot data """
value_to_int = {'unequal binary' : 0,
 			  'unequal fission': 1,
			   'equal fission 2': 2,
			   'equal fission 3': 3,
			   'equal fission 4': 4,
			   'equal fission 5': 5,
			   'equal fission 6': 6,
			   'equal fission 7': 7,
			   'equal fission 8': 8,
			   'equal fission 9': 9,
			   'equal fission 10': 10,
			   'equal fission 11': 11,
			   'equal fission 12': 12,
			   'equal fission 13': 13,
			   'equal fission 14': 14,
			   'equal fission 15': 15,
			   'too many offspring': 16
			   }
n = len(value_to_int) 

BaseCmap = "terrain"

Set1List = cm.get_cmap(BaseCmap, n)(np.linspace(0, 1, n))
Set1ColorMap = ListedColormap(Set1List)

ColorSet2 = ['#5e3c99', '#888888', '#e66101', '#eb6d1f', '#ef7933', '#f38444', '#f78f55', '#fa9a65',
			 '#fda676', '#ffb186', '#ffbc97', '#ffc7a8', '#ffd2b9', '#ffddca',
			 '#ffe8dc', '#fff4ed', '#ffffff']

List2 = list(map(to_rgba, ColorSet2))
Set2ColorMap = ListedColormap(List2)

cmap = sns.color_palette(BaseCmap, n) 
Data2Plot = dfLC.pivot('sigma', 'loss', 'class')
Data2Plot = Data2Plot.replace(value_to_int)
Data2Plot = Data2Plot.fillna(8)

fig, ax1 = plt.subplots(1, 1)
graph = sns.heatmap(Data2Plot, cmap = Set2ColorMap, vmin=0, vmax=len(List2))
ax1.invert_yaxis()
ax1.set_aspect(1.0/ax1.get_data_ratio())

colorbar = ax1.collections[0].colorbar 
r = colorbar.vmax - colorbar.vmin 
colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
colorbar.set_ticklabels(list(value_to_int.keys()))                                          

locs, labels = plt.yticks()
plt.xticks(0.5 + np.arange(0, 61, 20), ['0.0', '1.0', '2.0', '3.0'])
graph.set_xticklabels(['0.0', '1.0', '2.0', '3.0'],rotation=0)

Y_labels = np.asarray([0.1, 1.0, 2.0, 3.0, 4.0, 5.0])
Y_positions = 20*Y_labels-1.5
plt.yticks(Y_positions, Y_labels)

plt.xlabel('Mass loss', fontsize = 15)
plt.ylabel('Productivity peak width, '+r'$\sigma$', fontsize = 15)

if FlagSave2Fig == 1:
	plt.savefig('Calc5_Output_MaxBenefit='+Benefit+'_x0='+X0+'.png', dpi=300, bbox_inches='tight')

plt.show()

