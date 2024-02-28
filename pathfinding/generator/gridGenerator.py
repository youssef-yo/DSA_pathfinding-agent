import random
import math

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

def gridGenerator(rows, cols, freeCellRatio):
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    
    #add obstacles to grid
    obstacleRatio = 1 - freeCellRatio

    nObstacle = math.floor(rows*cols*obstacleRatio)
    grid = addObstacles(grid, nObstacle)

    return grid