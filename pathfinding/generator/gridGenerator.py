import random
import math

# GRID 
# 0 -> free cell
# 1 -> obstacle

def createAgglomeration(grid, nObstaclesInAgglomeration):
    """"
    Create an agglomeration of obstacles
    We suppose that we want one agglomeration of obstacles.
    Factor of agglomeration = [0, 1] and moltiplied the number of obstacles in the agglomeration gives us 
    the number of obstacles in the agglomeration.
    The ramaining obstacles will be placed randomly in the grid (so it can happen
    that they will be placed in the agglomeration as well, but it is not a problem)
    """

    directions = [(0,1), (0,-1), (1,0), (-1,0)]

    rows, cols = len(grid), len(grid[0])
    agglomeration = set()

    startR, startC = random.randint(0, rows-1), random.randint(0, cols-1)
    agglomeration.add((startR, startC))
    grid[startR][startC] = 1

    while len(agglomeration) < nObstaclesInAgglomeration:
        randomDirection = random.choice(directions)
        randomCellInAgglomeration = random.choice(list(agglomeration))

        nextR, nextC = randomCellInAgglomeration[0] + randomDirection[0], randomCellInAgglomeration[1] + randomDirection[1]
        if 0 <= nextR < rows and 0 <= nextC < cols and (nextR, nextC) not in agglomeration:
            agglomeration.add((nextR, nextC))
            grid[nextR][nextC] = 1

    return agglomeration
    
        
def addObstacles(grid, nObstacle, agglomerationFactor):

    rows, cols = len(grid), len(grid[0])

    nObstaclesInAgglomeration = math.floor(agglomerationFactor * nObstacle)
    obstacoles = createAgglomeration(grid, nObstaclesInAgglomeration) 

    nObstacle = nObstacle - nObstaclesInAgglomeration

    for _ in range(nObstacle):
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)

        while (r,c) in obstacoles:
            r = random.randint(0, rows-1)
            c = random.randint(0, cols-1)

        obstacoles.add((r,c))
        grid[r][c] = 1

    return grid

def gridGenerator(rows, cols, freeCellRatio, agglomerationFactor):
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    
    #add obstacles to grid
    obstacleRatio = 1 - freeCellRatio

    nObstacle = math.floor(rows*cols*obstacleRatio)
    grid = addObstacles(grid, nObstacle, agglomerationFactor)

    return grid