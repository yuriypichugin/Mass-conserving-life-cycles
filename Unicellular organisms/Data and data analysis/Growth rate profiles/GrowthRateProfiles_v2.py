#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:00:37 2020

@author: pichugin
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from copy import deepcopy

""" flag """
Write2File = 1

""" colors """
CLR_S = "black"

CLR_CR1 = '#eec900'
#CLR_CR1 = '#FFA200'
#CLR_CR2 = '#FF8C00'
CLR_CR2 = '#F0A100'
CLR_CR3 = '#EE7600'

""" read data from files """

Data_X = np.loadtxt('SubstrateList.dat')
Data_sph = np.loadtxt('GrowthRatesMap_sph_ke=1.dat')
Data_R1 = np.loadtxt('GrowthRatesMap_cyl_ke=1_R=1.dat')
Data_R2 = np.loadtxt('GrowthRatesMap_cyl_ke=1_R=2.dat')
Data_R3 = np.loadtxt('GrowthRatesMap_cyl_ke=1_R=3.dat')

""" Data subset """
Indices = np.arange(0, len(Data_X), 3)
PlotData_X = Data_X[Indices]
PlotData_sph = Data_sph[Indices]
PlotData_R1 = Data_R1[Indices]
PlotData_R2 = Data_R2[Indices]
PlotData_R3 = Data_R3[Indices]

""" make plot """
plt.style.use('default')
fig, ax = plt.subplots(1,1)
plt.yscale('log')
plt.xscale('log')

marker_size = 10
marker_style_sph = dict(marker='^', markersize=marker_size, fillstyle = 'full', color = CLR_S)
marker_style_R1 = dict(marker='o', markersize=marker_size, fillstyle = 'none', color = CLR_CR1, markeredgewidth = 2)
marker_style_R2 = dict(marker='o', markersize=marker_size, fillstyle = 'none', color = CLR_CR2, markeredgewidth = 2)
marker_style_R3 = dict(marker='o', markersize=marker_size, fillstyle = 'none', color = CLR_CR3, markeredgewidth = 2)

plt.plot(PlotData_X, PlotData_sph, 'o',  **marker_style_sph)
plt.plot(PlotData_X, PlotData_R1, 'o', **marker_style_R1)
plt.plot(PlotData_X, PlotData_R2, 'o', **marker_style_R2)
plt.plot(PlotData_X, PlotData_R3, 'o', **marker_style_R3)

#plt.plot(PlotData_X, PlotData_sph, 'o', color = CLR_S, markersize = 10)
#plt.plot(PlotData_X, PlotData_R1, 'o', color = CLR_CR1, markersize = 10)
#plt.plot(PlotData_X, PlotData_R2, 'o', color = CLR_CR2, markersize = 10)
#plt.plot(PlotData_X, PlotData_R3, 'o', color = CLR_CR3, markersize = 10)

ax.set_aspect(1.9)
#ax.set_aspect(1.0/ax.get_data_ratio())

LabelsFontSize = 20
TicksFontSize = 15
plt.xlabel('Substrate concentration, U', fontsize = LabelsFontSize)
plt.ylabel('Growth rate, '+r'$\lambda$', fontsize = LabelsFontSize)
ax.tick_params(labelsize=TicksFontSize)

if Write2File == 1:
	plt.savefig('GrowthRate_MMMa_v4.pdf', dpi=300, bbox_inches = 'tight')

plt.show()

#ax.set_aspect('equal', 'box')
#ax.set_aspect(1.0/ax.get_data_ratio())