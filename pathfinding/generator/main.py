import math
import random
from models.Graph import Graph

# GRID 
# 0 -> free cell
# 1 -> obstacle

def addObstacles(grid, nObstacle):
    rows, cols = len(grid), len(grid[0])
    obstacoles = set() 

    for _ in range(nObstacle):
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)

        while (r,c) in obstacoles:
            r = random.randint(0, rows-1)
            c = random.randint(0, cols-1)

        obstacoles.add((r,c))
        grid[r][c] = 1

    return grid

def createGraphFromGrid(grid):
    rows, cols = len(grid), len(grid[0])

    cardinalMoves = [(0,0), (-1,0), (1,0), (0,-1), (0,1)] #cardinal moves and self-loop have cost = 1
    diagonalMoves = [(1,1), (-1,1), (-1,-1), (1,-1)] #diagonal moves have cost = sqrt(2)

    graph = Graph()
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 1:
                for x,y in cardinalMoves:
                    r = i + x
                    c = j + y

                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                        graph.addEdge((i,j), (r,c), 1)

                for x,y in diagonalMoves:
                    r = i + x
                    c = j + y

                    if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                        graph.addEdge((i,j), (r,c), math.sqrt(2))
    return graph

def gridGenerator(rows, cols, freeCellRatio):
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    
    #add obstacles to grid
    obstacleRatio = 1 - freeCellRatio

    nObstacle = math.floor(rows*cols*obstacleRatio)
    grid = addObstacles(grid, nObstacle)

    return grid
    

def graphGenerator(rows, cols, freeCellRatio):
    grid = gridGenerator(rows, cols, freeCellRatio)
    graph = createGraphFromGrid(grid)

    graph.printGraph()

    return graph

def graphGeneratorFromGrid(grid):
    return createGraphFromGrid(grid)