#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:33:08 2020

@author: pichugin
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from copy import deepcopy as deepcopy
#from sklearn.decomposition import PCA
#from scipy.interpolate import interp1d

ReloadData = 1
Write2file = 1

File2ReadName = "RosettesCombined.txt"

""" Reading data from file take a lot of time """
if ReloadData == 1:
	PreData = np.loadtxt(File2ReadName, delimiter = ',', skiprows = 1)

LineInBatch = 15000
for i in np.arange(7):
	Subset = PreData[(LineInBatch*i):(LineInBatch*(i+1)),:]
	FileName = 'Combined_piece_'+str(i)+'.txt'
	np.savetxt(FileName, Subset, delimiter = ',')
