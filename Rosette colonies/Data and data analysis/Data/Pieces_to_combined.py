#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 13:33:08 2020

@author: pichugin
"""

import numpy as np

ReloadData = 1
Write2file = 1

if ReloadData == 1:
	Data = 7*[0]
	for i in np.arange(7):
		File2ReadName = 'Combined_piece_'+str(i)+'.txt'
		Data[i] = np.loadtxt(File2ReadName, delimiter = ',')

File2WriteName = "RosettesCombined_recovered.txt"

DataFull = np.concatenate(Data)
np.savetxt(File2WriteName, DataFull, delimiter = ',')
