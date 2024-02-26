from UI.UI import run
from generator.gridGenerator import gridGenerator
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import createPaths

nrows = 5
ncols = 5
freeCellRatio = 0.7

grid = gridGenerator(nrows,ncols, freeCellRatio)
graph = createGraphFromGrid(grid)

nAgents = 4 
max = 20
paths = createPaths(nAgents, max, graph)

run(grid, paths)

