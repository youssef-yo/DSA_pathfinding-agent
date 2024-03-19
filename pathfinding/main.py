import argparse

from UI.UI import run as runUI
from UI.interactiveUI import run as runInteractiveUI
from UI.newUI import UI

from generator.informationGenerator import Information
from generator import informationGenerator

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

import random
import numpy as np

import configparser
# seed = 10 to check waitGoalToBeFree (nAgent = 2)

def setSeed(seed):
    random.seed(seed)
    np.random.seed(seed)


def defaulParameterstValues():
    global NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH, SEED
    NROWS = 10
    NCOLS = 13
    FREE_CELL_RATIO = 1
    AGGLOMERATION_FACTOR = 0.3
    MAX = 40

    N_AGENTS = 3

    USE_RELAXED_PATH = True
    USE_REACH_GOAL_EXISTING_AGENTS = False

    SEED = 22

def readParametersFromFile():
    global NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH, SEED
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
    USE_RELAXED_PATH = config['INSTANCE'].getboolean('use_relaxed_path')
    USE_REACH_GOAL_EXISTING_AGENTS = config['INSTANCE'].getboolean('use_reach_goal_existing_agents')
    # SEED
    SEED = int(config['SEED']['seed'])
    

def getParameters():
    defaulParameterstValues()
    #readParametersFromFile()

def main():
    getParameters()
    setSeed(SEED)
    parser = argparse.ArgumentParser(description="Pathfinding algorithm for multi-agent systems.")
    parser.add_argument('--gui', action='store_true', help="Execute the program with the GUI interface. If not specified, the program will run in command line mode.")
    args = parser.parse_args()

    if args.gui:
        ui = UI(generateInstance, reachGoal, informationGenerator, SEED) #TODO: create class for the two controllers
        ui.run()
    else:
        # Start time and memory monitoring
        information = Information(SEED)
        information.startMonitoring()

        instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

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

                # runUI(instance.getGrid(), instance.getPaths(), minimumSpanningTree)
           

if __name__ == "__main__":
    main()