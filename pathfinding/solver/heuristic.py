import math

def bfs(v, g, graph):
    visited = set()
    queue = []
    queue.append((v, 0))

    while queue:
        node, distance = queue.pop(0)
        if node == g:
            return distance

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph.getNeighbors(node):
                queue.append((neighbor, distance + 1))
    return float('inf')

def diagonalDistance(v, g):
    dx = abs(v[0] - g[0])
    dy = abs(v[1] - g[1])
    return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

def computeHeuristic(graph, goal):
    # as heuristic use BFS to fine the shortest path from init to goal for each agent. 
    h = dict() # key = vertex v, goal g, value = bfs(v, g)
    for v in graph.adjacent.keys():
        # h[(v, goal)] = bfs(v, goal, graph)
        h[(v, goal)] = diagonalDistance(v, goal)

    return h