from main import gridGenerator
import random
from Path import Path 

def chooseRandomStart(availabeCells):
    if len(availabeCells) == 0:
        return None
    
    randomCell = random.choice(availabeCells)
    availabeCells.remove(randomCell)

    return randomCell

def chooseRandomGoal(availabeCells):
    if len(availabeCells) == 0:
        return None
    
    randomCell = random.choice(availabeCells)
    # availabeCells.remove(randomCell) 
    # we don't remove the goal cell from the list of available cells because it could be the initial position of another agent
    
    return randomCell

def main(n_agents, max):
    # for all n_agents we will choose randomly the initial and goal positions
    # The mowement of the agents will be random as well

    nrows, ncols = 3, 3
    freeCellRatio = 0.8
    # this variables will be all parameters of the instance
    
    graph = gridGenerator(nrows, ncols, freeCellRatio)

    availableCells = [] # list of tuples (r,c) where there are no obstacles
    for i in range(nrows):
        for j in range(ncols):
            if graph.containsVertex((i,j)):
                availableCells.append((i,j))

    # create path for each agent
    paths = []
    for i in range(n_agents):
        path = Path()
        init = chooseRandomStart(availableCells)
        goal = chooseRandomGoal(availableCells)

        current = init
        # create random path from init to goal
        t = 0   
        while t < max:
            availableMoves = graph.adjacent[current] # value: list of tuple, where a tuple contains (dst_node, weight)

            for p in paths:
                found = False
                edgeToRemove = None
                
                

                for edge in availableMoves:
                    if edge.isNeighbor(p.getMove(t)[1]):
                        edgeToRemove = edge
                        found = True
                        break

                if p.getMove(t) and found:
                    availableMoves.remove(edgeToRemove)

            if len(availableMoves) == 0:
                print("No more moves available for agent ", i, " at time ", t)
                break

            # choose a random move
            move = random.choice(availableMoves)

            path.addMove(t, init, move.neighbor, move.weight)
            current = move.neighbor
            t += 1
            if current == goal:
                break
        
        paths.append(path)

    for path in paths:
        path.printPath()


main(2, 30)


