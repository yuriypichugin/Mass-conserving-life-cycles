# -*- coding: utf-8 -*-
"""
Created on Wed May 23 15:13:06 2018

@author: pichugin
"""

import numpy as np
#import matplotlib.pyplot as plt


""" Functions for finding the population growth rate """

def LambdaDiff(L, Fragments, Loss, X, T):
	"""
	This compute the discrepancy in the continuous equation at a given value of lambda.
	
	Arguments:
		(float) L 	 	 	- the tested value of population growth rate lambda
		(list of float) Fragments 	 	- the list of fragment sizes
		(float) Loss 	 	 	- the amount of biomass lost at fragmentation
		(list of floats) X 	- the list of sizes
		(list of floats) T 	- the list of growth times
	
	Return:
		(float) Diff 	 	- the discrepancy
	"""

	ParentSize = sum(Fragments)+Loss
	if ParentSize > X[-1]:
		""" if the parent size is too big for supplied X, exit """
		return float('NaN')
	if min(Fragments) < X[0]:
		""" if the offspring sizes are too small"""
		return float('NaN')
	ParentPosition = np.argmin(abs(X - ParentSize))
#	Diff = np.exp(L*T[ParentPosition])
	Diff = 1
	
	for frag in Fragments:
		FragPosition = np.argmin(abs(X - frag))
		Diff -= np.exp(  L*(T[FragPosition] - T[ParentPosition])  )
	return Diff	

def LambdaBisect(Fragments, Loss, X, G, T):
	"""
	Computes lambda by minimizing discrepancy
	
	Arguments:
		(float) L 	 	 	- the tested value of population growth rate lambda
		(list of float) Fragments 	 	- the list of fragment sizes
		(float) Loss 	 	 	- the amount of biomass lost at fragmentation
		(list of floats) X 	- the list of sizes
		(list of floats) T 	- the list of growth times
	
	Return:
		(float) Lambda 	 	- the population growth rate
	"""
	Laccuracy=1e-9
#	Lmin = min(np.divide(G,X+1e-6))
	Lmin = 0
	Lmax = max(np.divide(G,X+1e-6))
	
	DiffMin=np.sign(LambdaDiff(Lmin, Fragments, Loss, X, T))
	DiffMax=np.sign(LambdaDiff(Lmax, Fragments, Loss, X, T))
	while DiffMax<0:
		Lmax = Lmax*2
		DiffMax=np.sign(LambdaDiff(Lmax, Fragments, Loss, X, T))
		
	if(DiffMin*DiffMax>0):
		print("Initial L-s are inefficient")
	else:
		while(Lmax - Lmin > Laccuracy):
			Lmid = (Lmax+Lmin)/2.0
			DiffMid=np.sign(LambdaDiff(Lmid, Fragments, Loss, X, T))
			if(DiffMid*DiffMax)<0:
				DiffMin = DiffMid
				Lmin = Lmid
			else:
				DiffMax = DiffMid
				Lmax = Lmid
	return (Lmax+Lmin)/2.0

""" Functions for generating growth, and death rates profiles """

def XGT_generate(XParams, GParams, GenerationMethod):
	""" 
	Generates growth/death rates profiles
	
	Arguments:
		(list of various) XParams 	- the set of size range parameters
								[0] is the minimal size (usually 1)
								[1] is the maximal size
								[2] is the step between neighbouring dots
		(list of various) GParams 	- the set of growth rate parameters
		(int) GenerationMethod 	- the method of X vector genration 
								(np.arange or np.linspace)
								0 is for discrete model
								1 is for continuous model
	
	Return:
		(list of lists) XBT 	- the list of output lists
							[0] is the list of sizes X
							[1] is the list of growth rates G
							[2] is the list of growth times T
	
	
	"""
	Xmin = XParams[0]
	Xmax = XParams[1]
	dx = XParams[2]
	
	if GenerationMethod==0:
		""" method 0 is appropriate for profiles used in discrete model """
		X = np.arange(Xmin, Xmax, dx)
	else:
		""" method 1 is appropriate for profiles used in continuous model """
		Nsteps = int(np.ceil((Xmax-Xmin)/dx))+1
		X = np.linspace(Xmin, Xmax, num = Nsteps)
	
	""" Here G is the group net growth rate! the cell birth rate would be B = G/X. """
	G = G_generate(X, GParams)

	T=np.zeros(len(G))
	for i in np.arange(1,len(T)):
		T[i] = T[i-1] + (X[i]-X[i-1])/((G[i]+G[i-1])/2.0 + 1e-10)
	return [X, G, T]

#def XBD_generate(XParams, BParams, DParams, GenerationMethod):
#	""" 
#	Generates growth/death rates profiles
#	
#	Arguments:
#		(list of various) XParams 	- the set of size range parameters
#								[0] is the minimal size (usually 1)
#								[1] is the maximal size
#								[2] is the step between neighbouring dots
#		(list of various) BParams 	- the set of birth rate parameters
#		(list of various) DParams 	- the set of death rate parameters
#		(int) GenerationMethod 	- the method of X vector genration 
#								(np.arange or np.linspace)
#								0 is for discrete model
#								1 is for continuous model
#	
#	Return:
#		(list of lists) XBD 	- the list of output lists
#							[0] is the list of sizes X
#							[1] is the list of growth rates B
#							[2] is the list of death rates D
#	
#	
#	"""
#	Xmin = XParams[0]
#	Xmax = XParams[1]
#	dx = XParams[2]
#	
#	if GenerationMethod==0:
#		""" method 0 is appropriate for profiles used in discrete model """
#		X = np.arange(Xmin, Xmax, dx)
#	else:
#		""" method 1 is appropriate for profiles used in continuous model """
#		Nsteps = int(np.ceil((Xmax-Xmin)/dx))+1
#		X = np.linspace(Xmin, Xmax, num = Nsteps)
#	
#	B = B_generate(X, BParams)
##	dB=np.zeros(len(X))
##	for i in np.arange(len(dB)-1):
##		dB[i] = (B[i+1]-B[i])/(X[i+1]-X[i])
#	D = D_generate(X, DParams)
#	return [X, B, D]

def G_generate(x, Parameters):
	"""
	Genarates the birth rates vector
	
	Arguments:
		(list of floats) X 			- the list of sizes at which the birth  
									rates are computed 
		(list of various) Parameters 	- the list of related parameters
									[0] must be the index of used model
									[>0] are model parameters
		
	Return:
		(list of floats) g 			- the list of birth rates
		
	Note:
		notation b - is the list of productivities, 
		while g - is the list of organism growth rates, g(x) = x b(x).
		
	"""
	g=np.array([])
	Model = Parameters[0]
	if Model == 1:
		""" Model 1 is gaussian bell """
		x_0 = Parameters[1]
		sigma = Parameters[2]
		prefactor = Parameters[3]
		b = prefactor*np.exp( -np.power((x-x_0),2)/(2.0*sigma*sigma) )
	elif Model == 2:
		""" Models 2 is power law """
		M = Parameters[1]
		alpha = Parameters[2]
		NMax = Parameters[3]
		b = 1 + M*np.power( (x-1)/(NMax-1), alpha )
	elif Model == 3:
		""" Model 3 is rectangular profile """
		B_perturbed = Parameters[1]
		X_min = Parameters[2]
		X_max = Parameters[3]
		b = 1 + (B_perturbed-1)*(x>=X_min)*(x<=X_max)
	elif Model == 4:
		""" Model 4 is a sharp peak with exponential decay """
		x_0 = Parameters[1]
		var = Parameters[2]
		Peak = Parameters[3]
		b = Peak*np.exp(-abs((x-x_0)/var))
	elif Model == 5:
		""" Model 5 is a smooth peak with 1/x decay """
		x_0 = Parameters[1]
		var = Parameters[2]
		Peak = Parameters[3]
		b = Peak/(1+abs((x-x_0)/var))
	elif Model == 6:
		""" Model 6 is bumped gaussian bell """
		x_0 = Parameters[1]
		sigma = Parameters[2]
		prefactor = Parameters[3]
		b = 1+prefactor*np.exp( -np.power((x-x_0),2)/(2.0*sigma*sigma) )
	elif Model == 7:
		""" Model 7 is a bumped sharp peak with exponential decay """
		x_0 = Parameters[1]
		var = Parameters[2]
		Peak = Parameters[3]
		b = 1 + Peak*np.exp(-abs((x-x_0)/var))
	elif Model == 8:
		""" Model 8 is a bumped smooth peak with 1/x decay """
		x_0 = Parameters[1]
		var = Parameters[2]
		Peak = Parameters[3]
		b = 1 + Peak/(1+abs((x-x_0)/var))
	elif Model == 9:
		""" Model 9 is a rectangular step function """
		x_0 = Parameters[1]
		HLeft = Parameters[2]
		HRight = Parameters[3]
		b = HLeft*(x<x_0)+HRight*(x>=x_0)
	elif Model == 10:
		""" Model 10 is the sigmoid function """
		x_0 = Parameters[1]
		HLeft = Parameters[2]
		HRight = Parameters[3]
		Sigma = Parameters[4]
		b = HLeft + (HRight - HLeft)/(1.0 + np.exp(-(x-x_0)/Sigma))
	elif Model == 11:
		""" Model 11 is a bumped smooth peak with x^(-n) decay """
		x_0 = Parameters[1]
		var = Parameters[2]
		Peak = Parameters[3]
		Pwr = Parameters[4]
		b = 1 + Peak/(1+np.power(abs((x-x_0)/var), Pwr))
	elif Model == 12:
		""" Model 12 is Michaelis Menton Monod kinetics for spherical cells """
		""" 	ke, k0 - parameters of reaction
			F - the resource inflow (surface area)
			E0 - amount of enzymes (volume minus DNA)
			s - amount of nutrients avalable in the environment"""
		ke = Parameters[1]
		k0 = Parameters[2]
		s = Parameters[3]
		E0 = x-1
		F = s*np.power(36*np.pi, 1.0/3.0)*np.power(x, 2.0/3.0)
		g = 0.5*( ke*x + k0*E0 + F - np.sqrt( np.power(ke*x + k0*E0 - F, 2) + 4*ke*x*F ) )
	elif Model == 13:
		""" Model 13 is Michaelis Menton Monod kinetics for disc cells """
		""" 	ke, k0 - parameters of reaction
			F - the resource inflow (surface area)
			E0 - amount of enzymes (volume minus DNA)
			L - hight of the disc
			s - amount of nutrients avalable in the environment"""
		ke = Parameters[1]
		k0 = Parameters[2]
		L = Parameters[3]
		s = Parameters[4]
		E0 = x-1
		F = 2*s*( np.power(np.pi*L*x, 0.5) + x/L )
		g = 0.5*( ke*x + k0*E0 + F - np.sqrt( np.power(ke*x + k0*E0 - F, 2) + 4*ke*x*F ) )
	elif Model == 14:
		""" Model 14 is Michaelis Menton Monod kinetics for cyllindric cells """
		""" 	ke, k0 - parameters of reaction
			F - the resource inflow (surface area)
			E0 - amount of enzymes (volume minus DNA)
			R - radius of the cyllinder
			s - amount of nutrients avalable in the environment"""
		ke = Parameters[1]
		k0 = Parameters[2]
		R = Parameters[3]
		s = Parameters[4]
		E0 = x-1
		F = 2*s*( np.pi*R*R + x/R )
		g = 0.5*( ke*x + k0*E0 + F - np.sqrt( np.power(ke*x + k0*E0 - F, 2) + 4*ke*x*F ) )
	elif Model == 15:
		""" Model 15 is a bumped asymmetric smooth peak with x^(-n) decay """
		x_0 = Parameters[1]
		var1 = Parameters[2][0]
		var2 = Parameters[2][1]
		Peak = Parameters[3]
		Pwr = Parameters[4]
		b = 1 + Peak/(1+np.power(  (x_0 - x)/var1*(x<x_0) + (x-x_0)/var2*(x>=x_0)  , Pwr))
	elif Model == 16:
		""" Model 16 is approximate Michaelis Menton Monod kinetics for spherical cells """
		""" 	k0, ke - rates of reactions
			S_0 - concentration of substrate in the environment
			F - the resource inflow (surface area)
			E0 - amount of enzymes (volume minus DNA)"""
		ke = Parameters[1]
		k0 = Parameters[2]
		S_0 = Parameters[3]
		E0 = x-1
		F = S_0 * np.power(36*np.pi, 1.0/3.0) * np.power(x, 2.0/3.0)
		g = k0 * E0 * F / (F + ke*x)
	elif Model == 17:
		""" Model 17 is approximate Michaelis Menton Monod kinetics for cyllindric cells """
		""" 	ke, k0 - parameters of reaction
			F - the resource inflow (surface area)
			E0 - amount of enzymes (volume minus DNA)
			R - radius of the cyllinder
			S_0 - amount of nutrients avalable in the environment"""
		ke = Parameters[1]
		k0 = Parameters[2]
		R = Parameters[3]
		S_0 = Parameters[4]
		E0 = x-1
		F = 2*S_0*( np.pi*R*R + x/R )
		g = k0 * E0 * F / (F + ke*x)
	elif Model == 18:
		""" Model 18 is the model of bee hive with workers doing foraging for food,
		 which converts into new brood members """
		""" 	U - the food density in environment
			kc - the rate of food consumption by workers
			m - the death rate of workers
			L - the queen bee egg laying rate
			f0 - the saturation constant for food
		"""
		U = Parameters[1]
		kc = Parameters[2]
		m = Parameters[3]
		L = Parameters[4]
		f0 = Parameters[5]
		Food = 2*np.sqrt(np.pi * U * x) - kc * x
		g = L*Food/(Food+f0) - m * x
	elif Model == 19:
		"""
		Model 19 is the interpolation through the list of nodes
		Arguments:
			(list of floats) Params[0] - X-coordinates of the nodes
			(list of floats) Params[1] - Y-coordinates of the nodes
		"""
		xnodes = Parameters[1]
		ynodes = Parameters[2]
		
		b = np.zeros(len(x))
		
		count = 0
		for X in x:
			ind = sum(X > xnodes)
			y = (X-xnodes[ind-1])/(xnodes[ind] - xnodes[ind-1])*(ynodes[ind] - ynodes[ind-1])+ynodes[ind-1]
			b[count] = y
			count+=1
	else:
		""" Default model is neutral g(x) = x """
		b = 1
	if sum(abs(g)) == 0:
		g = np.array(b)*x
	return g

def D_generate(x, Parameters):
	"""
	Genarates the death rates vector
	
	Arguments:
		(list of floats) X 			- the list of sizes at which the death  
									rates are computed 
		(list of various) Parameters 	- the list of related parameters
									[0] must be the index of used model
									[>0] are model parameters
		
	Return:
		(list of floats) d 			- the list of death rates
		
	"""
	Model = Parameters[0]
	if Model == 9:
		""" Model 9 is a rectangular step function """
		x_0 = Parameters[1]
		HLeft = Parameters[2]
		HRight = Parameters[3]
		d = HLeft*(x<x_0)+HRight*(x>=x_0)
	elif Model == 10:
		""" Model 10 is the sigmoid function """
		x_0 = Parameters[1]
		HLeft = Parameters[2]
		HRight = Parameters[3]
		Sigma = Parameters[4]
		d = HLeft + (HRight - HLeft)/(1.0 + np.exp(-(x-x_0)/Sigma))
	else:
		d = np.zeros(len(x))
	return d

def OptimizeGrowth(XParams, GParams, Loss, Perturbation, NumofOffspring):
	"""
	Find the optimal fragmentaiton mode for given environment
	Arguments:
		(list) XParams - the set of parameters to generate X-array
		(list) GParams - the set of parameters to generate G-array
		(float) Loss - the amount of biomass, lost at the fragmentation
		(float) Perturbation - the change in the offspring size (should be greater than the step in X)
		(int) NumofOffspring - the number of offspring (at Loss = 0, this should be 2)
	Return:
		(list) Output
			Output[0] - the optimal number of offspring
			Output[1] - the optimal life cycle, list of the offspring sizes
			Output[2] - the maximal population growth rate
	"""

#	Perturbation = 0.2
	
	[X,G,T] = XGT_generate(XParams, GParams, 1)

	""" grid optimization of life cycle """
	BLArray=[]
	BFRGArray=[]
	""" initialize life cycle """
#	bestFRG = max(GParams[1], 1.1) * np.ones(2)
	bestFRG = 3 * np.ones(NumofOffspring)
	bestLambda = LambdaBisect(bestFRG, Loss, X, G, T)
	
	""" while better neighbours on the grid are being found, continue optimization"""
	TheBestFound = 0
	while TheBestFound == 0:
		CurrentBestFRG = np.array(bestFRG)
		CurrentBestLambda = bestLambda
		TheBestFound = 1
		""" for each of the offspring group """
		for index in np.arange(len(bestFRG)):
			""" test slightly larger offspring """
			testFRG = np.array(bestFRG)
			testFRG[index] += Perturbation
			testLambda = LambdaBisect(testFRG, Loss, X, G, T)
			if testLambda > CurrentBestLambda:
				CurrentBestFRG = np.array(testFRG)
				CurrentBestLambda = testLambda
				TheBestFound=0
			
			""" test slightly smaller offspring """
			testFRG = np.array(bestFRG)
			testFRG[index] -= Perturbation
			if testFRG[index] > 1:
				testLambda = LambdaBisect(testFRG, Loss, X, G, T)
				if testLambda > CurrentBestLambda:
					CurrentBestFRG = np.array(testFRG)
					CurrentBestLambda = testLambda
					TheBestFound=0
		bestFRG = np.array(CurrentBestFRG)
		bestLambda = np.array(CurrentBestLambda)
	""" remember the best life cycle for each given fragments number """				
	BLArray.append(bestLambda)
	BFRGArray.append(bestFRG)
	
	""" optimize over fragments number """
	""" !! Probably, unnecessary !!"""
	BestOffNum = np.argmax(BLArray)
	TotalBestLC = BFRGArray[BestOffNum]
	TotalBestLambda = BLArray[BestOffNum]
	return [BestOffNum+2, TotalBestLC, TotalBestLambda]