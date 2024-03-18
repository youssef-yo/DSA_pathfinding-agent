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


# import time
# import tracemalloc

# seed = 10 to check waitGoalToBeFree (nAgent = 2)
random.seed(22)
np.random.seed(12)

NROWS = 100
NCOLS = 100
FREE_CELL_RATIO = 0.8
AGGLOMERATION_FACTOR = 1
MAX = 30

N_AGENTS = 3
LIMIT_LENGTH_PATH = FREE_CELL_RATIO * NROWS * NCOLS #TODO: distanza diagonale tra init e goal corrente * nAgents

MAX_ITERATION = 80 # max number of iteration to reset the creation of a single path
MAX_TOTAL_RUN = 6 # max number of run to create a valid instance

USE_RELAXED_PATH = True
USE_REACH_GOAL_EXISTING_AGENTS = True

def main():
    parser = argparse.ArgumentParser(description="Pathfinding algorithm for multi-agent systems.")
    parser.add_argument('--gui', action='store_true', help="Execute the program with the GUI interface. If not specified, the program will run in command line mode.")
    args = parser.parse_args()

    if args.gui:
        ui = UI(generateInstance, reachGoal, informationGenerator) #TODO: create class for the two controllers
        ui.run()
    else:
        # Start time and memory monitoring
        information = Information()
        information.startMonitoring()

        instance, nIteration = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

        if not instance:
            print("Parameter max was not valid for the current configuration.")

        if instance and nIteration < MAX_TOTAL_RUN: 
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
        else:
            print("Parameters too restrictive, try again with different ones.")

           
# def testCheckReachability(grid, init, goal):
#     grid = [["0", "0", "1", "1", "0"],
#             ["0", "0", "0", "1", "0"],
#             ["1", "1", "1", "0", "0"],
#             ["0", "0", "0", "0", "0"]]
    
#     islands = findIslands(grid)
#     print(islands)
#     init = (0, 0)
#     goal = (3, 4)
#     print(islands)
#     for island in islands:
#         if (init in island and goal not in island) or (goal in island and init not in island):
#             return False
#     return True

if __name__ == "__main__":
    main()