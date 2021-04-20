r#!/usr/bin/env python3
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

ReloadData = 0
Write2file = 1

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

ProfilesHighA = Data[LifeCycles['symmetry'] == 1]
ProfilesLowA = Data[LifeCycles['symmetry'] < 0.2]

""" Average across solutions """
QuantilesList = [0.25, 0.5, 0.75]
QuantilesData = np.quantile(Data, QuantilesList, axis = 0)
QuantilesHighA = np.quantile(ProfilesHighA, QuantilesList, axis = 0)
QuantilesLowA = np.quantile(ProfilesLowA, QuantilesList, axis = 0)

""" plot the result """

CLR_50_all = '#bdbdbd'
CLR_MD_all = '#636363'
CLR_50_low = '#b2abd2'
CLR_MD_low = '#5e3c99'
CLR_50_high = '#fdb863'
CLR_MD_high = '#e66101'


Alpha = 0.3

LabelsFontSize = 20
TicksFontSize = 15

plt.style.use('default')
fig, ax = plt.subplots(1,1)
plt.fill_between(Xarray, QuantilesData[0, :], QuantilesData[-1, :], color = CLR_MD_all, alpha=Alpha)
plt.plot(Xarray, QuantilesData[1, :], color = CLR_MD_all, lw = 3)

plt.fill_between(Xarray, QuantilesHighA[0, :], QuantilesHighA[-1, :], color = CLR_MD_high, alpha=Alpha)
plt.plot(Xarray, QuantilesHighA[1, :], color = CLR_MD_high, lw = 3)

plt.fill_between(Xarray, QuantilesLowA[0, :], QuantilesLowA[-1, :], color = CLR_MD_low, alpha=Alpha)
plt.plot(Xarray, QuantilesLowA[1, :], color = CLR_MD_low, lw = 3)


plt.ylim(0,10.5)
plt.xlim(0,21.5)
ax.set_aspect(1.0/ax.get_data_ratio())

plt.xticks(fontsize = TicksFontSize)
plt.yticks(fontsize = TicksFontSize)

plt.xlabel('Colony size, m', fontsize = LabelsFontSize)
plt.ylabel('Productivity, '+r'$g(m)/m$', fontsize = LabelsFontSize)

if Write2file == 1:
	plt.savefig('Profiles_classes_v3.png', dpi=300, bbox_inches='tight')
#	plt.savefig('Profiles_high_A.png', dpi=300)
#	plt.savefig('Profiles_low_A.png', dpi=300)
plt.show()

