from models.path import Path 

def reconstructPath(init, goal, P, tStart, tEnd):
    """
    P: dictionary where key is a state <node, time> and value is an array with index 0: the parent node, index 1: the cost
    tStart: start time
    tEnd: end time
    
    Reconstruction of the path from the goal to the init using the parent node of each state in P (Minimum Spanning Tree)
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

def reconstructBidirectionalPath(init, goal, closed, tStart, tEnd):
    
    path = Path(init, goal)
    current = goal
    while tEnd > tStart and closed[current]:
        src = closed[current][1]
        dst = current
        path.addMove(tEnd-1, src, dst, path.calculateWeight(src, dst)) 

        current = closed[current][1]
        tEnd -= 1

    return path

