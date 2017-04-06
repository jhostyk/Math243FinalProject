### Joseph Hostyk

### Math 243

### Setup of classes


import copy
import numpy as np


fitness = {"AA": 1.0, "AD": 1.0, "DD": 1.0}
deathRates = {"AA": 1.0, "AD": 1.0, "DD": 0.0}

class Graph(object):

	def __init__(self, numNodes):
		self.genotypes = []
		self.numNodes = numNodes
		# Weights is a matrix
		self.weights = None
		self.selectionMatrix = None
		self.alleleCounts = {}

	def __str__(self):
		s = ""
		for geno, i in enumerate(self.genotypes):
			s += geno + ". Neighbors: "
			for j in range(self.totalNodes):
				if weights[i][j] != 0.0:
					s += self.genotypes[j]
			s += "\n"
		return s


	# # Not sure if this is still necessary; maybe implement later.
	# def addNode(self, node, neighbors):
	# 	return

	# def updateNodeGenotype(self, nodeIndex, newGenotype):
	# 	self.alleleCounts[node.genotype] -= 1
	# 	node.updateGenotype(newGenotype)
	# 	if newGenotype not in self.alleleCounts:
	# 		self.alleleCounts[newGenotype] = 0
	# 	self.alleleCounts[newGenotype] += 1		


	# def calculateTotalFitness(self):
	# 	totalFitness = 0.0
	# 	for node in self.graph:
	# 		totalFitness += node.fitness
	# 	self.totalFitness = totalFitness
	# 	return totalFitness

	# def updateTotalFitness(self, difference):
	# 	self.totalFitness += difference

class Lattice(Graph):

	def __init__(self, rows, cols):
		Graph.__init__(self, rows*cols)
		self.numRows = rows
		self.numCols = cols
		self.weights = [[0]*self.numNodes for i in range(self.numNodes)]

		self.genotypes = ["AA"]*(rows*cols)

		for r in range(rows):
			for c in range(cols):
				neighbors = []
				# Being careful of the edges:
				if r != 0:
					self.weights[r*rows+c][(r-1)*rows+c] = 1
				if r != rows -1 :
					self.weights[r*rows+c][(r+1)*rows+c] = 1
				if c != 0:
					self.weights[r*rows+c][r*rows+c -1] = 1
				if c != cols - 1:
					self.weights[r*rows+c][r*rows+c + 1] = 1

	def __str__(self):
		s = ""
		for r in range(self.numRows):
			for c in range(self.numCols):
				s += self.genotypes[r*c-1] + " "
			s += "\n"
		return s

class FullyConnected(Graph):
	def __init__(self, numNodes):
		Graph.__init__(self, numNodes)
		self.weights = [[1]*self.numNodes for i in range(self.numNodes)]
		self.genotypes = ["AA"]*(numNodes)		


class Bipartite(Graph):
	def __init__(self, numNodes, fitness, deathrate, genotype):
		Graph.__init__(self)



if __name__ == '__main__':
	

	# rows = 3
	# cols = 3
	# for r in range(rows):
	# 	for c in range(cols):
	# 		"R: {}, C: {}".format(r, c)
	# 		print "Node number: ", str(r*rows+c)
	# 		# Being careful of the edges:
	# 		if r != 0:
	# 			print "Above is ", str((r-1)*rows+c)
	# 		if r != rows -1 :
	# 			print "Below is ", str((r+1)*rows+c)
	# 		if c != 0:
	# 			print "Left is ", str(r*rows+c -1)
	# 		if c != cols - 1:
	# 			print "Right is ", str(r*rows+c + 1)


