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

def createInits(nAgents, availableCells):
    """
    Select random Init for each agent. 
    Select Init e Goal for the n+1 agent
    Return a set of inits and a dictionary where:
    KEY: goal cell
    VALUE: tuple (init cell, value of max time that a past agent pass through that goal)
    """
    inits = set()
    for _ in range(nAgents):
        init = chooseRandomInit(availableCells, None)
        inits.add(init)
    
    # find the init and goal for the n+1 agent
    goalsInits = {}
    goal = random.choice(availableCells)
    init = chooseRandomInit(availableCells, goal)
    goalsInits[goal] = (init, -1)

    return inits, goalsInits

def generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, maxLengthPathNewAgent, limitLengthExistingPaths, goalsInits, useReachGoal=False, useRelaxedPath = True):
    # limitLengthPath = freeCellRatio * nrows * ncols
    goalInitNewAgent, grid, graph, paths, maxLenthAllPaths = initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthExistingPaths, goalsInits, useReachGoal, useRelaxedPath)

    if not paths: 
        return None
    
    goal, (init, timeMaxOccupied) = goalInitNewAgent.popitem()

    maxAvailableCells = len(graph.getNodes())
    limitMaxNewAgent = maxAvailableCells + maxLenthAllPaths

    if maxLengthPathNewAgent > limitMaxNewAgent:
        return None
    
    instance = Instance(grid, graph, paths, init, goal, maxLengthPathNewAgent, timeMaxOccupied)

    return instance


def initVars(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, limitLengthExistingPaths, goalsInits, useReachGoal, useRelaxedPath):   
    grid = gridGenerator(nrows,ncols, freeCellRatio, agglomerationFactor)
    graph = createGraphFromGrid(grid)

    availableCells = list(graph.getNodes())
    if len(availableCells) < nAgents:
        #TODO: throw exception
        print("Not enough cells to create a path for each agent")
        return None, None, None, None, None

    limit = len(availableCells)
    if useReachGoal:
        if not goalsInits:
            goalsInits = createGoalsInits(nAgents, availableCells)
    
        # check reachability
        islands = findIslands(grid)
        if islands:
            for goal, (init, _) in goalsInits.items():
                if not checkReachability(init, goal, islands):
                    return goalsInits, grid, graph, None, None
            
        paths, maxLengthAllPaths, goalInitNewAgent = createPathsUsingReachGoal(goalsInits, nAgents, limit, graph, useRelaxedPath)
    else:
        if not goalsInits:
            inits, goalsInits = createInits(nAgents, availableCells)
        else:
            inits = set()
            for _, (init, _) in goalsInits.items():
                inits.add(init)
                
        paths, maxLengthAllPaths, goalInitNewAgent = createPaths(inits, goalsInits, nAgents, limitLengthExistingPaths, graph)
    
    return goalInitNewAgent, grid, graph, paths, maxLengthAllPaths