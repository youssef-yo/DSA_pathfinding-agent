import heapq
from .reconstructPath import reconstructPath
from collections import defaultdict 
from models.state import State

def aStarBidirectional(graph, heuristic, init, goal, maxLengthNewAgent, startTime):
    # initialize the open and closed sets
    openListInit = []
    closedSetInit = set() # set o tuples (node, time)
    stateDictInit = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state

    stateDictInit[(init, startTime)] = State(init, startTime, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(openListInit, (stateDictInit[(init, startTime)].f, stateDictInit[(init, startTime)]))
    
    # initialize the open and closed sets
    openListGoal = []
    closedSetGoal = set() # set o tuples (node, time)
    stateDictGoal = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state

    stateDictGoal[(init, startTime)] = State(init, startTime, None, 0, heuristic[(init, goal)])

    # push the initial node into the open set with its f-score
    heapq.heappush(openListGoal, (stateDictGoal[(init, startTime)].f, stateDictGoal[(init, startTime)]))
    
    while openListInit and openListGoal:
        #INIT side

        # get the node with the lowest f-score from the open set
        currentStateInit = heapq.heappop(openListInit)[1]
        closedSetInit.add((currentStateInit.getNode(), currentStateInit.getTime()))
        # closedSetInit[currentStateInit.getNode()] = (currentStateInit.getTime(), currentStateInit.getParentNode())
        if (currentStateInit.getNode(), currentStateInit.getTime()) in closedSetGoal:
            # reconstruct the path from the initial node to the goal
            pathStart = reconstructPath(init, currentStateInit.getNode(), stateDictInit, startTime, currentStateInit.getTime())
            pathGoal = reconstructPath(goal, currentStateGoal.getNode(), stateDictGoal, startTime, currentStateGoal.getTime())

            t = currentStateGoal.getTime() - 1
            currentT = currentStateInit.getTime() - 1
            while pathGoal.existMoveAtTimeT(t):
                move = pathGoal.getMove(t)
                pathStart.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                t -= 1
                currentT += 1
            return pathStart

        if currentStateInit.getTime() < maxLengthNewAgent:
            # explore the neighbors of the current node
            for edge in graph.getNeighbors(currentStateInit.getNode()):
                
                neighbor = edge.dst
                weight = edge.weight

                if (neighbor, currentStateInit.getTime() + 1) in closedSetInit:
                    continue
                
                currentGscore = currentStateInit.g + weight

                updateStateDict(goal, stateDictInit, heuristic, currentStateInit, neighbor, currentGscore)
                                
                if (neighbor, currentStateInit.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openListInit]:
                    heapq.heappush(openListInit, (stateDictInit[(neighbor, currentStateInit.getTime() + 1)].f, stateDictInit[(neighbor, currentStateInit.getTime() + 1)]))
        
        #GOAL side
        # get the node with the lowest f-score from the open set
        currentStateGoal = heapq.heappop(openListInit)[1]
        closedSetGoal.add((currentStateGoal.getNode(), currentStateGoal.getTime()))
        # closedSetGoal[currentStateGoal.getNode()] = (currentStateGoal.getTime(), currentStateGoal.getParentNode())
        if (currentStateGoal.getNode(), currentStateGoal.getTime()) in closedSetInit:
            # reconstruct the path from the initial node to the goal
            pathGoal = reconstructPath(goal, currentStateGoal.getNode(), stateDictGoal, startTime, currentStateGoal.getTime())
            pathStart = reconstructPath(init, currentStateGoal.getNode(), stateDictInit, startTime, currentStateInit.getTime())

            t = currentStateGoal.getTime() - 1
            currentT = currentStateInit.getTime() - 1
            while pathStart.existMoveAtTimeT(t):
                move = pathStart.getMove(t)
                pathGoal.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                t -= 1
                currentT += 1
            return pathGoal
        
        if currentStateGoal.getTime() < maxLengthNewAgent:
            # explore the neighbors of the current node
            for edge in graph.getNeighbors(currentStateGoal.getNode()):
                
                neighbor = edge.dst
                weight = edge.weight

                if (neighbor, currentStateGoal.getTime() + 1) in closedSetGoal:
                    continue
                
                currentGscore = currentStateGoal.g + weight

                updateStateDict(goal, stateDictGoal, heuristic, currentStateGoal, neighbor, currentGscore)
                                
                if (neighbor, currentStateGoal.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openListInit]:
                    heapq.heappush(openListInit, (stateDictGoal[(neighbor, currentStateGoal.getTime() + 1)].f, stateDictGoal[(neighbor, currentStateGoal.getTime() + 1)]))



def updateStateDict(goal, stateDict, heuristic, currentState, neighbor, currentGscore):
    # Is the neighbor at time t+1 already in the stateDict?
    # If not, add it to the stateDict
    if not stateDict.get((neighbor, currentState.getTime() + 1), None):        
        stateDict[(neighbor, currentState.getTime()+1)] = State(neighbor, currentState.getTime() + 1, None, float('inf'), float('inf'))

    if currentGscore < stateDict[(neighbor, currentState.getTime()+1)].g:
        stateDict[(neighbor, currentState.getTime() + 1)].parentNode = currentState.getNode()
        stateDict[(neighbor, currentState.getTime() + 1)].g = currentGscore
        stateDict[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goal)]


def findBidirectional(graph, heuristic, init, goal, maxLengthNewAgent, startTime):
    # initialize the open and closed sets for both directions
    openList_start = []
    openList_goal = []
    closedSet_start = set() # set o tuples (node, time) for start direction
    closedSet_goal = set() # set o tuples (node, time) for goal direction
    stateDict_start = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state for start direction
    stateDict_goal = defaultdict(State) # list of states, we use it instead of P. Each state has a pointer to parent state for goal direction

    # Initialize start direction from init
    stateDict_start[(init, startTime)] = State(init, startTime, None, 0, heuristic[(init, goal)])
    heapq.heappush(openList_start, (stateDict_start[(init, startTime)].f, stateDict_start[(init, startTime)]))

    # Initialize goal direction from goal
    stateDict_goal[(goal, startTime)] = State(goal, startTime, None, 0, heuristic[(goal, init)])
    heapq.heappush(openList_goal, (stateDict_goal[(goal, startTime)].f, stateDict_goal[(goal, startTime)]))
    
    while openList_start and openList_goal:
        # Explore from start to goal
        current_state_start = heapq.heappop(openList_start)[1]
        closedSet_start.add((current_state_start.getNode(), current_state_start.getTime()))

        if (current_state_start.getNode(), current_state_start.getTime()) in closedSet_goal:
            pathStart = reconstructPath(init, current_state_start.getNode(), stateDict_start, startTime, current_state_start.getTime())
            pathGoal = reconstructPath(goal, current_state_start.getNode(), stateDict_goal, startTime, current_state_start.getTime())

            t = current_state_goal.getTime() - 1
            currentT = current_state_start.getTime() - 1
            while pathGoal.existMoveAtTimeT(t):
                move = pathGoal.getMove(t)
                pathStart.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                t -= 1
                currentT += 1
            for state in stateDict_goal:
                    stateDict_start[state] = stateDict_goal[state]
                    
            closedSet_start.update(closedSet_goal)
            return pathStart, stateDict_start, closedSet_start
        
        if current_state_start.getTime() < maxLengthNewAgent:
            # Explore the neighbors of the current node in start direction
            for edge in graph.getNeighbors(current_state_start.getNode()):
                neighbor = edge.dst
                weight = edge.weight

                if (neighbor, current_state_start.getTime() + 1) in closedSet_start:
                    continue
                
                current_g_score = current_state_start.g + weight
                updateStateDict(goal, stateDict_start, heuristic, current_state_start, neighbor, current_g_score)
                                
                if (neighbor, current_state_start.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openList_start]:
                    heapq.heappush(openList_start, (stateDict_start[(neighbor, current_state_start.getTime() + 1)].f, stateDict_start[(neighbor, current_state_start.getTime() + 1)]))

        # Explore from goal to start
        current_state_goal = heapq.heappop(openList_goal)[1]
        closedSet_goal.add((current_state_goal.getNode(), current_state_goal.getTime()))

        if (current_state_goal.getNode(), current_state_goal.getTime()) in closedSet_start:
            pathStart = reconstructPath(init, current_state_goal.getNode(), stateDict_start, startTime, current_state_goal.getTime())
            pathGoal = reconstructPath(goal, current_state_goal.getNode(), stateDict_goal, startTime, current_state_goal.getTime())

            t = current_state_start.getTime() - 1
            currentT = current_state_goal.getTime() - 1
            while pathStart.existMoveAtTimeT(t):
                move = pathStart.getMove(t)
                pathGoal.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                t -= 1
                currentT += 1
            for state in stateDict_start:
                    stateDict_goal[state] = stateDict_start[state]
                    
            closedSet_goal.update(closedSet_start)
            return pathGoal, stateDict_goal, closedSet_goal
        
        if current_state_goal.getTime() < maxLengthNewAgent:
            # Explore the neighbors of the current node in goal direction
            for edge in graph.getNeighbors(current_state_goal.getNode()):
                neighbor = edge.dst
                weight = edge.weight

                if (neighbor, current_state_goal.getTime() + 1) in closedSet_goal:
                    continue
                
                current_g_score = current_state_goal.g + weight
                updateStateDict(init, stateDict_goal, heuristic, current_state_goal, neighbor, current_g_score)
                                
                if (neighbor, current_state_goal.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in openList_goal]:
                    heapq.heappush(openList_goal, (stateDict_goal[(neighbor, current_state_goal.getTime() + 1)].f, stateDict_goal[(neighbor, current_state_goal.getTime() + 1)]))

    return None, None, None
