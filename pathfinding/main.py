import argparse

from UI.UI import run as plot

from UI.newUI import UI

from generator.informationGenerator import Information
from generator import informationGenerator

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

from automated_test.automatedTest import AutomatedTest
from automated_test.elaborateInformation import ElaborateInformation

import random
import numpy as np

import configparser

def getInputArgs():
    parser = argparse.ArgumentParser(description="Pathfinding algorithm for multi-agent systems.")
    parser.add_argument('--gui', action='store_true', help="Execute the program with the GUI interface. If not specified, the program will run in command line mode.")
    parser.add_argument('--test', action='store_true', help="Evaluate the program using automated tests.")
    parser.add_argument('--plot', action='store_true', help="Evaluate the program using cli and plot the final grid.")

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
    

def executeCLI(plotGrid):
    # Start time and memory monitoring
    information = Information(SEED)
    information.startMonitoring()

    goalsInits = None
    instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

    if not instance:
        print("Could not create instance.")
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
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, USE_RELAXED_PATH, USE_REACH_GOAL_EXISTING_AGENTS, LIMIT_LENGTH_EXISTING_PATHS)
            
            information.printInformation()
            information.saveInformationToFile()

            if plotGrid:
                plot(instance.getGrid(), instance.getPaths(), minimumSpanningTree)

def executeUI():
    ui = UI(generateInstance, reachGoal, informationGenerator)
    ui.run()
        
def main():
    args = getInputArgs()
    if args.gui:
        executeUI()
    elif args.test:
        
        seed = 1234
        setSeed(seed)

        # Uncomment to create a csv

        proceed = input("Do you want to proceed with the automated test? (y/n): ")
        if proceed.lower() == "y":
            automatedTest = AutomatedTest()
            data = automatedTest.executeEvaluationTest(seed)
            
            elaborateInformation = ElaborateInformation(data)
            elaborateInformation.printData()
            elaborateInformation.saveDataToFile()
        else:
            print("Automated test cancelled.")

        # Uncomment to read the csv and plot the data
        
        # elaborateInformation = ElaborateInformation(None)
        # elaborateInformation.loadDataFromFile()
        # elaborateInformation.elaborateData()
    else:
        readParametersFromFile()
        # defaulParameterstValues()

        setSeed(SEED)   
        executeCLI(args.plot)
           

if __name__ == "__main__":
    main()