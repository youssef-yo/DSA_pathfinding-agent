import models.graph as Graph

class Instance:

    def __init__(self, grid, graph: Graph, paths, init, goal, max, maxTimeGoalOccupied) -> None:
        self.grid = grid
        self.graph = graph
        self.paths = paths
        self.init = init
        self.goal = goal
        self.maxTimeGoalOccupied = maxTimeGoalOccupied
        self.maxLengthNewAgent = max

    def getGrid(self):
        return self.grid
    
    def getGraph(self): 
        return self.graph

    def getPaths(self):
        return self.paths
    
    def getInit(self):
        return self.init
    
    def getGoal(self):
        return self.goal 
    
    def getMaxLengthNewAgent(self):
        return self.maxLengthNewAgent
    
    def getMaxTimeGoalOccupied(self):
        return self.maxTimeGoalOccupied
    
    def addPath(self, path):
        self.paths.append(path)
