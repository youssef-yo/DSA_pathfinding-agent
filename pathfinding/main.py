from UI.UI import run as runUI
from UI.interactiveUI import run as runInteractiveUI

from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

import random
import numpy as np

# seed = 10 to check waitGoalToBeFree (nAgent = 2)
random.seed(13)
np.random.seed(13)


nrows = 7
ncols = 7
freeCellRatio = 0.9
agglomerationFactor = 0.2
max = 40

nAgents = 4
limitLengthPath = freeCellRatio * nrows * ncols

maxIteration = 80 # max number of iteration to reset the creation of a single path
maxRun = 6 # max number of run to create a valid instance

useRelaxedPath = False
instance, nIteration = generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, max, limitLengthPath, maxIteration, maxRun)

if not instance:
    print("Parameter max was not valid for the current configuration.")

if instance and nIteration < maxRun: 
    print(" ------------- ")
    print("NEW AGENT (init, goal): (", instance.getInit(), ", ", instance.getGoal(), ")")
    
    path, minimumSpanningTree = reachGoal(instance.getGraph(), instance.getPaths(), instance.getInit(), instance.getGoal(), max, useRelaxedPath)
    
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

