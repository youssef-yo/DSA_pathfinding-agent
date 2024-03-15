from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths, createPathsUsingReachGoal
from generator.reachability import checkReachability, findIslands
from models.instance import Instance

import random

def chooseRandomInit(availableCells, goal):
    """
    Chose init from availableCells, remove it from availableCells and return it
    """

    init = random.choice(availableCells)
    while init == goal:
        init = random.choice(availableCells)
    availableCells.remove(init)
    return init

def createGoalsInits(nAgents, availableCells):
    """
    Select random Init and Goal for each agent plus the new agent
    Return a dictionary where:
    KEY: goal cell
    VALUE: tuple (init cell, value of max time that a past agent pass through that goal)
    """
    goalsInits = {}
    for _ in range(nAgents + 1):
        goal = random.choice(availableCells)
        while goal in goalsInits:
            goal = random.choice(availableCells)
        init = chooseRandomInit(availableCells, goal)

        goalsInits[goal] = (init, -1)
    return goalsInits


def generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, maxLengthPathNewAgent, limitLengthPath, limitIteration, limitRun, useReachGoal=False, useRelaxedPath = True):
    goalsInits, grid, graph, paths, maxLengthPath, i = initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthPath, limitIteration, limitRun, useReachGoal, useRelaxedPath)

    if not paths: 
        return None, i
    
    goal, (init, timeMaxOccupied) = goalsInits.popitem()

    maxAvailableCells = len(graph.getNodes())
    maxLengthPath = max(maxLengthPath, maxAvailableCells)

    if maxLengthPathNewAgent > maxLengthPath:
        return None, i
    
    instance = Instance(grid, graph, paths, init, goal, maxLengthPathNewAgent, timeMaxOccupied)

    return instance, i

def chooseRandomNode(grid, occupied_nodes):
    nrows, ncols = grid.getNrows(), grid.getNcols()
    node = None
    
    while not node or node in occupied_nodes:
        r = random.randint(0, nrows-1)
        c = random.randint(0, ncols-1)

        if grid.isFree(r, c):
            node = (r,c)
    
    return node


def initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthPath, limitIteration, limitRun, useReachGoal, useRelaxedPath):
    i = 0
    
    grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
    graph = createGraphFromGrid(grid)

    availableCells = list(graph.getNodes())
    if len(availableCells) < nAgents:
        #TODO: throw exception
        print("Not enough cells to create a path for each agent")
        return None, None, None, None, None, None
    goalsInits = createGoalsInits(nAgents, availableCells)
    
    # check reachability
    islands = findIslands(grid)
    for goal, (init, _) in goalsInits.items():
        if not checkReachability(init, goal, islands):
            return goalsInits, grid, graph, None, None, None

    limit = nrows*ncols*nAgents
    if useReachGoal:
        paths, maxLengthPath, goalsInits = createPathsUsingReachGoal(goalsInits, nAgents, limit, graph, useRelaxedPath)
    else: 
        paths, maxLengthPath, goalsInits = createPaths(goalsInits, nAgents, limitLengthPath, graph, limitIteration)

    while not paths and i < limitRun:
        grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
        graph = createGraphFromGrid(grid)
        
        if useReachGoal:
            paths, maxLengthPath, goalsInits = createPathsUsingReachGoal(goalsInits, nAgents, limit, graph, useRelaxedPath)
        else:
            paths, maxLengthPath, goalsInits = createPaths(goalsInits, nAgents, limitLengthPath, graph, limitIteration)
        
        i += 1

    return goalsInits, grid, graph, paths, maxLengthPath, i