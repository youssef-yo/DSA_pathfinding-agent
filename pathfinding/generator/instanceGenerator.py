from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths, createPathsUsingReachGoal
from models.instance import Instance

import random

def generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, maxLengthPathNewAgent, limitLengthPath, limitIteration, limitRun):

    grid, graph, paths, maxLengthPath, i = initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthPath, limitIteration, limitRun)

    if not paths: 
        return None, i
    
    occupied_inits = set()
    occupied_goals = set()
    for path in paths:
        init = path.getInit()
        goal = path.getGoal()
        occupied_inits.add(init)
        occupied_goals.add(goal)

    init = chooseRandomNode(grid, occupied_inits)

    goal = chooseRandomNode(grid, occupied_goals)
    while goal == init:
        goal = chooseRandomNode(grid, occupied_goals)

    maxAvailableCells = len(graph.adjacent.keys())
    maxLengthPath = max(maxLengthPath, maxAvailableCells)

    if maxLengthPathNewAgent > maxLengthPath:
        return None, i
    
    instance = Instance(grid, graph, paths, init, goal, maxLengthPathNewAgent)

    return instance, i

def chooseRandomNode(grid, occupied_nodes):
    nrows, ncols = len(grid), len(grid[0])
    node = None
    
    while not node or node in occupied_nodes:
        r = random.randint(0, nrows-1)
        c = random.randint(0, ncols-1)

        if grid[r][c] == 0:
            node = (r,c)
    
    return node


def initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthPath, limitIteration, limitRun):
    i = 0
    
    grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
    #TODO: handle when graph is None
    graph = createGraphFromGrid(grid)
    #paths, maxLengthPath = createPaths(nAgents, limitLengthPath, graph, limitIteration)
    limit = nrows*ncols*nAgents
    paths, maxLengthPath = createPathsUsingReachGoal(nAgents, limit, graph)

    while not paths and i < limitRun:
        grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
        graph = createGraphFromGrid(grid)
        #paths, maxLengthPath = createPaths(nAgents, limitLengthPath, graph, limitIteration)
        
        paths, maxLengthPath = createPathsUsingReachGoal(nAgents, limit, graph)
        i += 1

    return grid, graph, paths, maxLengthPath, i