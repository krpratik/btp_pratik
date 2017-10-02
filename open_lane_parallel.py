import random
from random import randint
import numpy as np 
import copy as cp
import matplotlib.pyplot as plt
# Define the number of cells on the the circular track (Basically the length of the circular Track)
numberOfCells=100
# Initialize alpha and beta for the simulation to begin
alpha = 0.30
beta = 0.90
prob = 0.70
# Number of times to be averaged 
numberTrips = 50
# Sum of tracks occupancy to find average occupancy
finalSumTrack = np.zeros(numberOfCells)
for i in range(0,numberTrips):
	track = np.zeros(numberOfCells)
	timeLimit= 100000
	warmTime = timeLimit/2
	sumTrack = np.zeros(numberOfCells)
	for time in range(0,timeLimit):
		tempTrack = cp.copy(track)
		cellsToFilled = []
		for index in range (0,numberOfCells-1):
			if ((track[index]==1) and (track[(index+1)] == 0)):
				cellsToFilled.append(index)		
		for cell in cellsToFilled :
			randFloat = random.uniform(0,1)
			if (randFloat <= prob):
				tempTrack[cell] = 0
				tempTrack[cell+1] = 1
		if ((0 not in cellsToFilled) and (track[0]==0)):
			randFloat = random.uniform(0,1)
			if (randFloat <= alpha):
				tempTrack[0] = 1
		if ((track[numberOfCells-1]==1) and (numberOfCells-2 not in cellsToFilled)):
			randFloat = random.uniform(0,1)
			if (randFloat <= beta):
				tempTrack[numberOfCells-1] = 0
		track = cp.copy(tempTrack)
		if (time > warmTime):
			sumTrack = cp.copy(track+sumTrack)
	sumTrack = sumTrack/float(warmTime)
	finalSumTrack = cp.copy(sumTrack+finalSumTrack)
	print("Trip number is "+str(i))
finalSumTrack = finalSumTrack/float(numberTrips)
trackWithMarkedCells = [i for i in range(0,numberOfCells)]
plt.plot(trackWithMarkedCells, finalSumTrack)
plt.ylabel('Averaged occupancy')
plt.xlabel('Cell Number')
#plt.axis([0, 6, 0, 20])
axes = plt.gca()
axes.set_ylim([0.0,1.0])
plt.show()