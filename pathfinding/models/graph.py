from collections import defaultdict

class Edge: 
	def __init__(self, v, w):
		self.dst = v 
		self.weight = w

	def isDestination(self, v):
		return self.dst == v
 
	def __str__(self):
		return "(" + str(self.dst) + "," + str(self.weight) + ")"
    
class Graph:
	# adjacent -> hashmap
	# key: vertex
	# value: list of tuple, where a tuple contains (dst_node, weight)
	def __init__(self) -> None:
		self.adjacent = defaultdict(list)
	
	def addEdge(self, src, dst, w):
		self.adjacent[src].append(Edge(dst, w))

	def containsVertex(self, vertex):
		return vertex in self.adjacent
	
	def getNodes(self):
		return self.adjacent.keys()

	def getNeighbors(self, vertex):
		""""
		Return a list of vertices that are adjacent to the given vertex
		"""
		return self.adjacent[vertex]

	def printGraph(self):
		for vertex in self.adjacent:
			print(vertex, end=" -> ")
			for edge in self.adjacent[vertex]:
				print(edge, end=" ")
			print()
	

			

    
