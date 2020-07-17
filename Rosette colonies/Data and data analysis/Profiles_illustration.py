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


""" plot the result """
LinesInds = [5,7,8]

CLR_90 = '#f0f0f0'
CLR_50 = '#bdbdbd'
CLR_MD = '#636363'
#CLR_lines = '#016020'
CLR_lines = '#8bbca4'


LabelsFontSize = 20
TicksFontSize = 15

plt.style.use('default')
fig, ax = plt.subplots(1,1)
plt.fill_between(Xarray, QuantilesData[0, :], QuantilesData[-1, :], color = CLR_90)
plt.fill_between(Xarray, QuantilesData[1, :], QuantilesData[-2, :], color = CLR_50)
plt.plot(Xarray, QuantilesData[2, :], color = CLR_MD, lw = 5)
plt.plot(Xarray, Data[LinesInds[0], :], color = CLR_lines, lw = 2)
plt.plot(Xarray, Data[LinesInds[1], :], color = CLR_lines, lw = 2)
plt.plot(Xarray, Data[LinesInds[2], :], color = CLR_lines, lw = 2)


MarkerLoc = 100
marker_selected = ["X",'o','^']
for i in np.arange(3):
	plt.scatter(Xarray[MarkerLoc], Data[LinesInds[i], MarkerLoc], color = CLR_lines, marker = marker_selected[i], s=250)

plt.ylim(0,10.5)
plt.xlim(0,21.5)
ax.set_aspect(1.0/ax.get_data_ratio())

plt.xticks(fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)

plt.xlabel('Colony size, m', fontsize = LabelsFontSize)
plt.ylabel('Productivity, '+r'$g(m)/m$', fontsize = LabelsFontSize)

if Write2file == 1:
	plt.savefig('Profiles_illustration_v4.png', dpi=300, bbox_inches='tight')
plt.show()



""" compute symmetries of chosen lines """
LifeCycles = pd.DataFrame( PreData[IndsFiltered, 1:3], columns = ['Off1', 'Off2'])
LifeCycles['min_off'] = np.minimum(LifeCycles['Off1'], LifeCycles['Off2'])
LifeCycles['max_off'] = np.maximum(LifeCycles['Off1'], LifeCycles['Off2'])
LifeCycles['symmetry'] = (LifeCycles['min_off'] - 1.0) / ( (LifeCycles['min_off'] + LifeCycles['max_off'])/2.0 - 1.0 )

Symmetries = LifeCycles['symmetry']
print(Symmetries[LinesInds])