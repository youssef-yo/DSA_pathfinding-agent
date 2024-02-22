from collections import defaultdict

class Edge: 
	def __init__(self, v, w):
		self.neighbor = v 
		self.weight = w
 
	def __str__(self):
		return "(" + str(self.neighbor) + "," + str(self.weight) + ")"
    
class Graph:
	# adjacent -> hashmap
	# key: vertex
	# value: list of tuple, where a tuple contains (dst_node, weight)
	def __init__(self) -> None:
		self.adjacent = defaultdict(list)
	
	def addEdge(self, src, dst, w):
		self.adjacent[src].append(Edge(dst, w))

	def printGraph(self):
		for vertex in self.adjacent:
			print(vertex, end=" -> ")
			for edge in self.adjacent[vertex]:
				print(edge, end=" ")
			print()
	

			

    