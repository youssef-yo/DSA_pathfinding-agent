from UI.UI import run
from generator.instanceGenerator import generateInstance

nrows = 5
ncols = 5
freeCellRatio = 0.8
agglomerationFactor = 0.3
max = 20

nAgents = 4
limitLengthPath = freeCellRatio * nrows * ncols

maxIteration = 80 # max number of iteration to reset the creation of a single path
maxRun = 4 # max number of run to create a valid instance

instance, nIteration = generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, max, limitLengthPath, maxIteration, maxRun)

if not instance:
    print("Parameter max was not valid for the current configuration.")

if instance and nIteration < maxRun:
    run(instance.getGrid(), instance.getPaths())
else:
    print("Parameters too restrictive, try again with different ones.")

