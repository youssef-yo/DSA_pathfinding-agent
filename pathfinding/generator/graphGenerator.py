import math
from models.Graph import Graph

def createGraphFromGrid(grid):
    rows, cols = len(grid), len(grid[0])

    cardinalMoves = [(0,0), (-1,0), (1,0), (0,-1), (0,1)] # Cardinal moves and self-loop have cost = 1
    diagonalMoves = [(1,1), (-1,1), (-1,-1), (1,-1)] # Diagonal moves have cost = sqrt(2)

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