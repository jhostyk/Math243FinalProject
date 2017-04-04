### Joseph Hostyk

### Math 243

### driveOnGraphs: runs the simulations

import copy
import sys

from graphs import *

import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *

import plotlySignIn
 
# The probability that a Driven gene produces a Driven offspring
P = 1.0

fitness = {"AA": 1.0, "AD": 1.0, "DD": 1.0}
deathRates = {"AA": 1.0, "AD": 1.0, "DD": 1.0}



def findTotalFitness(genotypes):
	totalFitness = 0.0
	for g in genotypes:
		totalFitness += fitness[g]
	return totalFitness

# What offspring will be produced by A and B?
def matingOutcome(A, B):

	possibleOffspring = ["DD", "AD", "AA"]

	# We use Chuck's mating-tables to find the probabilities of each offspring.
	# The array returned is the probability of DD, AD, and AA offspring respectively.
	matingTable = {
		("AA", "AA"): [0.0, 0.0, 1.0],
		("AA", "AD"): [1/2.0 * P, 1/2.0 - 1/2.0 * P, 1/2.0],
		("AA", "DD"): [P, 1- P, 0.0],
		("AD", "AD"): [1/4.0 + 1/2.0 * P, 1/2.0 - 1/2.0 * P, 1/4.0],
		("AD", "DD"): [1/2.0  + 1/2.0 * P, 1/2.0 - 1/2.0 * P, 0],
		("DD", "DD"): [1.0, 0.0, 0.0]
	}

	# The table above only includes 6 of the 9 possible matings,
	# since we don't care about order.
	# That raises errors, for ones that are in different orders.
	# (E.g. (AD,DD) is in the dic, so (DD, AD) raises an error.)
	# Not sure how to cleanly deal with that, so we just catch the error.

	try:
		probs = matingTable[(A, B)]
	except KeyError:
		probs = matingTable[(B, A)]		
	offspring = np.random.choice(possibleOffspring, size=1, p = probs)[0]
	return offspring


# Takes in the array of genotypes, and the number of individuals in the population.

def runGeneration(genotypes, weights, N):
	totalFitness = findTotalFitness(genotypes)
	matingProbs = {}
	# Go through the upper-right triangle of the matrix:
	for i in range(N):
		for j in range(i+1, N):
			matingProb = fitness[genotypes[i]]*fitness[genotypes[j]]*weights[i][j]
			matingProbs[(i, j)] = matingProb

	# Now we have a dictionary that matches every pair with its probability of being a mate.
	# Not normalized probability though.

	# Choose a random pair:

	normalizedMatingProbs = np.array(matingProbs.values())/sum(matingProbs.values())
	index = np.random.choice(range(len(matingProbs.keys())), size=1, p = normalizedMatingProbs)[0]
	iRandMate, jRandMate = matingProbs.keys()[index]

	childGenotype = matingOutcome(genotypes[iRandMate], genotypes[jRandMate])

	# Find the neighbor to die:
	deathProbs = {}

	for k in range(N):
		deathProbs[k] = deathRates[genotypes[k]]* (weights[iRandMate][k] + weights[jRandMate][k])
	normalizedDeathProbs = np.array(deathProbs.values())/sum(deathProbs.values())
	toDie = np.random.choice(range(N), size=1, p = normalizedDeathProbs)[0]

	genotypes[toDie] = childGenotype

	return genotypes

def getDriveAlleleFreq(genotypes):
	numAlleles = 0.0
	for geno in genotypes:
		if geno == "AD":
			numAlleles += 1
		if geno == "DD":
			numAlleles += 2
	return numAlleles/(2*len(genotypes))

def oneSimulation():
	# Fully-connected graph of 5 nodes:
	N = 100
	weights = [[1]*N for i in range(N)]
	genotypes = ["AA"]*N

	# Start Drive:
	genotypes[0] = "DD"

	DFreqs = []
	DFreq = -1.0
	gen = 0
	while(DFreq != 0.0 and DFreq != 1.0):
		gen += 1
		newGenotypes = runGeneration(genotypes, weights, N)
		DFreq = getDriveAlleleFreq(newGenotypes)
		DFreqs.append(DFreq)

	Fixed = DFreq == 1.0
	return DFreqs, gen, Fixed

# For graphing purposes. Want the lines to continue until the longest simulation has finished.
def extendArray(arr, length):
	curLength = len(arr)
	last = arr[curLength-1]
	for i in range(length - curLength):
		arr.append(last)
	return

def plotFreqs(arrays):
	data = []
	for array in arrays:
		line = Scatter(x=range(len(array)), y=array)
		data.append(line)
	title = 'Drive Frequency. Moran Process, 100 Individuals, 20 Simulations, 4-4-17'
	layout = Layout(title = title, xaxis=XAxis(autorange=True, title = 'Generations'),yaxis=YAxis(autorange=True, title = "Drive Allele Frequency"),showlegend = False)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)
	return

if __name__ == '__main__':
	# DFreqs, gen, Fixed = oneSimulation()
	# print "Fixed? ", Fixed
	# print "Gens: ", gen
	# print "DFreqs: ", DFreqs
	numSims = 20
	numFixed = 0.0
	arrayOfDFreqs = []
	for i in range(numSims):
		print "Sim # {}\r".format(i),
		DFreqs, gen, Fixed = oneSimulation()
		numFixed += Fixed
		arrayOfDFreqs.append(DFreqs)
		sys.stdout.flush()

	print "Fixation prob: ", numFixed/numSims

	maxLength = 0
	for array in arrayOfDFreqs:
		if len(array) > maxLength:
			maxLength = len(array)
	for array in arrayOfDFreqs:
		extendArray(array, maxLength)
	plotFreqs(arrayOfDFreqs)




