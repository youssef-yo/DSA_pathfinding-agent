import argparse

from UI.UI import run as plot

from UI.newUI import UI

from generator.informationGenerator import Information
from generator import informationGenerator

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

import math
import random
import numpy as np
import gc   # garbage collector

import configparser

def getInputArgs():
    parser = argparse.ArgumentParser(description="Pathfinding algorithm for multi-agent systems.")
    parser.add_argument('--gui', action='store_true', help="Execute the program with the GUI interface. If not specified, the program will run in command line mode.")
    parser.add_argument('--test', action='store_true', help="Evaluate the program using automated tests.")

    return parser.parse_args()


def setSeed(seed):
    random.seed(seed)
    np.random.seed(seed)


def defaulParameterstValues():
    global NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH, SEED
    NROWS = 45
    NCOLS = 45
    FREE_CELL_RATIO = 0.7
    AGGLOMERATION_FACTOR = 0.2
    MAX = 60
    LIMIT_LENGTH_EXISTING_PATHS = 40

    N_AGENTS = 50

    USE_RELAXED_PATH = True
    USE_REACH_GOAL_EXISTING_AGENTS = False

    SEED = 6453

def readParametersFromFile():
    global NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH, SEED
    config = configparser.ConfigParser()
    config.read('parameters.INI')

    # GRID
    NROWS = int(config['GRID']['n_rows'])
    NCOLS = int(config['GRID']['n_cols'])
    FREE_CELL_RATIO = float(config['GRID']['free_cells_ratio'])
    AGGLOMERATION_FACTOR = float(config['GRID']['agglomeration_factor'])
    # INSTANCE
    N_AGENTS = int(config['INSTANCE']['n_agents'])
    MAX = int(config['INSTANCE']['max'])
    LIMIT_LENGTH_EXISTING_PATHS = int(config['INSTANCE']['limit_length_existing_paths'])
    USE_RELAXED_PATH = config['INSTANCE'].getboolean('use_relaxed_path')
    USE_REACH_GOAL_EXISTING_AGENTS = config['INSTANCE'].getboolean('use_reach_goal_existing_agents')
    # SEED
    SEED = int(config['SEED']['seed'])
    

def executeCLI():
    # Start time and memory monitoring
    information = Information(SEED)
    information.startMonitoring()

    goalsInits = None
    instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

    if not instance:
        print("Parameter max was not valid for the current configuration.\n Parameters too restrictive, try again with different ones.")
    else:
        print(" ------------- ")
        print("NEW AGENT (init, goal): (", instance.getInit(), ", ", instance.getGoal(), ")")
        
        path, minimumSpanningTree, closedSet = reachGoal(instance, USE_RELAXED_PATH)
        
        if not path:
            print("No path found for new agent")
        else:
            print("!!!! Path found for new agent")
            path.printPath()

        if path:
            instance.addPath(path)

            information.stopMonitoring()
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, USE_RELAXED_PATH, USE_REACH_GOAL_EXISTING_AGENTS)
            
            information.printInformation()
            information.saveInformationToFile()

            plot(instance.getGrid(), instance.getPaths(), minimumSpanningTree)

def executeUI():
    ui = UI(generateInstance, reachGoal, informationGenerator) #TODO: create class for the two controllers
    ui.run()

def runSingleSimulation(goalsInits, useReachGoalExistingAgents, useRelaxedPath):
    information = Information(SEED)
    information.startMonitoring()
        
    instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
    
    if not instance:
        print("Could not create instance.")
        # TODO: save to file
    else:
        path, minimumSpanningTree, closedSet = reachGoal(instance, USE_RELAXED_PATH)
        if path:
            instance.addPath(path)

            information.stopMonitoring()
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, USE_RELAXED_PATH, USE_REACH_GOAL_EXISTING_AGENTS)
            
            # information.printInformation()
            information.saveInformationToFile()
        else:
            print("No path found for new agent")
            # TODO: save to file
    
    return instance

def freeMemory():
    gc.collect()

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


def executeEvaluationTest():
    global NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH
    
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
    
    for i in range(0, 0.7, 0.1):
        FREE_CELL_RATIO = i
        NROWS = NCOLS = math.ceil(10 * ((i*10)+1))
        
        AGGLOMERATION_FACTOR = 1 / math.ceil(10 * ((i*10)+1))
        N_AGENTS = 3*math.ceil(10 * ((i*10)+1))
        MAX = 10 * N_AGENTS * math.ceil(10 * ((i*10)+1))

        defineCombination()
        
def main():
    args = getInputArgs()
    args.test = True
    if args.gui:
        executeUI()
    elif args.test:
        defaulParameterstValues() # TODO: remove, ask user for SEED
        setSeed(SEED)   
        executeEvaluationTest()
    else:
        # readParametersFromFile()
        defaulParameterstValues()

        setSeed(SEED)   
        executeCLI()
           

if __name__ == "__main__":
    main()