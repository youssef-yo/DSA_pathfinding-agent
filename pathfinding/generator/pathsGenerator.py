import random
from models.path import Path
from models.instance import Instance
from solver.reachGoal import reachGoal

def chooseRandomGoals(availableCells, nAgents):
    """
    Return a dictionary where:
    KEY: goal cell
    VALUE: max time that a past agent pass through that goal
    """
    goals = {}
    for _ in range(nAgents):
        goal = random.choice(availableCells)
        while goal in goals:
            goal = random.choice(availableCells)
        goals[goal] = -1
    return goals

def chooseRandomInit(availableCells, goal):
    """
    Chose init from availableCells, remove it from availableCells and return it
    """

    init = random.choice(availableCells)
    while init == goal:
        init = random.choice(availableCells)
    availableCells.remove(init)
    return init

def resetPath(path, init, goal, availableCells, nReset, goalsCopy):
    nReset += 1
    t = 0

    tmp = init 
    # if goal in availableCells:
    #     availableCells.remove(goal)
    #     init = random.choice(availableCells)
    #     availableCells.append(goal)
    # else:
    #     init = random.choice(availableCells)
    init = chooseRandomInit(availableCells, goal)
    availableCells.append(tmp)
    current = init

    path = Path(init, goal)

    return t, current, path, goalsCopy, availableCells, nReset

def createPaths(nAgents, limitLengthPath, graph, limitNumberReset):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    availableCells = list(graph.getNodes())
    
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
            
            availableMoves = graph.getNeighbors(current)
            move = None

            for m in availableMoves:
                if m.dst == goal:
                    t = path.waitGoalToBeFree(m, paths, t, timeMaxOccupied, current)
                    move = m if not Path.checkIllegalMove(m.dst, paths, current, t) else None
                    break

            if not move:       
                availableMoves = Path.removeIllegalMoves(availableMoves, paths, current, t)

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

    availableCells = list(graph.getNodes()) 
    
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
        
        # grid is None becuase we don't need it in reachGoal
        instance = Instance(None, graph, paths, init, goal, limitLengthPath)

        path, _ = reachGoal(instance, useRelaxedPath)
       
        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # TODO: remove print
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath