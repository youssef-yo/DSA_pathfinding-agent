from models.state import State
from generator import pathsGenerator
from collections import defaultdict 
from .reconstructPath import reconstructPath
from .heuristic import computeHeuristic
import heapq



def reachGoal(graph, paths, init, goal, maxLengthNewAgent, relaxedPlan = False):
    # initialize the open and closed sets
    openList = []
    closedSet = set() # set o tuples (node, time)
    stateDict = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state
    heuristic = computeHeuristic(graph, goal)

    stateDict[(init, 0)] = State(init, 0, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(openList, (stateDict[(init, 0)].f, stateDict[(init, 0)]))

    #check for wait
    maxTimeGoalOccupied = calculateMaxTimeGoalOccupied(paths, goal)
    if maxTimeGoalOccupied + 1 > maxLengthNewAgent:
        return None, None
    
    while openList:
        # get the node with the lowest f-score from the open set
        currentState = heapq.heappop(openList)[1]
        closedSet.add((currentState.getNode(), currentState.getTime()))

        # check if the goal will be occupied in the future, if so take another state
        #TODO: prefer self loop instead of other moves
        if currentState.getNode() == goal and currentState.getTime() <= maxTimeGoalOccupied + 1:
            newCurrentState = heapq.heappop(openList)[1]
            closedSet.add((newCurrentState.getNode(), newCurrentState.getTime()))

            currentState = newCurrentState

        if currentState.getNode() == goal:
            return reconstructPath(init, goal, stateDict, 0, currentState.getTime()), stateDict

        if relaxedPlan:
            #compute realxed plan   
            relaxedPath, relaxedStateList = findRelaxedPath(graph, heuristic, currentState.getNode(), goal, maxLengthNewAgent - currentState.getTime(), currentState.getTime())
            if relaxedPath and pathsGenerator.isPathCollisionFree(relaxedPath, paths, currentState.getTime(), maxTimeGoalOccupied):
                path = reconstructPath(init, goal, stateDict, 0, currentState.getTime())

                for state in relaxedStateList:
                    stateDict[state] = relaxedStateList[state]

                path.concatenatePaths(relaxedPath)

                return path, stateDict

        if currentState.getTime() < maxLengthNewAgent:
            exploreNeighborhood(graph, paths, goal, openList, closedSet, stateDict, heuristic, currentState)
    return None, None

def exploreNeighborhood(graph, paths, goal, openList, closedSet, stateDict, heuristic, currentState):
    """"
    Explore the neighbors of the current node    
    """
    for neighbor, weight in graph.getNeighbors(currentState.getNode()):
        if (neighbor, currentState.getTime() + 1) in closedSet:
            continue

        traversable = True
                
        if pathsGenerator.checkIllegalMove(neighbor, paths, currentState.getNode(), currentState.getTime()):
            traversable = False
                
        if traversable:
            currentGscore = currentState.g + weight

            updateStateDict(goal, stateDict, heuristic, currentState, neighbor, currentGscore)
                    
            #TODO: make efficient
            if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openList]:
                heapq.heappush(openList, (stateDict[(neighbor, currentState.getTime() + 1)].f, stateDict[(neighbor, currentState.getTime() + 1)]))

def updateStateDict(goal, stateList, heuristic, currentState, neighbor, currentGscore):
    # Is the neighbor at time t+1 already in the stateList?
    # If not, add it to the stateList
    if not stateList.get((neighbor, currentState.getTime() + 1), None):        
        stateList[(neighbor, currentState.getTime()+1)] = State(neighbor, currentState.getTime() + 1, None, float('inf'), float('inf'))

    if currentGscore < stateList[(neighbor, currentState.getTime()+1)].g:
        stateList[(neighbor, currentState.getTime() + 1)].parentNode = currentState.getNode()
        stateList[(neighbor, currentState.getTime() + 1)].g = currentGscore
        stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]

def calculateMaxTimeGoalOccupied(paths, goal):
    """"
    Return the max time the goal will be occupied by any of the others agents
    """
    maxTimeGoalOccupied = -1
    for path in paths:
        for time, move in path.getMoves().items():
            if move.dst == goal:
                maxTimeGoalOccupied = max(maxTimeGoalOccupied, time)
    return maxTimeGoalOccupied

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

                updateStateDict(goal, stateList, heuristic, currentState, neighbor, currentGscore)
                                
                #TODO: make efficient
                if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                    heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
    return None, None
