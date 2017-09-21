import random
from random import randint
from operator import add
import matplotlib.pyplot as plt

# Define the number of cells on the the circular track (Basically the length of the circular Track)
numberOfCells=100
# Initialize alpha and beta for the simulation to begin
alpha = 0.95
beta = 0.95

# Number of times to be averaged 
numberTrips = 200

# Sum of tracks occupancy to find average occupancy
finalSumTrack = [0]*numberOfCells
for i in range(0,numberTrips):
	# Define the number of vehciles on the circular track
	# numberOfCars= randint(0,numberOfCells)
	# Now Positioning cars into cells
	# Randomly select the positions of the cars onto the tracks
	# trackWithMarkedCells = [i for i in range(0,numberOfCells)]
	# Initialize the cells of the road. We will mark the empty cells by O and filled by 1
	# Initializing all the cells with 0 (empty cells)
	track = [0]*numberOfCells
	#cellsToFilled = random.sample(trackWithMarkedCells, numberOfCars)
	#for cell in cellsToFilled :
	#	track[cell] = 1
	# Particle based approach with series updating (Not parallel update)
	# Set time (Number of updates) 
	timeLimit= 300*numberOfCells
	sumTrack = track
	for time in range(0,timeLimit) :
		# Randomly select the particle which needs to be updated
		for car in range(0,numberOfCells):
			index = randint(0,numberOfCells-1)
			if ((index == 0) and (track[index] == 0)):
				randFloat = random.uniform(0,1)
				if (randFloat <= alpha):
					track[index] = 1
			elif ((index == 0) and (track[index] == 1)):
				if track[(index+1)] == 0:
					track[(index+1)] = 1
					track[index] = 0

			if ((index == numberOfCells-1) and (track[index] == 1)):
				randFloat = random.uniform(0,1)
				if (randFloat <= beta):
					track[index] = 0
			if (0 < index < numberOfCells-1):	
				if (track[index]==1):
					if track[(index+1)] == 0:
						track[(index+1)] = 1
						track[index] = 0
		sumTrack = map(add, sumTrack, track)
	sumTrack = [x/float(timeLimit) for x in sumTrack]
	finalSumTrack = map(add, sumTrack, finalSumTrack) 
	print("Trip number is "+str(i))
finalSumTrack = [x/float(numberTrips) for x in finalSumTrack]
trackWithMarkedCells = [i for i in range(0,numberOfCells)]
plt.plot(trackWithMarkedCells, finalSumTrack)
plt.ylabel('Averaged occupancy')
plt.xlabel('Cell Number')
#plt.axis([0, 6, 0, 20])
plt.show()