from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths
from models.instance import Instance

import random

def generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, maxLengthPathNewAgent, limitLengthPath, limitIteration, limitRun):

    i = 0

    grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
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
    
    while not init:
        r = random.randint(0, nrows-1)
        c = random.randint(0, ncols-1)

        if grid[r][c] == 0:
            init = (r,c)

    while not goal:
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