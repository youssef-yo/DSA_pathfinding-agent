import random
from models.Path import Path 

def chooseRandomCell(availableCells):
    return random.choice(availableCells) if len(availableCells) > 0 else None


def createPaths(nAgents, max, graph):
    # for all nAgents we will choose randomly the initial and goal positions
    # The movement of the agents will be random as well

    availableCells = list(graph.adjacent.keys())

    #INIT and GOAL must be different for each agent
    if len(availableCells) < nAgents*2:
        print("Not enough cells to create a path for each agent")
        return []
    
    goals = set()

    for _ in range(nAgents):
        goal = chooseRandomCell(availableCells)
        while goal in goals:
            goal = chooseRandomCell(availableCells)
        goals.add(goal)

    # create path for each agent
    paths = []
    for i in range(nAgents):
        path = Path()

        # init = chooseRandomCell(availableCells)
        # availableCells.remove(init)

        # #TODO: is it right to remove init from avaibleCells? A goal could be the init of another agent
        # goal = chooseRandomCell(availableCells)

        goal = goals.pop()

        init = chooseRandomCell(availableCells)
        while init[0] == goal[0] and init[1] == goal[1]:
            print("Init and goal of agents: ", i, " are the same")
            print(init)
            print(goal)
            print(availableCells)
            print("----")
            init = chooseRandomCell(availableCells)
        availableCells.remove(init)

        current = init
        # create random path from init to goal
        t = 0   
        while t < max:
            availableMoves = graph.adjacent[current] # value: list of tuple, where a tuple contains (dst_node, weight)

            for p in paths:
                for edge in availableMoves:
                    if p.checkCollision(current, edge.dst, t):
                        availableMoves.remove(edge)

            #TODO: we need to have a path for all the agents so this break is not correct
            if len(availableMoves) == 0:
                print("No more moves available for agent ", i, " at time ", t)
                break

            # choose a random move
            move = random.choice(availableMoves)

            path.addMove(t, current, move.dst, move.weight)
            current = move.dst
            t += 1
            if current == goal:
                break
        
        paths.append(path)

    for path in paths:
        path.printPath()
    
    return paths


# nrows, ncols = 3, 3
# freeCellRatio = 0.8
# # these variables will be all parameters of the instance

# graph = graphGenerator(nrows, ncols, freeCellRatio)
# main(2, 20, graph)


