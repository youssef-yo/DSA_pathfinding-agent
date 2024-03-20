import argparse

from UI.UI import run as plot

from UI.newUI import UI

from generator.informationGenerator import Information
from generator import informationGenerator

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

from automated_test import automatedTest

import random
import numpy as np

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
        
def main():
    args = getInputArgs()
    # args.test = True
    if args.gui:
        executeUI()
    elif args.test:
        # defaulParameterstValues() # TODO: remove, ask user for SEED
        # setSeed(SEED)   
        automatedTest.executeEvaluationTest()
    else:
        # readParametersFromFile()
        defaulParameterstValues()

        setSeed(SEED)   
        executeCLI()
           

if __name__ == "__main__":
    main()