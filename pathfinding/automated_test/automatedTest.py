import gc
import math
import random
import numpy as np
from generator.informationGenerator import Information
from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal


def freeMemory():
    gc.collect()

def executeEvaluationTest():
    global SEED, NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS
    
    #TODO: generate random or ask?
    SEED = 1234

    for i in range(1,11): # totali run = 10 * 6 * 3 = 180 * 4 (combinazioni) = 720 
        for kRows in range(5,11):
            NROWS = NCOLS = kRows * i
            FREE_CELL_RATIO = 1 - 0.1 * (i - 1)
            AGGLOMERATION_FACTOR = 1 / i
            for factorAgent in np.arange(0.1, 0.6, 0.2):
                availableCells = NROWS * NCOLS * FREE_CELL_RATIO  

                N_AGENTS = int(math.ceil(availableCells * factorAgent))                 
                LIMIT_LENGTH_EXISTING_PATHS = max(int((availableCells - N_AGENTS) * 0.5), 1)
                MAX = int(math.ceil((availableCells + LIMIT_LENGTH_EXISTING_PATHS) * 0.3))

                print("I: ", i, "NROWS: ", NROWS, " N_AGENTS: ", N_AGENTS, " FREE_CELL_RATIO: ", FREE_CELL_RATIO, " AGGLOMERATION_FACTOR: ", AGGLOMERATION_FACTOR, " MAX: ", MAX, " LIMIT_LENGTH_EXISTING_PATHS: ", LIMIT_LENGTH_EXISTING_PATHS)
                
                defineCombination()


def runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath):
    information = Information(SEED)
    information.startMonitoring()
        
    instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
    
    if not instance:
        print("Could not create instance.")
        information.stopMonitoring()
        information.setValues(None, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, None, None, None, useRelaxedPath, useReachGoalExistingAgents)
        information.saveFailInformationToFile()
    else:
        path, minimumSpanningTree, closedSet = reachGoal(instance, useRelaxedPath)
        if path:
            instance.addPath(path)

            information.stopMonitoring()
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, useRelaxedPath, useReachGoalExistingAgents)
            
            # information.printInformation()
            information.saveInformationToFile()
        else:
            print("No path found for new agent")
            information.stopMonitoring()
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, None, None, None, useRelaxedPath, useReachGoalExistingAgents)
            information.saveFailInformationToFile()
    
    return instance

def defineCombination():
    goalsInits = None
    useReachGoalExistingAgents = False
    useRelaxedPath = False

    print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
    instance = runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath)

    freeMemory()
    #####

    if instance:
        goalsInits = instance.getGoalsInits()
    
    useReachGoalExistingAgents = False
    useRelaxedPath = True

    print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
    instance = runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath)
    freeMemory()
    #####

    if instance:
        goalsInits = instance.getGoalsInits()
    
    useReachGoalExistingAgents = True
    useRelaxedPath = False

    print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
    instance = runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath)
    freeMemory()
    #####

    if instance:
        goalsInits = instance.getGoalsInits()
    
    useReachGoalExistingAgents = True
    useRelaxedPath = True

    print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
    instance = runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath)
    freeMemory()