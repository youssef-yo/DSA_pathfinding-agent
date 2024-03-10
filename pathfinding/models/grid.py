import random

class Grid:
    def __init__(self, nrows, ncols) -> None:
        """
        nrows: number of rows
        ncols: number of columns
        freeCells: set of free cells
        """
        self.nrows = nrows
        self.ncols = ncols
        
        self.occupiedCells = set()

    def getNrows(self):
        return self.nrows

    def getNcols(self):
        return self.ncols
    
    def getOccupiedCells(self):
        return self.occupiedCells

    def isFree(self, r, c):
        return not self.isObstacle(r, c)
    
    def isObstacle(self, r, c):
        return (r,c) in self.occupiedCells
    
    def addObstacle(self, r, c):
        self.occupiedCells.add((r,c))

    def addRandomObstacle(self, nObstacle):
        for _ in range(nObstacle):
            r = random.randint(0, self.nrows-1)
            c = random.randint(0, self.ncols-1)

            while (r,c) in self.occupiedCells:
                r = random.randint(0, self.nrows-1)
                c = random.randint(0, self.ncols-1)

            self.addObstacle(r,c)
    
    def getLengthObstacles(self):
        return len(self.occupiedCells)



    