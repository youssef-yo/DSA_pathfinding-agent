from models.state import State
from generator import pathsGenerator
from collections import defaultdict 
from .reconstructPath import reconstructPath
from .heuristic import computeHeuristic
import heapq
     
def reachGoal(graph, paths, init, goal, maxLengthNewAgent):
    # initialize the open and closed sets
    open_set = []
    closed_set = set() # set o tuples (node, time)
    stateList = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state
    heuristic = computeHeuristic(graph, goal)

    stateList[(init, 0)] = State(init, 0, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(open_set, (stateList[(init, 0)].f, stateList[(init, 0)]))

    #check for wait
    maxTimeGoalOccupied = -1
    for path in paths:
        for time, move in path.getMoves().items():
            if move.dst == goal:
                maxTimeGoalOccupied = max(maxTimeGoalOccupied, time)
    if maxTimeGoalOccupied + 1 > maxLengthNewAgent:
        return None, None
    
    while open_set:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(open_set)[1]
        closed_set.add((currentState.getNode(), currentState.getTime()))

        # check if the goal will be occupied in the future, if so take another state
        #TODO: prefer self loop instead of other moves
        if currentState.getNode() == goal and currentState.getTime() <= maxTimeGoalOccupied + 1:
            newCurrentState = heapq.heappop(open_set)[1]
            closed_set.add((newCurrentState.getNode(), newCurrentState.getTime()))

            currentState = newCurrentState

        # check if the current node is the goal
        if currentState.getNode() == goal:
            # reconstruct the path from the initial node to the goal
            return reconstructPath(init, goal, stateList, 0, currentState.getTime()), stateList

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
                        stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]
                    
                    #TODO: make efficient
                    if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                        heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
    return None, None

def findRelaxedPath(graph, heuristic, init, goal, maxLengthNewAgent, startTime):
    # initialize the open and closed sets
    open_set = []
    closed_set = set() # set o tuples (node, time)
    stateList = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state

    stateList[(init, startTime)] = State(init, startTime, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(open_set, (stateList[(init, startTime)].f, stateList[(init, startTime)]))
    
    while open_set:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(open_set)[1]
        closed_set.add((currentState.getNode(), currentState.getTime()))

        if currentState.getNode() == goal:
            # reconstruct the path from the initial node to the goal
            return reconstructPath(init, goal, stateList, startTime, currentState.getTime()), stateList

        if currentState.getTime() < maxLengthNewAgent:
            # explore the neighbors of the current node
            for neighbor, weight in graph.getNeighbors(currentState.getNode()):

                if (neighbor, currentState.getTime() + 1) in closed_set:
                    continue
                
                currentGscore = currentState.g + weight

                if not stateList.get((neighbor, currentState.getTime() + 1), None):
                    stateList[(neighbor, currentState.getTime()+1)] = State(neighbor, currentState.getTime() + 1, None, float('inf'), float('inf'))

                if currentGscore < stateList[(neighbor, currentState.getTime()+1)].g:
                    stateList[(neighbor, currentState.getTime() + 1)].parentNode = currentState.getNode()
                    stateList[(neighbor, currentState.getTime() + 1)].g = currentGscore
                    stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]
                
                #TODO: make efficient
                if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                    heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
    return None, None

def reachGoalV2(graph, paths, init, goal, maxLengthNewAgent):
    # initialize the open and closed sets
    open_set = []
    closed_set = set() # set o tuples (node, time)
    stateList = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state
    heuristic = computeHeuristic(graph, goal)

    stateList[(init, 0)] = State(init, 0, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(open_set, (stateList[(init, 0)].f, stateList[(init, 0)]))

    #check for wait
    maxTimeGoalOccupied = -1
    for path in paths:
        for time, move in path.getMoves().items():
            if move.dst == goal:
                maxTimeGoalOccupied = max(maxTimeGoalOccupied, time)
    if maxTimeGoalOccupied + 1 > maxLengthNewAgent:
        return None, None
    
    while open_set:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(open_set)[1]
        closed_set.add((currentState.getNode(), currentState.getTime()))

        # check if the goal will be occupied in the future, if so take another state
        #TODO: prefer self loop instead of other moves
        if currentState.getNode() == goal and currentState.getTime() <= maxTimeGoalOccupied + 1:
            newCurrentState = heapq.heappop(open_set)[1]
            closed_set.add((newCurrentState.getNode(), newCurrentState.getTime()))

            currentState = newCurrentState

        # check if the current node is the goal
        if currentState.getNode() == goal:
            # reconstruct the path from the initial node to the goal
            return reconstructPath(init, goal, stateList, 0, currentState.getTime()), stateList
        
        #compute realxed plan   
        relaxedPath, relaxedStateList = findRelaxedPath(graph, heuristic, currentState.getNode(), goal, maxLengthNewAgent - currentState.getTime(), currentState.getTime())
        if relaxedPath and pathsGenerator.isPathCollisionFree(relaxedPath, paths, currentState.getTime(), maxTimeGoalOccupied):
            path = reconstructPath(init, goal, stateList, 0, currentState.getTime())

            for state in relaxedStateList:
                stateList[state] = relaxedStateList[state]

            path.concatenatePaths(relaxedPath)

            return path, stateList
        #if collision free
            #return reconstructPath + pi

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
                        stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]
                    
                    #TODO: make efficient
                    if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                        heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
    return None, None