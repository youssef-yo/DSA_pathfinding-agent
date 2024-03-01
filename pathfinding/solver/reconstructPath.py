import math
from models.path import Path 

def reconstructPath(init, goal, P, t):
    """
    P: dictionary where key is a state <ndoe, time> and value is an array with index 0: the parent node, index 1: the cost
    """

    path = Path(init, goal)
    current = goal
    while t > 0 and P[(current, t)]:
        src = P[(current, t)].getParentNode()
        dst = current
        path.addMove(t-1, src, dst, getWeight(src, dst)) 

        current = P[(current, t)].getParentNode()
        t -= 1

    return path

# TODO: reduntant code
def getWeight(src, dst):
    cardinalMoves = [(0,0), (-1,0), (1,0), (0,-1), (0,1)] # Cardinal moves and self-loop have cost = 1
    #diagonalMoves = [(1,1), (-1,1), (-1,-1), (1,-1)] # Diagonal moves have cost = sqrt(2)

    if (dst[0] - src[0], dst[1] - src[1]) in cardinalMoves:
        return 1
    else:
        return math.sqrt(2)

