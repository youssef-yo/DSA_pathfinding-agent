from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths
from models.instance import Instance

import random

def generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, maxLengthPathNewAgent, limitLengthPath, limitIteration, limitRun):

    i = 0

    grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
    #TODO: handle when graph is None
    graph = createGraphFromGrid(grid)
    paths, maxLengthPath = createPaths(nAgents, limitLengthPath, graph, limitIteration)

    while not paths and i < limitRun:
        grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
        graph = createGraphFromGrid(grid)
        paths, maxLengthPath = createPaths(nAgents, limitLengthPath, graph, limitIteration)
        i += 1
    

    if not paths: 
        return None, i
    
    # devo definire max
    init, goal = None, None
    occupied_inits = set()
    occupied_goals = set()
    for path in paths:
        init = path.getInit()
        goal = path.getGoal()
        occupied_inits.add(init)
        occupied_goals.add(goal)

    # TODO: check if init and goal are the same, init end goal should be different from existing agents init and goal
    while not init or init in occupied_inits:
        r = random.randint(0, nrows-1)
        c = random.randint(0, ncols-1)

        if grid[r][c] == 0:
            init = (r,c)

    while not goal or goal in occupied_goals or goal == init:
        r = random.randint(0, nrows-1)
        c = random.randint(0, ncols-1)

        if grid[r][c] == 0:
            goal = (r,c)

    maxAvailableCells = len(graph.adjacent.keys())
    maxLengthPath = max(maxLengthPath, maxAvailableCells)

    if maxLengthPathNewAgent > maxLengthPath:
        return None, i
    
    instance = Instance(grid, graph, paths, init, goal, maxLengthPathNewAgent)

    return instance, i