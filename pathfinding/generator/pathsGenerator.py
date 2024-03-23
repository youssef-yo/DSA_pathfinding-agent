import random
from models.path import Path
from models.instance import Instance
from solver.reachGoal import reachGoal

def resetPath(path, init, goal, nReset, goalsInitsCopy):
    nReset += 1
    t = 0

    current = init

    path = Path(init, goal)

    return t, current, path, nReset, goalsInitsCopy

def createPaths(inits, goalsInits, nAgents, limitLengthExistingPaths, graph):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """
    paths = []

    #TODO: check if it works ok (alternative: us random.gauss
    limitPath = random.randint(1, limitLengthExistingPaths) 
    maxLengthAllPaths = 0

    for _ in range(nAgents):
        init = inits.pop()

        path = Path(init, None)
        current = init
        t = 0

        while t < limitPath:
            availableMoves = graph.getNeighbors(current)

            availableMoves = Path.removeIllegalMoves(availableMoves, paths, current, t)

            if len(availableMoves) == 0:
                return None, 0, None
            
            move = random.choice(availableMoves)

            if move.dst in goalsInits:
                goalsInits[move.dst] = (goalsInits[move.dst][0], max(goalsInits[move.dst][1], t))

            path.addMove(t, current, move.dst, move.weight)
            current = move.dst
            t += 1
        
        path.setGoal(current)

        paths.append(path)
        maxLengthAllPaths = max(maxLengthAllPaths, path.getLength())

    return paths, maxLengthAllPaths, goalsInits

def createPathsUsingReachGoal(goalsInits, nAgents, limitLengthPath, graph, useRelaxedPath = False):
    """
    For all nAgents we will choose randomly the initial and goal positions
        The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    paths = []
    maxLengthPath = 0

    for _ in range(nAgents):
        goal, (init, timeMaxGoalOccupied) = goalsInits.popitem()

        # grid is None becuase we don't need it in reachGoal
        instance = Instance(None, graph, paths, init, goal, limitLengthPath, timeMaxGoalOccupied)

        path, _, _ = reachGoal(instance, useRelaxedPath)

        if not path:
            return None, None, None

        for t, move in path.getMoves():
            if move.dst in goalsInits:
                    goalsInits[move.dst] = (goalsInits[move.dst][0], max(goalsInits[move.dst][1], t))

        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # for path in paths:
    #     path.printPath()

    return paths, maxLengthPath, goalsInits