from models.state import State
from models.path import Path
from collections import defaultdict 
from .reconstructPath import reconstructPath
from .heuristic import computeHeuristic
import heapq

from .relaxedPath import aStarBidirectional, findBidirectional



def reachGoal(instance, relaxedPlan = False):
    """"
    Find a path from the initial node to the goal node
    Return the path and the list of states
    """
    # Note that instance.getGrid() could be None
    graph = instance.getGraph()
    paths = instance.getPaths()
    init = instance.getInit()
    goal = instance.getGoal()
    maxLengthNewAgent = instance.getMaxLengthNewAgent()
    maxTimeGoalOccupied = instance.getMaxTimeGoalOccupied()

    # initialize the open and closed sets
    openList = []
    closedSet = set() # set o tuples (node, time)
    stateDict = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state
    heuristic = computeHeuristic(graph, goal)

    stateDict[(init, 0)] = State(init, 0, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(openList, (stateDict[(init, 0)].f, stateDict[(init, 0)]))

    #check for wait
    if maxTimeGoalOccupied + 1 > maxLengthNewAgent:
        return None, None, None
    
    while openList:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(openList)[1]
        closedSet.add((currentState.getNode(), currentState.getTime()))

        # check if the goal will be occupied in the future, if so take another state
        if currentState.getNode() == goal and currentState.getTime() <= maxTimeGoalOccupied + 1:
            newCurrentState = heapq.heappop(openList)[1]
            closedSet.add((newCurrentState.getNode(), newCurrentState.getTime()))

            currentState = newCurrentState
        elif currentState.getNode() == goal and currentState.getTime() > maxTimeGoalOccupied + 1:
            return reconstructPath(init, goal, stateDict, 0, currentState.getTime()), stateDict, closedSet

        if relaxedPlan:
            #compute realxed plan
            bidHeuristic = {**computeHeuristic(graph, currentState.getNode()),  **heuristic}

            relaxedPath, relaxedStateList, relaxedClosedSet = findBidirectional(graph, bidHeuristic, currentState.getNode(), goal, maxLengthNewAgent - currentState.getTime(), currentState.getTime())   
            # relaxedPath, relaxedStateList, relaxedClosedSet = findRelaxedPath(graph, heuristic, currentState.getNode(), goal, maxLengthNewAgent - currentState.getTime(), currentState.getTime())
            if relaxedPath and relaxedPath.isPathCollisionFree(paths, currentState.getTime(), maxTimeGoalOccupied):
                path = reconstructPath(init, currentState.getNode(), stateDict, 0, currentState.getTime())

                for state in relaxedStateList:
                    stateDict[state] = relaxedStateList[state]
                    
                closedSet.update(relaxedClosedSet)
                path.concatenatePaths(relaxedPath)

                return path, stateDict, closedSet

        if currentState.getTime() < maxLengthNewAgent:
            exploreNeighborhood(graph, paths, goal, openList, closedSet, stateDict, heuristic, currentState)
    return None, None, None

def exploreNeighborhood(graph, paths, goal, openList, closedSet, stateDict, heuristic, currentState):
    """"
    Explore the neighbors of the current node    
    """
    # for neighbor, weight in graph.getNeighbors(currentState.getNode()):
    for edge in graph.getNeighbors(currentState.getNode()):
        neighbor = edge.dst
        weight = edge.weight

        if (neighbor, currentState.getTime() + 1) in closedSet:
            continue

        traversable = True
                
        if Path.checkIllegalMove(neighbor, paths, currentState.getNode(), currentState.getTime()):
            traversable = False
                
        if traversable:
            currentGscore = currentState.g + weight

            updateStateDict(goal, stateDict, heuristic, currentState, neighbor, currentGscore)
                    
            if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openList]:
                heapq.heappush(openList, (stateDict[(neighbor, currentState.getTime() + 1)].f, stateDict[(neighbor, currentState.getTime() + 1)]))

def updateStateDict(goal, stateDict, heuristic, currentState, neighbor, currentGscore):
    # Is the neighbor at time t+1 already in the stateDict?
    # If not, add it to the stateDict
    if not stateDict.get((neighbor, currentState.getTime() + 1), None):        
        stateDict[(neighbor, currentState.getTime()+1)] = State(neighbor, currentState.getTime() + 1, None, float('inf'), float('inf'))

    if currentGscore < stateDict[(neighbor, currentState.getTime()+1)].g:
        stateDict[(neighbor, currentState.getTime() + 1)].parentNode = currentState.getNode()
        stateDict[(neighbor, currentState.getTime() + 1)].g = currentGscore
        stateDict[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]

def findRelaxedPath(graph, heuristic, init, goal, maxLengthNewAgent, startTime):
    # initialize the open and closed sets
    openList = []
    closedSet = set() # set o tuples (node, time)
    stateDict = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state

    stateDict[(init, startTime)] = State(init, startTime, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(openList, (stateDict[(init, startTime)].f, stateDict[(init, startTime)]))
    
    while openList:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(openList)[1]
        closedSet.add((currentState.getNode(), currentState.getTime()))

        if currentState.getNode() == goal:
            # reconstruct the path from the initial node to the goal
            return reconstructPath(init, goal, stateDict, startTime, currentState.getTime()), stateDict, closedSet

        if currentState.getTime() < maxLengthNewAgent:
            # explore the neighbors of the current node
            for edge in graph.getNeighbors(currentState.getNode()):
                
                neighbor = edge.dst
                weight = edge.weight

                if (neighbor, currentState.getTime() + 1) in closedSet:
                    continue
                
                currentGscore = currentState.g + weight

                updateStateDict(goal, stateDict, heuristic, currentState, neighbor, currentGscore)
                                
                if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openList]:
                    heapq.heappush(openList, (stateDict[(neighbor, currentState.getTime() + 1)].f, stateDict[(neighbor, currentState.getTime() + 1)]))
    return None, None, None
