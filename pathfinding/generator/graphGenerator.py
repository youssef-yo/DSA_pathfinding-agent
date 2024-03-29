import math
from models.graph import Graph
from models.path import Path

def createGraphFromGrid(grid):
    
    if not grid:
        return None
    
    rows, cols = grid.getNrows(), grid.getNcols()

    cardinalMoves = Path.getCardinalMoves() # Cardinal moves and self-loop have cost = 1
    diagonalMoves = Path.getDiagonalMoves() # Diagonal moves have cost = sqrt(2)

    graph = Graph()
    
    for i in range(rows):
        for j in range(cols):
            if not grid.isObstacle(i,j):
                for x,y in cardinalMoves:
                    r = i + x
                    c = j + y

                    if 0 <= r < rows and 0 <= c < cols and grid.isFree(r,c):
                        graph.addEdge((i,j), (r,c), 1)

                for x,y in diagonalMoves:
                    r = i + x
                    c = j + y

                    if 0 <= r < rows and 0 <= c < cols and grid.isFree(r, c):
                        graph.addEdge((i,j), (r,c), math.sqrt(2))
    return graph