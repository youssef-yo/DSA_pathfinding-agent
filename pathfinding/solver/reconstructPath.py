from models.path import Path 

def reconstructPath(init, goal, P, tStart, tEnd):
    """
    P: dictionary where key is a state <ndoe, time> and value is an array with index 0: the parent node, index 1: the cost
    """

    path = Path(init, goal)
    current = goal
    while tEnd > tStart and P[(current, tEnd)]:
        src = P[(current, tEnd)].getParentNode()
        dst = current
        path.addMove(tEnd-1, src, dst, path.calculateWeight(src, dst)) 

        current = P[(current, tEnd)].getParentNode()
        tEnd -= 1

    return path