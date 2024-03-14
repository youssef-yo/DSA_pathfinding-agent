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

def createPaths(goalsInits, nAgents, limitLengthPath, graph, limitNumberReset):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    paths = []
    maxLengthPath = 0

    for _ in range(nAgents):
        goal, (init, timeMaxGoalOccupied) = goalsInits.popitem()
        path = Path(init, goal)
        current = init
        t = 0   
        nReset = 0

        goalsInitsCopy = goalsInits.copy()

        #TODO: remove print
        while current != goal:
            if nReset > limitNumberReset:
                print("STOPPED FOR MAX ITERATION REACHED")
                return None, 0
            
            availableMoves = graph.getNeighbors(current)
            move = None

            for m in availableMoves:
                if m.dst == goal:
                    t = path.waitGoalToBeFree(m, paths, t, timeMaxGoalOccupied, current)
                    move = m if not Path.checkIllegalMove(m.dst, paths, current, t) and t > timeMaxGoalOccupied else None
                    break

            if not move:       
                availableMoves = Path.removeIllegalMoves(availableMoves, paths, current, t)

                if len(availableMoves) == 0:
                    print("RESET NO MOVE")
                    t, current, path, nReset, goalsInits = resetPath(path, init, goal, nReset, goalsInitsCopy)
                    maxLengthPath = 0
                    continue

                move = random.choice(availableMoves)

            if move.dst in goalsInits:
                goalsInits[move.dst] = (goalsInits[move.dst][0], max(goalsInits[move.dst][1], t))

            path.addMove(t, current, move.dst, move.weight)
            current = move.dst
            t += 1

            # if I can't reach the goal in max iteration, I will start again
            if t > limitLengthPath:
                print("RESET MAX ITERATION")
                t, current, path, nReset, goalsInits = resetPath(path, init, goal, nReset, goalsInitsCopy)
                maxLengthPath = 0


        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # TODO: remove print
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath, goalsInits

def createPathsUsingReachGoal(goalsInits, nAgents, limitLengthPath, graph, useRelaxedPath = False):
    """
    For all nAgents we will choose randomly the initial and goal positions
    The movement of the agents will be random as well
    INIT and GOAL must be different for each agent
    """

    paths = []
    nReset = 0
    maxLengthPath = 0

    for _ in range(nAgents):
        goal, (init, timeMaxGoalOccupied) = goalsInits.popitem()

        # grid is None becuase we don't need it in reachGoal
        instance = Instance(None, graph, paths, init, goal, limitLengthPath, timeMaxGoalOccupied)

        path, _, _ = reachGoal(instance, useRelaxedPath)
       
        paths.append(path)
        maxLengthPath = max(maxLengthPath, path.getLength())

    # TODO: remove print
    for path in paths:
        path.printPath()
    
    return paths, maxLengthPath, goalsInits