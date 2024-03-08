import random
from models.path import Path
from solver.reachGoal import reachGoal

def isPathCollisionFree(path, paths, startTime, maxTimeGoalOccupied):

    # if path is shorter than the time that the goal will be occupied, it means that it will collide
    if path.getLength() + startTime < maxTimeGoalOccupied + 1:
        return False

    for t, move in path.getMoves().items():
        if checkIllegalMove(move.dst, paths, move.src, t):
            return False
    return True

#TODO: a better way to implement and use checkIllegalMove and removeIllegalMoves
def checkIllegalMove(dst, paths, current, t):
    for p in paths: 
        pathEnded = False

        if t not in p.getMoves():
            pathEnded = True

        if pathEnded:
            if dst == p.getGoal():
                return True
        else:
            if p.checkCollision(current, dst, t):
                return True
    return False

def removeIllegalMoves(availableMoves, paths, current, t):
    for p in paths: 
        pathEnded = False

        if t not in p.getMoves():
            pathEnded = True

        for edge in availableMoves:
            if pathEnded:
                if edge.dst == p.getGoal():
                    availableMoves.remove(edge)
            else:
                if p.checkCollision(current, edge.dst, t):
                    availableMoves.remove(edge)

    return availableMoves


def chooseRandomGoals(availableCells, nAgents):
    """
    Return a dictionary where:
    KEY: goal cell
    VALUE: max time that a past agent pass through that goal
    """
    goals = {}
    for _ in range(nAgents):
        goal = availableCells.pop()
        while goal in goals:
            availableCells.add(goal)
            goal = availableCells.pop()
        availableCells.add(goal)
        goals[goal] = 0
    return goals

def chooseRandomInit(availableCells, goal):
    """
    Chose init from availableCells, remove it from availableCells and return it
    """
    if goal in availableCells:
        availableCells.remove(goal)
        init = availableCells.pop()
        availableCells.add(goal)
    else:
        init = availableCells.pop()
    return init

def resetPath(path, init, goal, availableCells, nReset, goalsCopy):
    nReset += 1
    t = 0

    tmp = init 
    if goal in availableCells:
        availableCells.remove(goal)
        init = availableCells.pop()
        availableCells.add(goal)
    else:
        init = availableCells.pop()
    availableCells.add(tmp)
    current = init

    path = Path(init, goal)

    return t, current, path, goalsCopy, availableCells, nReset


def waitGoalToBeFree(move, path, paths, t, timeMaxOccupied, current):
    while (checkIllegalMove(move.dst, paths, current, t) or t <= timeMaxOccupied) and not checkIllegalMove(current, paths, current, t):
        path.addMove(t, current, current, 1)
        t += 1
    return t, path

def createPaths(nAgents, limitLengthPath, graph, limitNumberReset):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    availableCells = set(graph.adjacent.keys())
    
    if len(availableCells) < nAgents:
        print("Not enough cells to create a path for each agent")
        return None, 0
    
    goals = chooseRandomGoals(availableCells, nAgents) 

    paths = []
    nReset = 0
    maxLengthPath = 0

    for _ in range(nAgents):
        goal, timeMaxOccupied  = random.choice(list(goals.items()))
        goals.pop(goal)
        
        init = chooseRandomInit(availableCells, goal)

        path = Path(init, goal)
        current = init
        t = 0   


        goalsCopy = goals.copy()

        #TODO: remove print
        while current != goal:
            if nReset > limitNumberReset:
                print("STOPPED FOR MAX ITERATION REACHED")
                return None, 0
            
            availableMoves = graph.adjacent[current] # list of tuple, where a tuple contains (dstNode, weight)

            move = None

            for m in availableMoves:
                if m.dst == goal:
                    t, path = waitGoalToBeFree(m, path, paths, t, timeMaxOccupied, current)
                    move = m if not checkIllegalMove(m.dst, paths, current, t) else None
                    break

            if not move:       
                availableMoves = removeIllegalMoves(availableMoves, paths, current, t)

                if len(availableMoves) == 0:
                    print("RESET NO MOVE")
                    t, current, path, goals, availableCells, nReset = resetPath(path, init, goal, availableCells, nReset, goalsCopy)
                    maxLengthPath = 0
                    continue

                move = random.choice(availableMoves)

            if move.dst in goals:
                goals[move.dst] = t

            path.addMove(t, current, move.dst, move.weight)
            current = move.dst
            t += 1

            # if I can't reach the goal in max iteration, I will start again
            if t > limitLengthPath:
                print("RESET MAX ITERATION")
                t, current, path, goals, availableCells, nReset = resetPath(path, init, goal, availableCells, nReset, goalsCopy)
                maxLengthPath = 0


        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # TODO: remove print
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath



def createPathsUsingReachGoal(nAgents, limitLengthPath, graph, useRelaxedPath = False):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    availableCells = set(graph.adjacent.keys())
    
    if len(availableCells) < nAgents:
        print("Not enough cells to create a path for each agent")
        return None, 0
    
    goals = chooseRandomGoals(availableCells, nAgents) 

    paths = []
    nReset = 0
    maxLengthPath = 0

    for _ in range(nAgents):
        goal, timeMaxOccupied  = random.choice(list(goals.items()))
        goals.pop(goal)
        
        init = chooseRandomInit(availableCells, goal)

        path, _ = reachGoal(graph, paths, init, goal, limitLengthPath, useRelaxedPath)
       
        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # TODO: remove print
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath