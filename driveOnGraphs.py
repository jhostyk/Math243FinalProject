### Joseph Hostyk

### Math 243

### driveOnGraphs: runs the simulations

import copy
import sys

from graphs import *

import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *

py.sign_in('jhostyk', 'i9GvNlCOHgLLRsbT0Djw')

# The probability that a Driven gene produces a Driven offspring
P = 1.0

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


# def chooseRandNode(group, )

def runGeneration(Graph):
	# Go through all possible combinations 
	allProbs = np.array([node.fitness for node in Graph.graph])
	normalizedProbs = allProbs/Graph.totalFitness
	randNode = np.random.choice(Graph.graph.keys(), size=1, p = normalizedProbs)[0]

	# Now that we've chosen a random node from the graph,
	# we choose a random neighbor of that node.
	neighbors = [n for n in Graph.graph[randNode]]
	mateProbs = np.array([neighbor.fitness for neighbor in neighbors])
	normalizedProbs = mateProbs/sum(mateProbs)
	mate = np.random.choice(neighbors, size=1, p = normalizedProbs)[0]

	# We've got the two neighboring individuals. What ofspring do they produce?
	child = matingOutcome(randNode.genotype, mate.genotype)

	# We now choose one to die, from all the neighbors of both mates.
	neighbors.remove(mate)
	for neighbor in Graph.graph[mate]:
		if neighbor not in neighbors and neighbor != randNode:
			neighbors.append(neighbor)
	deathProbs = np.array([neighbor.fitness for neighbor in neighbors])
	normalizedProbs = deathProbs/sum(deathProbs)
	toDie = np.random.choice(neighbors, size=1, p = normalizedProbs)[0]

	Graph.updateNodeGenotype(toDie, child)

	return Graph.alleleCounts


def startDrive(graph, node):
	graph.updateNodeGenotype(node, "DD")
	return

# Taking in a dict where the keys are diploid genotypes, e.g. "AD".
# We want to see how many many "D"s there are.
def getDriveAlleleFreq(dic):
	freq = 0.0
	for key in dic:
		if key == "AD":
			freq += 1 * dic[key]
		if key == "DD":
			freq += 2 * dic[key]
	return freq


# def run1Simulation(G, gens):
def run1Simulation(G):
	# For Lattice:
	# startDrive(G, G.lattice[4][4])

	# For Moran:
	startDrive(G, G.graph.keys()[0])
	totalNodes = 2.0 * len(G.graph)
	DFreqs = []
	currentFreq = -1.0
	gen = 0
	# for i in range(gens):
	while(currentFreq != 0.0 and currentFreq != 1.0):
		gen += 1
		alleleCounts = runGeneration(G)
		DFreq = getDriveAlleleFreq(alleleCounts)
		currentFreq = DFreq/totalNodes
		DFreqs.append(currentFreq)
	Fixed = currentFreq == 1.0
	return DFreqs, gen, Fixed

# Repeat the array's last value so that the array is the correct length.
# We're not making copies of the arrays, so the array itself should be edited.
# (Nothing needs to be returned.) Using this for graphing.
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
	title = 'Drive Frequency. Moran Process, 100 Individuals, 20 Simulations'
	layout = Layout(title = title, xaxis=XAxis(autorange=True, title = 'Generations'),yaxis=YAxis(autorange=True, title = "Drive Allele Frequency"),showlegend = False)
	fig = Figure(data=data, layout=layout)
	unique_url = py.plot(fig, filename=title)
	return

def runSimulations(reps):
	freqsArray = []
	gensArray = []
	numFixed = 0.0
	for i in range(reps):
		sys.stdout.write("Simulation #{}\r".format(i))
		G = FullyConnected(100, 0.5, "AA")

		# G = Lattice(10,10)
		freqs, gen, fixed = run1Simulation(G)
		# freqsArray.append(freqs)
		# gensArray.append(gen)
		numFixed += fixed
		sys.stdout.flush()
	print 

	fixationRate = numFixed/reps
	print "Fixation Rate: ", fixationRate
	# Manage the results:
	# length = max(gensArray)
	# for array in freqsArray:
	# 	extendArray(array, length)
	# plotFreqs(freqsArray)
	return



if __name__ == '__main__':

	# # Testing nodes:
	# a = Node(1.0, "W")
	# b = Node(2.0, "D")
	# c = Node(3.0, "R")

	# print a
	# dic = {a: [b,c]}	
	# dic[b] = a
	# a.fitness = 4.0
	# print a.fitness
	# print dic[b].fitness
	# for x in dic.keys():
	# 	print x.fitness
	# print dic[b].fitness

	# # Testing graph:
	# a = Node(1.0, "W")
	# b = Node(2.0, "D")
	# c = Node(3.0, "R")
	# A = Graph()
	# A.addNode(a, [b,c])
	# A.addNode(b, [c])
	# A.addNode(c, [a])

	# A.calculateTotalFitness()
	# print A.totalFitness


	# # Testing Lattice:
	# L = Lattice(2,2)
	# print L
	# print L.totalFitness


	# Testing random choice:
	# L = Lattice(2,2)
	# print randNode.coords


	# # Test Mating Outcome:
	# assert(matingOutcome("AA", "AA") == "AA")
	# assert(matingOutcome("DD", "DD") == "DD")
	

	# Test generation:
	# L = Lattice(4,4)
	# print L.alleleCounts

	# # runGeneration(L)

	# # # print L

	# startDrive(L, L.lattice[1][1])
	# print L.alleleCounts

	# print L
	# for i in range(50):
	# 	runGeneration(L)
	# 	print L.alleleCounts
	# # print L

	# # Test extendArray:
	# a = [0.3, 0.4, 0.6, 0.6, 0.8, 1.0]
	# extendArray(a, 20)
	# print a
	# print len(a)


	# Test Moran Process (Fully-Connected)
	# F = FullyConnected(100, 0.5, "AA")
	# runSimulations(F, 3)
	runSimulations(50)



