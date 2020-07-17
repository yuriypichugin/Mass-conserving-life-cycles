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

def PlotCutoff(Data_X, Data_Y, cutoff):
	LastIndex = sum(Data_Y<cutoff-1e-3)
	Indices = np.arange(0, LastIndex, 5)
	if LastIndex < len(Data_Y):
		for i in np.arange(1,5):
			Indices = np.append(Indices, LastIndex-i)
	else:
		Indices = np.append(Indices, LastIndex-1)
	Indices = np.unique(Indices)
	New_X = Data_X[Indices]
	New_Y = Data_Y[Indices]
	return [New_X, New_Y]

def PlotCutoff_sph(Data_X, Data_Y, cutoff):
	LastIndex = sum(Data_Y<cutoff-1e-3)
	Indices = np.arange(0, LastIndex, 5)
#	if LastIndex < len(Data_Y):
#		for i in np.arange(1,5):
#			Indices = np.append(Indices, LastIndex-i)
#	else:
	Indices = np.append(Indices, LastIndex-1)
	Indices = np.unique(Indices)
	New_X = Data_X[Indices]
	New_Y = Data_Y[Indices]
	return [New_X, New_Y]

""" flag """
Write2File = 1

""" colors """
CLR_S = "black"

CLR_CR1 = '#eec900'
#CLR_CR1 = '#FFA200'
#CLR_CR2 = '#FF8C00'
CLR_CR2 = '#f0a100'
CLR_CR3 = '#EE7600'

""" read data from files """

Data_X = np.loadtxt('SubstrateList.dat')
Data_sph = np.loadtxt('CombinedOffspringSize_sph_ke=1.dat')
Data_R1 = np.loadtxt('CombinedOffspringSize_cyl_ke=1_R=1.dat')
Data_R2 = np.loadtxt('CombinedOffspringSize_cyl_ke=1_R=2.dat')
Data_R3 = np.loadtxt('CombinedOffspringSize_cyl_ke=1_R=3.dat')

""" Data subset """
cutoff = 1000
X_sph, Y_sph = PlotCutoff_sph(Data_X, Data_sph, 1000)
X_R1, Y_R1 = PlotCutoff(Data_X, Data_R1, cutoff)
X_R2, Y_R2 = PlotCutoff(Data_X, Data_R2, cutoff)
X_R3, Y_R3 = PlotCutoff(Data_X, Data_R3, cutoff)

""" compute asymptotics """
Low_R1 = 3.0/(1-1/3.14)
Low_R2 = 3.0/(1-1/3.14/8)
Low_R3 = 3.0/(1-1/3.14/27)
Low_sph = 2*2.92

Vert_R1 = 1.0/2.0*(3.14-1)
Vert_R2 = 2.0/2.0*(3.14*8-1)
Vert_R3 = 3.0/2.0*(3.14*27-1)

X_power = np.asarray([3e1, 1e3])
Coeff_sph = np.power(36*np.pi, 1.0/3.0)/( 2*(np.power(2, 1.0/3.0) - 1) )
Power_sph = 2*np.power(Coeff_sph*X_power, 3.0/4.0)

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

plt.plot(X_sph, Y_sph, 'o',  **marker_style_sph)
plt.plot(X_R1, Y_R1, 'o', **marker_style_R1)
plt.plot(X_R2, Y_R2, 'o', **marker_style_R2)
plt.plot(X_R3, Y_R3, 'o', **marker_style_R3)
#plt.plot(X_R1, Y_R1, 'o', color = CLR_CR1, markersize = 10)
#plt.plot(X_R2, Y_R2, 'o', color = CLR_CR2, markersize = 10)
#plt.plot(X_R3, Y_R3, 'o', color = CLR_CR3, markersize = 10)

LWD = 2
plt.plot([0, 3e-3],[Low_sph, Low_sph], '-', color = CLR_S, linewidth = LWD)
plt.plot([0, 3e-3],[Low_R1, Low_R1], '-', color = CLR_CR1, linewidth = LWD)
plt.plot([0, 3e-3],[Low_R2, Low_R2], '-', color = CLR_CR2, linewidth = LWD)
plt.plot([0, 3e-3],[Low_R3, Low_R3], '-', color = CLR_CR3, linewidth = LWD)

plt.plot([Vert_R1, Vert_R1], [1, 1e3], '--', color = CLR_CR1, linewidth = LWD)
plt.plot([Vert_R2, Vert_R2], [1, 1e3], '--', color = CLR_CR2, linewidth = LWD)
plt.plot([Vert_R3, Vert_R3], [1, 1e3], '--', color = CLR_CR3, linewidth = LWD)

plt.plot(X_power, Power_sph, '-', color = CLR_S, linewidth = LWD )

plt.ylim(1,1000)

ax.set_aspect(2.5)

LabelsFontSize = 20
TicksFontSize = 15	
plt.xlabel('Substrate concentration, U', fontsize = LabelsFontSize)
plt.ylabel('Size at division, '+r'$m^*$', fontsize = LabelsFontSize)
ax.tick_params(labelsize=TicksFontSize)

if Write2File == 1:
	plt.savefig('MaturitySize_MMMa_v4.pdf', dpi=300, bbox_inches = 'tight')

plt.show()

#ax.set_aspect('equal', 'box')
#ax.set_aspect(1.0/ax.get_data_ratio())