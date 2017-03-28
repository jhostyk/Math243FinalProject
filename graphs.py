### Joseph Hostyk

### Math 243

### Setup of classes


import copy


# class Node(object):
class Node(object):

	def __init__(self, fitness, deathrate, genotype):
		# Fitness and deathrate are doubles
		self.fitness = fitness
		self.deathrate = deathrate
		# Can be wildgenotype, drive, reverse, immune.
		self.genotype = genotype

	def __str__(self):
		return "{}{}-{}".format(self.genotype, self.fitness, self.deathrate)

	def updateGenotype(self, newType):
		self.genotype = newType


class Graph(object):

	def __init__(self):
		# The standard graph is a dictionary of {Node: neighbors}
		# neighbors is array of [(neighbor, weightFromNodeToNeighbor)]. 
		self.graph = {}
		self.totalFitness = 0.0
		self.alleleCounts = {}

	def __str__(self):
		s = ""
		for node in self.graph:
			s += "Node {} with neighbors ".format(node)
			for neigh, weight in self.graph[node]:
				s += str(neigh) + " ({}); ".format(weight)
			s += "\n"
		return s


	def addNode(self, node, neighbors):
		self.graph[node] = neighbors
		self.totalFitness += node.fitness
		if node.genotype not in self.alleleCounts:
			self.alleleCounts[node.genotype] = 0
		self.alleleCounts[node.genotype] += 1

	def updateNodeGenotype(self, node, newGenotype):
		self.alleleCounts[node.genotype] -= 1
		node.updateGenotype(newGenotype)
		if newGenotype not in self.alleleCounts:
			self.alleleCounts[newGenotype] = 0
		self.alleleCounts[newGenotype] += 1		


	def calculateTotalFitness(self):
		totalFitness = 0.0
		for node in self.graph:
			totalFitness += node.fitness
		self.totalFitness = totalFitness
		return totalFitness

	def updateTotalFitness(self, difference):
		self.totalFitness += difference

class LatticeNode(Node):

	# Coords is [row, col]
	def __init__(self, coords, fitness, deathrate, genotype):
		Node.__init__(self, fitness, deathrate, genotype)
		self.coords = coords

	def __str__(self):
		[x,y] = self.coords
		return "{}{}({},{})".format(self.genotype, self.fitness,x,y)

class Lattice(Graph):

	def __init__(self, rows, cols):
		Graph.__init__(self)

		# Doing too much work - making both a matrix and the usual Graph dict.
		# Not sure which one should be dropped.
		self.lattice = [[0]*cols for i in range(rows)]
		fitness = 0.5
		genotype = "AA"
		for r in range(rows):
			for c in range(cols):
				self.lattice[r][c] = LatticeNode([r,c], fitness, deathrate, genotype)
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



