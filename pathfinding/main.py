from UI.UI import run
from generator.instanceGenerator import generateInstance
from solver.reachGoal import start
nrows = 7
ncols = 7
freeCellRatio = 0.9
agglomerationFactor = 0.2
max = 40

nAgents = 3
limitLengthPath = freeCellRatio * nrows * ncols

maxIteration = 80 # max number of iteration to reset the creation of a single path
maxRun = 4 # max number of run to create a valid instance

instance, nIteration = generateInstance(nrows, ncols, freeCellRatio, agglomerationFactor, nAgents, max, limitLengthPath, maxIteration, maxRun)

if not instance:
    print("Parameter max was not valid for the current configuration.")

if instance and nIteration < maxRun: 
    path = start(instance.getGraph(), instance.getPaths(), instance.getInit(), instance.getGoal(), max)
    if path:
        instance.addPath(path)
        
    run(instance.getGrid(), instance.getPaths())

else:
    print("Parameters too restrictive, try again with different ones.")

