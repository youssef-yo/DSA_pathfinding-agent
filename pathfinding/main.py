from UI.UI import run as runUI
from UI.interactiveUI import run as runInteractiveUI

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

import random
import numpy as np

# seed = 10 to check waitGoalToBeFree (nAgent = 2)
random.seed(22)
np.random.seed(12)

NROWS = 7
NCOLS = 7
FREE_CELL_RATIO = 0.9
AGGLOMERATION_FACTOR = 0.2
MAX = 30

N_AGENTS = 4
LIMIT_LENGTH_PATH = FREE_CELL_RATIO * NROWS * NCOLS

MAX_ITERATION = 80 # max number of iteration to reset the creation of a single path
MAX_TOTAL_RUN = 6 # max number of run to create a valid instance

USE_RELAXED_PATH = False
USE_REACH_GOAL_EXISTING_AGENTS = True

def main():
    instance, nIteration = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

    if not instance:
        print("Parameter max was not valid for the current configuration.")

    if instance and nIteration < MAX_TOTAL_RUN: 
        print(" ------------- ")
        print("NEW AGENT (init, goal): (", instance.getInit(), ", ", instance.getGoal(), ")")
        
        path, minimumSpanningTree = reachGoal(instance, USE_RELAXED_PATH)
        
        if not path:
            print("No path found for new agent")
        else:
            print("!!!! Path found for new agent")
            path.printPath()

        if path:
            instance.addPath(path)

        runUI(instance.getGrid(), instance.getPaths(), minimumSpanningTree)
        # runInteractiveUI(instance.getGrid(), instance.getPaths())

    else:
        print("Parameters too restrictive, try again with different ones.")

if __name__ == "__main__":
    main() 