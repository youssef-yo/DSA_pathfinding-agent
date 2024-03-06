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
        path.addMove(t-1, src, dst, path.calculateWeight(src, dst)) 

        current = P[(current, t)].getParentNode()
        t -= 1

    return path