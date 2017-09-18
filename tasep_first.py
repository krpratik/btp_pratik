import random

# Define the number of cells on the the circular track (Basically the length of the circular Track)
numberOfCells=100
# initialize vehicle density 
vehicleDensity = 0.1 
finalFluxList=[]
while (vehicleDensity <= 1):
	#Define the number of vehciles on the circular track
	numberOfCars= int(vehicleDensity*numberOfCells)
	# Now Positioning cars into cells
	# Randomly select the positions of the cars onto the tracks
	trackWithMarkedCells = [i for i in range(0,numberOfCells)]
	# Number of Iterations for a particular number of Vehicle
	numIteration = 10
	totalFlux = 0
	for i in range(0,numIteration):
		# Initialize the cells of the road. We will mark the empty cells by O and filled by 1
		# Initializing all the cells with 0 (empty cells)
		track = [0]*numberOfCells
		cellsToFilled = random.sample(trackWithMarkedCells, numberOfCars)
		for cell in cellsToFilled :
			track[cell] = 1
		# Particle based approach with series updating (Not parallel update)
		# Set time (Number of updates) 
		timeLimit= 2000*numberOfCells
		fluxCount = 0
		for time in range(0,timeLimit) :
			# Randomly select the particle which needs to be updated
			particleToBeUpdated = random.sample(cellsToFilled, 1)[0]
			if track[(particleToBeUpdated+1)%numberOfCells] == 0:
				track[(particleToBeUpdated+1)%numberOfCells] = 1
				track[particleToBeUpdated] = 0
				index = cellsToFilled.index(particleToBeUpdated)
				cellsToFilled[index]= (particleToBeUpdated+1)%numberOfCells
				if (particleToBeUpdated == numberOfCells/2):
					fluxCount = fluxCount+1
		totalFlux = totalFlux + fluxCount/float(timeLimit)
		print(i)
	finalFlux = totalFlux/float(numIteration)
	finalFluxList.append([vehicleDensity,finalFlux])
	vehicleDensity = vehicleDensity+0.1

print (finalFluxList)

# Now parallel updatation approach
