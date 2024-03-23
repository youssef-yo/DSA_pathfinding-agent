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
        self.isNewAgentAdded = False

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

    def removeLastPath(self):
        self.paths.pop()

    def setIsNewAgentAdded(self, value):
        self.isNewAgentAdded = value
    
    def getIsNewAgentAdded(self):
        return self.isNewAgentAdded
    
    def getGoalsInits(self):
        goalsInits = {}
        for path in self.paths:
            goalsInits[path.getGoal()] = (path.getInit(), -1)