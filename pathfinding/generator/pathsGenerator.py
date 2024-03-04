import random
from models.path import Path

def checkIllegalMove(dst, paths, current, t):
    for p in paths: 
        pathEnded = False

        if t not in p.getMoves(): # TODO: create method in Path class
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

        if t not in p.getMoves(): # TODO: create method in Path class
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

def waitGoalToBeFree(move, path, paths, t, tMax, current, ):
    while checkIllegalMove(move.dst, paths, current, t):
        path.addMove(t, current, current, 1)
        t += 1
    # Improvement: if next move is the goal but another path will pass through that goal before,
    # I will choose the self loop
    while t <= tMax:
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
        goal, tMax  = random.choice(list(goals.items()))
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

            # Improvement: if next move is the goal but it's illegal, I will choose the self loop until it becomes legal
            for m in availableMoves:
                if m.dst == goal:
                    t, path = waitGoalToBeFree(m, path, paths, t, tMax, current)
                    move = m

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

    
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath