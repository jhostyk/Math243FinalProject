### Joseph Hostyk

### Math 243

### Setup of classes


import copy
import numpy as np


fitness = {"AA" = 0.5, "AD" = 0.5, "DD" = 0.5}
deathRates = {"AA" = 0.8, "AD" = 0.8, "DD" = 0.8}

class Graph(object):

	def __init__(self):
		self.genotypes = []
		self.totalNodes = None
		self.totalFitness = 0.0
		self.weights = np.matrix()
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
		Graph.__init__(self)
		

		for r in range(rows):
			for c in range(cols):
				neighbors = []
				# Being careful of the edges:
				if r != 0:
					neighbors.append((self.lattice[r-1][c], 1))
				if r != rows-1:
					neighbors.append((self.lattice[r+1][c], 1))
				if c != 0:
					neighbors.append((self.lattice[r][c-1], 1))
				if c != cols-1:
					neighbors.append((self.lattice[r][c+1], 1))
				self.addNode(self.lattice[r][c], neighbors)

		# Now should have normal Graph dict
		self.calculateTotalFitness()

	def __str__(self):
		s = ""
		for row in self.lattice:
			for node in row:
				s += str(node) + "\n"
		return s

class FullyConnected(Graph):
	def __init__(self, numNodes, fitness, deathrate, genotype):
		Graph.__init__(self)
		tempArray = []
		for i in range(numNodes):
			tempArray.append((Node(fitness, deathrate, genotype),1))

		# Build the graph:
		for node in tempArray:
			neighbors = [n for n in tempArray]
			neighbors.remove(node)
			self.addNode(node, neighbors)


class Bipartite(Graph):
	def __init__(self, numNodes, fitness, deathrate, genotype):
		Graph.__init__(self)


if __name__ == '__main__':
	a = np.matrix([[1,2],[3,4]])
	print np.multiply(a,a)
