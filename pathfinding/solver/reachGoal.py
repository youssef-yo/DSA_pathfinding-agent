from models.state import State
import math
from generator import pathsGenerator
from collections import defaultdict 
from .reconstructPath import reconstructPath
import heapq

def start(graph, paths, init, goal, maxLengthNewAgent):
    print(" ------------- ")
    print("NEW AGENT (init, goal): (", init, ", ", goal, ")")

    path, stateList = reachGoal(graph, paths, init, goal, maxLengthNewAgent)

    if not path:
        print("No path found for new agent")
        return None
    else:
        print("!!!! Path found for new agent")
        path.printPath()
        
        return path, stateList
        
def reachGoal(graph, paths, init, goal, maxLengthNewAgent):

    def calculateHeuristic(graph):
        # implement BFS algorithm
        # calculate minimum distance from vertex v to goal g
        def bfs(v, g):
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

        # as heuristic use BFS to fine the shortest path from init to goal for each agent. 
        h = dict() # key = vertex v, goal g, value = bfs(v, g)
        for v in graph.adjacent.keys():
            # h[(v, goal)] = bfs(v, goal)
            h[(v, goal)] = diagonalDistance(v, goal)

        return h
        

    def a_star(graph, paths, init, goalNode):
        # initialize the open and closed sets
        open_set = []
        closed_set = set() # set o tuples (node, time)
        stateList = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state
        heuristic = calculateHeuristic(graph)

        stateList[(init, 0)] = State(init, 0, None, 0, heuristic[(init, goalNode)])

        # push the initial node into the open set with its f-score
        heapq.heappush(open_set, (stateList[(init, 0)].f, stateList[(init, 0)]))

        #check for wait
        maxTimeGoalOccupied = -1
        for path in paths:
            for time, move in path.getMoves().items():
                if move.dst == goalNode:
                    maxTimeGoalOccupied = max(maxTimeGoalOccupied, time)
        if maxTimeGoalOccupied + 1 > maxLengthNewAgent:
            return None 
        
        while open_set:
            # get the node with the lowest f-score from the open set
            currentState = heapq.heappop(open_set)[1]
            closed_set.add((currentState.getNode(), currentState.getTime()))

            # check if the goal will be occupied in the future, if so take another state
            #TODO: prefer self loop instead of other moves
            if currentState.getNode() == goalNode and currentState.getTime() <= maxTimeGoalOccupied + 1:
                newCurrentState = heapq.heappop(open_set)[1]
                closed_set.add((newCurrentState.getNode(), newCurrentState.getTime()))

                currentState = newCurrentState

            # check if the current node is the goal
            if currentState.getNode() == goalNode:
                # reconstruct the path from the initial node to the goal
                return reconstructPath(init, goalNode, stateList, currentState.getTime()), stateList

            if currentState.getTime() < maxLengthNewAgent:
                # explore the neighbors of the current node
                for neighbor, weight in graph.getNeighbors(currentState.getNode()):

                    if (neighbor, currentState.getTime() + 1) in closed_set:
                        continue

                    traversable = True
                    
                    # TODO: da creare un metodo apposito in una classe utils magari
                    if pathsGenerator.checkIllegalMove(neighbor, paths, currentState.getNode(), currentState.getTime()):
                        traversable = False
                    
                    if traversable:
                        currentGscore = currentState.g + weight

                        if not stateList.get((neighbor, currentState.getTime() + 1), None):
                            stateList[(neighbor, currentState.getTime()+1)] = State(neighbor, currentState.getTime() + 1, None, float('inf'), float('inf'))

                        if currentGscore < stateList[(neighbor, currentState.getTime()+1)].g:
                            stateList[(neighbor, currentState.getTime() + 1)].parentNode = currentState.getNode()
                            stateList[(neighbor, currentState.getTime() + 1)].g = currentGscore
                            stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goalNode)]
                        
                        #TODO: make efficient
                        if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                            heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
        return None

    return a_star(graph, paths, init, goal)