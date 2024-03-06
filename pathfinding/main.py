from UI.UI import run
from generator.instanceGenerator import generateInstance
from solver.reachGoal import start
import math

import random
import numpy as np

random.seed(10)
np.random.seed(10)


nrows = 10
ncols = 7
freeCellRatio = 0.9
agglomerationFactor = 0.2
max = 40

nAgents = 2
limitLengthPath = freeCellRatio * nrows * ncols

maxIteration = 80 # max number of iteration to reset the creation of a single path
maxRun = 6 # max number of run to create a valid instance

instance, nIteration = generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, max, limitLengthPath, maxIteration, maxRun)

if not instance:
    print("Parameter max was not valid for the current configuration.")

if instance and nIteration < maxRun: 
    path, minimumSpanningTree = start(instance.getGraph(), instance.getPaths(), instance.getInit(), instance.getGoal(), max)
    if path:
        instance.addPath(path)
        
    # matrix = [[None] * (nAgents+1)  for _ in range(math.ceil(limitLengthPath))]
    # for i, path in enumerate(instance.getPaths()):
    #     for t, move in path.getMoves().items():
    #         matrix[t][i] = move

    # print("Matrix:")
    # for row in matrix:
    #     # print(row)
    #     for r in row:
    #         print(r, end="\t\t\t")
    #     print("\t")

    run(instance.getGrid(), instance.getPaths(), minimumSpanningTree)

else:
    print("Parameters too restrictive, try again with different ones.")

