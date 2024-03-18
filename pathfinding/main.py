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

# seed = 10 to check waitGoalToBeFree (nAgent = 2)
seed = 22
random.seed(seed)
np.random.seed(seed)

NROWS = 10
NCOLS = 13
FREE_CELL_RATIO = 1
AGGLOMERATION_FACTOR = 0.3
MAX = 40

N_AGENTS = 3

USE_RELAXED_PATH = True
USE_REACH_GOAL_EXISTING_AGENTS = False

def main():
    parser = argparse.ArgumentParser(description="Pathfinding algorithm for multi-agent systems.")
    parser.add_argument('--gui', action='store_true', help="Execute the program with the GUI interface. If not specified, the program will run in command line mode.")
    args = parser.parse_args()

    if args.gui:
        ui = UI(generateInstance, reachGoal, informationGenerator, seed) #TODO: create class for the two controllers
        ui.run()
    else:
        # Start time and memory monitoring
        information = Information(seed)
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