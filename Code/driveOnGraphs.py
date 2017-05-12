### Joseph Hostyk

### Math 243

### driveOnGraphs: runs the simulations

import copy
import sys
import numpy as np

from graphs import *

from plotlySignIn import *

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

def runGeneration(G):
	N = G.numNodes
	totalFitness = findTotalFitness(G.genotypes)
	matingProbs = {}
	# Go through the upper-right triangle of the matrix:
	for i in range(N):
		for j in range(i+1, N):
			matingProb = fitness[G.genotypes[i]]*fitness[G.genotypes[j]]*G.weights[i][j]
			matingProbs[(i, j)] = matingProb

	# Now we have a dictionary that matches every pair with its probability of being a mate.
	# Not normalized probability though.

	# Choose a random pair:

	normalizedMatingProbs = np.array(matingProbs.values())/sum(matingProbs.values())
	index = np.random.choice(range(len(matingProbs.keys())), size=1, p = normalizedMatingProbs)[0]
	iRandMate, jRandMate = matingProbs.keys()[index]

	childGenotype = matingOutcome(G.genotypes[iRandMate], G.genotypes[jRandMate])

	# Find the neighbor to die:
	deathProbs = {}

	possibleForDeath = range(N)

	# Can't replace the parents.
	possibleForDeath.remove(iRandMate)
	possibleForDeath.remove(jRandMate)

	for k in possibleForDeath:
		deathProbs[k] = deathRates[G.genotypes[k]] * (G.weights[iRandMate][k] + G.weights[jRandMate][k])
	normalizedDeathProbs = np.array(deathProbs.values())/sum(deathProbs.values())
	toDie = np.random.choice(possibleForDeath, size=1, p = normalizedDeathProbs)[0]
	G.replaceNode(toDie, childGenotype)


	return

# Taking in a dict where the keys are diploid genotypes, e.g. "AD".
# We want to see how many many "D"s there are.
def getDriveAlleleFreq(G):
	freq = 0.0
	for geno in G.genotypeCounts:
		if geno == "AD":
			freq += 1 * G.genotypeCounts[geno]
		if geno == "DD":
			freq += 2 * G.genotypeCounts[geno]
	return freq/(2*G.numNodes)

def oneSimulation(G, indicesOfInitalDrive):
	# Start Drive:
	for i in indicesOfInitalDrive:
		G.replaceNode(i, "DD")
	DFreqs = []
	DFreq = -1.0
	numGens = 0
	while(DFreq != 0.0 and DFreq != 1.0):
		sys.stdout.flush()
		print "Current Gen: {}\r".format(numGens),
		numGens += 1
		runGeneration(G)
		DFreq = getDriveAlleleFreq(G)
		DFreqs.append(DFreq)
	Fixed = DFreq == 1.0
	return DFreqs, numGens, Fixed

def manySimulations(G, indicesOfInitalDrive, numSims):
	numFixed = 0.0
	arrayOfDFreqs = []
	for i in range(numSims):
		graph = copy.deepcopy(G)
		print "Sim # {}\r".format(i)
		DFreqs, numGens, Fixed = oneSimulation(graph, indicesOfInitalDrive) 		
		numFixed += Fixed
		arrayOfDFreqs.append(DFreqs)
		sys.stdout.flush()
	fixationRate = numFixed/numSims
	return fixationRate


# if __name__ == '__main__':
# 	F = FullyConnected(60)
# 	frate = manySimulations(F, [0, 1, 2], 10)
# 	print "Rate: ", frate



