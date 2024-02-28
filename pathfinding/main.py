from UI.UI import run
from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths

nrows = 5
ncols = 5
freeCellRatio = 0.8

nAgents = 4
max = freeCellRatio * nrows * ncols

maxIteration = 80

maxRun = 4
i = 0

grid = gridGenerator(nrows,ncols, freeCellRatio)
graph = createGraphFromGrid(grid)
paths = createPaths(nAgents, max, graph, maxIteration)

while not paths and i < maxRun:
    grid = gridGenerator(nrows,ncols, freeCellRatio)
    graph = createGraphFromGrid(grid)
    paths = createPaths(nAgents, max, graph, maxIteration)
    i += 1

if i < maxRun:
    run(grid, paths)
else:
    print("Parameters too restrictive, try again with different ones.")

