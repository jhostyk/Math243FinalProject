### Joseph Hostyk

### Math 243

### Setup of classes


import copy
import numpy as np


class Graph(object):

	def __init__(self, numNodes):
		self.genotypes = []
		self.numNodes = numNodes
		# Weights is a matrix
		self.weights = None
		self.selectionMatrix = None
		self.genotypeCounts = {}

	def __str__(self):
		s = ""
		for i, geno in enumerate(self.genotypes):
			s += "{}. Neighbors: ".format(geno)
			for j in range(self.numNodes):
				if i != j and self.weights[i][j] != 0.0:
					s += self.genotypes[j] + ", "
			s += "\n"
		return s


	# # Not sure if this is still necessary; maybe implement later.
	# def addNode(self, node, neighbors):
	# 	return

	# Helpful to just have the frequencies in a dict. Call this after
	# the genotypes array is initialized.
	def calculateGenotypeFrequencies(self):
		for g in self.genotypes:
			if g not in self.genotypeCounts:
				self.genotypeCounts[g] = 0
			self.genotypeCounts[g] += 1

	def replaceNode(self, oldIndex, newGenotype):
		self.genotypeCounts[self.genotypes[oldIndex]] -= 1
		self.genotypes[oldIndex] = newGenotype
		if newGenotype not in self.genotypeCounts:
			self.genotypeCounts[newGenotype] = 0
		self.genotypeCounts[newGenotype] += 1		


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
		self.calculateGenotypeFrequencies()

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
		self.calculateGenotypeFrequencies()


class Bipartite(Graph):
	def __init__(self, numNodes, fitness, deathrate, genotype):
		Graph.__init__(self)



# if __name__ == '__main__':
# 	return	



