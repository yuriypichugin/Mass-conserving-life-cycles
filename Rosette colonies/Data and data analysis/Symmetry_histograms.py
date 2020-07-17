#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:21:37 2019

@author: pichugin
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy as deepcopy
#from sklearn.decomposition import PCA
#from scipy.interpolate import interp1d

Write2file = 1
ReloadData = 0



File2ReadName = "Data/RosettesCombined_recovered.txt"

""" Reading data from file take a lot of time """
if ReloadData == 1:
	PreData = np.loadtxt(File2ReadName, delimiter = ',')


Xarray = PreData[0, 4:]

""" filter out not converged optimizations, where the max size is less than 20 """
IndsFiltered = np.where(PreData[:,1]+PreData[:,2]>=20)[0]
Data = PreData[IndsFiltered, 4:]
LifeCycles = pd.DataFrame( PreData[IndsFiltered, 1:3], columns = ['Off1', 'Off2'])
LifeCycles['min_off'] = np.minimum(LifeCycles['Off1'], LifeCycles['Off2'])
LifeCycles['max_off'] = np.maximum(LifeCycles['Off1'], LifeCycles['Off2'])
LifeCycles['symmetry'] = (LifeCycles['min_off'] - 1.0) / ( (LifeCycles['min_off'] + LifeCycles['max_off'])/2.0 - 1.0 )

""" Average across solutions """
QuantilesList = [0.05, 0.25, 0.5, 0.75, 0.95]
QuantilesData = np.quantile(Data, QuantilesList, axis = 0)

""" compute frequncies """
AHist, edges = np.histogram(LifeCycles['symmetry'], bins = 30)
AHist = AHist/sum(AHist)
X_bars = np.zeros(len(edges) - 1)
for i in np.arange(len(X_bars)):
	X_bars[i] = (edges[i]+edges[i+1])/2.0


	
""" plot the linear histogram """
LabelsFontSize = 20
TicksFontSize = 15

#fig, ax = plt.subplots(1,1)
fig = plt.figure(figsize=(5,5))
ax = plt.subplot(111)
plt.bar(X_bars, AHist, lw = 1, edgecolor = 'black', width = X_bars[1]-X_bars[0], color = 'grey', zorder = 1)


X_selected = [0.989, 0.968, 0.630]
Y_selected = [0.065, 0.095, 0.08]
marker_selected = ["X",'o','^']
#CLR_selected = '#016020'
CLR_selected = '#8bbca4'
for i in np.arange(3):	
	plt.scatter(X_selected[i], Y_selected[i], marker = marker_selected[i], s = 250, color = CLR_selected, zorder = 2)


ax.set_aspect(1.0/ax.get_data_ratio())
plt.xticks(fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)

plt.xlabel('Mass distribution symmetry, A', fontsize = LabelsFontSize)
plt.ylabel('Frequency', fontsize = LabelsFontSize)
if Write2file == 1:
	plt.savefig('Symmetry_histogram_linear_v4.png', dpi=300, bbox_inches='tight')
plt.show()



#""" plot the log histogram """
#LabelsFontSize = 25
#TicksFontSize = 22
#
#fig, ax = plt.subplots(1,1)
#plt.bar(X_bars, AHist, lw = 1, edgecolor = 'black', width = X_bars[1]-X_bars[0], log = True)
#
#
#ax.set_aspect(1.0/ax.get_data_ratio())
#
#Xticks = [0.0, 0.5, 1.0]
#Yticks = [0.0001, 0.01, 1.0]
#plt.xticks(Xticks, fontsize = TicksFontSize)
#plt.yticks(Yticks, fontsize = TicksFontSize)
#
#if Write2file == 1:
#	plt.savefig('Symmetry_histogram_log_v2.png', dpi=300)
#plt.show()