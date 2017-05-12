### Joseph Hostyk

### Math 243

### changingParameters.py: runs simulations, testing different cases.

from driveOnGraphs import *
import math
import random 

# Make the DD die more and more.
def changingDeathRate(G):
	delta = 0.1
	numSims = 50
	simulationFixationRates = []
	analyticFixationRates = []
	deathRange = np.arange(0.1, 2.0 + delta, delta)
	for d in deathRange:
		print "Death rate: ", d
		deathRates["DD"] = d
		# simulationFixationRate = manySimulations(F, numSims)
		# simulationFixationRates.append(simulationFixationRate)
		# print "simulationFixationRate: ", simulationFixationRate
		analyticFixationRate = 1 - (d/(2* P))**2 # Raised to 2 because that's the number of starting DDs.
		analyticFixationRates.append(analyticFixationRate)
	return deathRange, simulationFixationRates, analyticFixationRates


def plotDeathVsFixation(G, deathRange, simulationFixationRates, analyticFixationRates):
	print "Death range: ", deathRange
	print "simulationFixationRates: ", simulationFixationRates
	print "analyticFixationRates: ", analyticFixationRates
	simulation = Scatter(x=deathRange, y=simulationFixationRates, name = "Simulation (50 Simulations)")
	analytic = Scatter(x=deathRange, y=analyticFixationRates, name = "Analytic Solution")

	data = [simulation, analytic]
	title = 'Death Rates, Moran Process. {} Individuals.'.format(G.numNodes)
	layout = Layout(title = title, xaxis=XAxis(autorange=True, title = 'Death Rate'),yaxis=YAxis(autorange=True, title = "Fixation Rate"),showlegend = True)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)
	return	

def plotDeathVsFixationWithChangingInitialFreq(G):
	F = FullyConnected(100)
	numSims = 50
	simulationFixationRates = []
	indicesOfInitalDrive = []
	range(0,100,20)

	for i in range(G.numNodes):
		print "Initial Drive Frequency", i/float(G.numNodes)
		simulationFixationRate = manySimulations(F, indicesOfInitalDrive, numSims)
		simulationFixationRates.append(simulationFixationRate)
		print "simulationFixationRate: ", simulationFixationRate
		indicesOfInitalDrive.append(i)
	freqsOfInitalDrive = np.array(indicesOfInitalDrive)/G.numNodes
	return simulationFixationRates, freqsOfInitalDrive




	deathRange, simulationFixationRates, analyticFixationRates = changingDeathRate(F)



# For graphing purposes. Want the lines to continue until the longest simulation has finished.
def extendArray(arr, length):
	curLength = len(arr)
	last = arr[curLength-1]
	for i in range(length - curLength):
		arr.append(last)
	return

def plotFreqs(arrays):
	maxLength = 0
	for array in arrays:
		if len(array) > maxLength:
			maxLength = len(array)
	for array in arrays:
		extendArray(array, maxLength)

	data = []
	for array in arrays:
		line = Scatter(x=range(maxLength), y=array)
		data.append(line)
	title = 'Drive Frequency. Moran Process, 100 Individuals, 20 Simulations, 4-4-17'
	layout = Layout(title = title, xaxis=XAxis(autorange=True, title = 'Generations'),yaxis=YAxis(autorange=True, title = "Drive Allele Frequency"),showlegend = False)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)
	return

def changingInitialFreq(G):
	numSims = 50
	simulationFixationRates = []
	indicesOfInitalDrive = []
	for i in range(G.numNodes):
		print "Initial Drive Frequency", i/float(G.numNodes)
		simulationFixationRate = manySimulations(F, indicesOfInitalDrive, numSims)
		simulationFixationRates.append(simulationFixationRate)
		print "simulationFixationRate: ", simulationFixationRate
		indicesOfInitalDrive.append(i)
	freqsOfInitalDrive = np.array(indicesOfInitalDrive)/G.numNodes
	return simulationFixationRates, freqsOfInitalDrive

def plotInitFreqVsFixation():
	simulationFixationRate = [0.0, 0.475, 0.625, 0.95, 0.95, 0.95, 0.975, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
	errorLower = []
	errorUpper = []
	numSims = 40
	for p in simulationFixationRate:
		error = math.sqrt(p*(1-p) / numSims)
		errorLower.append(max(p-error, 0.0))
		errorUpper.append(min(p+error, 1.0))
	initDriveFreq = np.arange(0, 1.01, 0.01)
	initDriveFreq_rev = initDriveFreq[::-1]

	# errorLower = errorLower[::-1]


	simulationLine = Scatter(x=initDriveFreq, y=simulationFixationRate)
	errorLine = Scatter(x=initDriveFreq+initDriveFreq, y=errorLower+errorUpper, fill='tozerox', fillcolor='rgba(0,100,80,0.2)', line=Line(color='transparent'), showlegend=False)


	data = [simulationLine]#, errorLine]


	title = 'Fixation Rate. Moran Process, 100 Individuals, 40 Simulations, 4-16-17'
	layout = Layout(title = title, xaxis=XAxis(range=[0,1], title = 'Initial Drive Frequency'),yaxis=YAxis(autorange=True, title = "Fixation Rate"),showlegend = False)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)


def changingInitLocationOnLattice(L):
	numSims = 100
	simulationFixationRates = []
	indicesOfInitalDrive = [0]
	for initialLocation in range(L.numNodes):
		indicesOfInitalDrive[0] = initialLocation
		print "Initial Location: ", initialLocation
		simulationFixationRate = manySimulations(L, indicesOfInitalDrive, numSims)
		simulationFixationRates.append(simulationFixationRate)
		print "simulationFixationRate: ", simulationFixationRate
	return simulationFixationRates


def plotChangingInitLocation(fixRates, L):
	xs = []
	ys = []
	colors = []
	fixRatesIndex = 0
	for r in range(L.numRows):
		for c in range(L.numCols):
			xs.append(c)
			ys.append(r)
			colors.append(fixRates[fixRatesIndex])
			fixRatesIndex += 1
	data = [
	    {'x': xs, 'y': ys, 'mode': 'markers', 'marker':
	    	{'color': colors,'size': [20]*L.numNodes, 'showscale': True } }]

	title = 'Changing Drive Seed Location'
	layout = Layout(title = title)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)

def createLatticeGenotypeTimestep(L):
	genotypeXs = {}
	genotypeYs = {}
	genotypeColors = {}
	genotypesIndex = 0
	for r in range(L.numRows):
		for c in range(L.numCols):
			currentGenotype = L.genotypes[genotypesIndex]
			# If we haven't seen this genotype yet, add entries in all the dictionaries.
			if currentGenotype not in genotypeXs:
				genotypeXs[currentGenotype] = []
				genotypeYs[currentGenotype] = []
				genotypeColors[currentGenotype] = 'rgb({}, {}, {})'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
			genotypeXs[currentGenotype].append(c)
			genotypeYs[currentGenotype].append(r)
			genotypesIndex += 1
	data = []
	for genotype in genotypeXs:
		n = len(genotypeXs[genotype])
		data.append({'x': genotypeXs[genotype], 'y': genotypeYs[genotype], 'name': genotype, 'mode': 'markers', 'marker':
	    	{'color': [genotypeColors[genotype]]*n,'size': [20]*n} })

	return data



def plotLatticeGenotypeAnimation(timesteps):

	frames = []
	for t in timesteps:
		frames.append({'data': t})
	print "FRAMES"
	print frames

	data = timesteps[0]


	figure = {'data': [{'y': [0, 1, 1], 'x': [1, 0, 1], 'name': 'AA', 'marker': {'color': ['rgb(231, 47, 29)', 'rgb(231, 47, 29)', 'rgb(231, 47, 29)'], 'size': [20, 20, 20]}, 'mode': 'markers'}, {'y': [0], 'x': [0], 'name': 'DD', 'marker': {'color': ['rgb(18, 177, 47)'], 'size': [20]}, 'mode': 'markers'}],
          'layout': {'xaxis': {'range': [0, 5], 'autorange': False},
                     'yaxis': {'range': [0, 5], 'autorange': False},
                     'title': 'Start Title',
                     'updatemenus': [{'type': 'buttons',
                                      'buttons': [{'label': 'Play',
                                                   'method': 'animate',
                                                   'args': [None]}]}]
                    },
          'frames': [{'data': [{'y': [0, 1, 1], 'x': [1, 0, 1], 'name': 'AA', 'marker': {'color': ['rgb(231, 47, 29)', 'rgb(231, 47, 29)', 'rgb(231, 47, 29)'], 'size': [20, 20, 20]}, 'mode': 'markers'}, {'y': [0], 'x': [0], 'name': 'DD', 'marker': {'color': ['rgb(18, 177, 47)'], 'size': [20]}, 'mode': 'markers'}]},
                     {'data': [{'y': [1, 1], 'x': [0, 1], 'name': 'AA', 'marker': {'color': ['rgb(149, 217, 103)', 'rgb(149, 217, 103)'], 'size': [20, 20]}, 'mode': 'markers'}, {'y': [0, 0], 'x': [0, 1], 'name': 'DD', 'marker': {'color': ['rgb(195, 227, 73)', 'rgb(195, 227, 73)'], 'size': [20, 20]}, 'mode': 'markers'}]}, {'data': [{'y': [1], 'x': [0], 'name': 'AA', 'marker': {'color': ['rgb(153, 35, 77)'], 'size': [20]}, 'mode': 'markers'}, {'y': [0, 0, 1], 'x': [0, 1, 1], 'name': 'DD', 'marker': {'color': ['rgb(11, 118, 241)', 'rgb(11, 118, 241)', 'rgb(11, 118, 241)'], 'size': [20, 20, 20]}, 'mode': 'markers'}]}]}


	
	title = 'Drive. Population Animation'
	layout = Layout(title = title, updatemenus = [{'type': 'buttons',
		'buttons': [{'label': 'Play', 'method': 'animate','args': [None]}]}])
	fig = Figure(data=data, layout=layout, frames=Frames(frames))
	unique_url = py.plot(figure, filename=title)

	return

if __name__ == '__main__':
	# F = FullyConnected(100)
	# deathRange, simulationFixationRates, analyticFixationRates = changingDeathRate(F)
	# changingInitialFreq(F)
	# fixation = manySimulations(F, [], 10)

	# simulationFixationRates, indicesOfInitalDrive = changingInitialFreq(F)
	# print "simulationFixationRates", simulationFixationRates
	# print "indicesOfInitalDrive", indicesOfInitalDrive


	L = Lattice(2,2)
	# # print L.weights
	# fixRates = changingInitLocationOnLattice(L)
	# print "fixRates: ", fixRates
	# # fixRates = [0.2, 0.8, 0.4, 0.4, 0.2,  0.2, 0.2, 0.6, 0.2, 0.6, 0.6,  0.4, 0.4, 0.4, 1.0, 0.4, 0.6, 0.8, 0.4, 0.2, 0.6, 0.6, 0.6, 0.6, 0.6]
	# plotChangingInitLocation(fixRates, L)
	L.replaceNode(0, "DD")
	timestep1 = createLatticeGenotypeTimestep(L)
	L.replaceNode(1, "DD")
	timestep2 = createLatticeGenotypeTimestep(L)
	L.replaceNode(3, "DD")
	timestep3 = createLatticeGenotypeTimestep(L)
	plotLatticeGenotypeAnimation([timestep1, timestep2, timestep3])

