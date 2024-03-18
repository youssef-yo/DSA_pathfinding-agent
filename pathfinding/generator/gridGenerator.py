import random
import math
from models.grid import Grid

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

    startR, startC = random.randint(0, grid.getNrows()-1), random.randint(0, grid.getNcols()-1)    
    grid.addObstacle(startR, startC)

    while grid.getLengthObstacles() < nObstaclesInAgglomeration:
        randomDirection = random.choice(directions)
        randomCellInAgglomeration = random.choice(list(grid.getOccupiedCells()))

        nextR, nextC = randomCellInAgglomeration[0] + randomDirection[0], randomCellInAgglomeration[1] + randomDirection[1]
        if 0 <= nextR < grid.getNrows() and 0 <= nextC < grid.getNcols() and grid.isFree(nextR, nextC):
            grid.addObstacle(nextR, nextC) 
    
        
def addObstacles(grid, nObstacle, agglomerationFactor):
    if nObstacle == 0:
        return grid
    nObstaclesInAgglomeration = math.floor(agglomerationFactor * nObstacle)

    createAgglomeration(grid, nObstaclesInAgglomeration)

    nObstacle = nObstacle - nObstaclesInAgglomeration

    grid.addRandomObstacle(nObstacle)

    return grid

def gridGenerator(rows, cols, freeCellRatio, agglomerationFactor):
    """"
    Generate a grid of size rows x cols with freeCellRatio of free cells
    grid[r][c] = 0 -> free cell
    grid[r][c] = 1 -> obstacle
    """

    # grid = [[0 for _ in range(rows)] for _ in range(cols)]
    grid = Grid(rows, cols)

    #add obstacles to grid
    obstacleRatio = 1 - freeCellRatio

    nObstacle = math.floor(rows*cols*obstacleRatio)
    grid = addObstacles(grid, nObstacle, agglomerationFactor)

    return grid