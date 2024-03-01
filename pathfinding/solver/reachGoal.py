from models.state import State
import random

def start(graph, paths, init, goal, max):
    print(" ------------- ")
    print("NEW AGENT (init, goal): (", init, ", ", goal, ")")

    path = reachGoal(graph, paths, init, goal, max)

    if not path:
        print("No path found for new agent")
        return None
    else:
        print("!!!! Path found for new agent")
        path.printPath()
        
        return path
        
def reachGoal(graph, paths, init, goal, max):
    # implement A* algorithm
    import heapq
    from .reconstructPath import reconstructPath

    def calculateHeuristic(graph):
        # implement BFS algorithm
        # calculate minimum distance from vertex v to goal g
        def bfs(v, g):
            visited = set()
            queue = []
            queue.append((v, 0))

            while queue:
                node, distance = queue.pop(0)
                if node == g:
                    return distance

                if node not in visited:
                    visited.add(node)
                    for neighbor, weight in graph.getNeighbors(node):
                        queue.append((neighbor, distance + 1))
            return float('inf')

        


        # as heuristic use BFS to fine the shortest path from init to goal for each agent. 
        h = dict() # key = vertex v, goal g, value = bfs(v, g)
        for v in graph.adjacent.keys():
            h[(v, goal)] = bfs(v, goal)

        return h
        

    # implement A* algorithm
    def a_star(graph, paths, init, goalNode):
        import heapq

        # initialize the open and closed sets
        open_set = []
        closed_set = set() # set o tuples (node, time)
        stateList = dict() # list of states, we use it instead of P. Each state has a pointer to parent state
        heuristic = calculateHeuristic(graph)

        # create a dictionary to store the g-score for each node
        for t in range(max):
            for v in graph.adjacent.keys():
                stateList[(v, t)] = State(v, t, None, float('inf'), float('inf'))

        stateList[(init, 0)].g = 0
        stateList[(init, 0)].f = heuristic[(init, goalNode)]

        # push the initial node into the open set with its f-score
        heapq.heappush(open_set, (stateList[(init, 0)].f, stateList[(init, 0)]))

        while open_set:
            # get the node with the lowest f-score from the open set
            currentState = heapq.heappop(open_set)[1]
            closed_set.add((currentState.getNode(), currentState.getTime()))

            # check if the current node is the goal
            if currentState.getNode() == goalNode:
                # reconstruct the path from the initial node to the goal
                return reconstructPath(init, goalNode, stateList, currentState.getTime())

            if currentState.getTime() < max:
                # explore the neighbors of the current node
                for neighbor, weight in graph.getNeighbors(currentState.getNode()):
                    #neighborState = stateList[(neighbor, currentState.getTime() + 1)]
                    
                    if (neighbor, currentState.getTime() + 1) in closed_set:
                        continue

                    traversable = True
                    for path in paths:
                        if path.checkCollision(currentState.getNode(), neighbor, currentState.getTime() + 1):
                            traversable = False
                            break
                    
                    if traversable:
                        currentGscore = currentState.g + weight

                        if currentGscore < stateList[(neighbor, currentState.getTime() + 1)].g:
                            stateList[(neighbor, currentState.getTime() + 1)].parentState = currentState
                            stateList[(neighbor, currentState.getTime() + 1)].g = currentGscore
                            # TODO: define heuristic
                            stateList[(neighbor, currentState.getTime() + 1)].f = currentGscore + heuristic[(neighbor, goalNode)]
                        
                        if (neighbor, currentState.getTime() + 1) not in [(state[1].getNode(), state[1].getTime()) for state in open_set]:
                            heapq.heappush(open_set, (stateList[(neighbor, currentState.getTime() + 1)].f, stateList[(neighbor, currentState.getTime() + 1)]))
                                                
        # if no path is found, return None
        return None

    return a_star(graph, paths, init, goal)