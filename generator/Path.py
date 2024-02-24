from typing import Any


class Path:
    def __init__(self) -> None:
        self.path = {} # key = time t as integer, value: (startnode, endnode, weight)
        self.cost = 0
        self.lenght = 0
    
    def getFirstNode(self):
        return self.path[0][0]
    
    def getLastNode(self):
        return self.path[self.lenght-1][1]

    def getCost(self):
        return self.cost
    
    def getLenght(self):
        return self.lenght
    
    def getMove(self, t):
        return self.path.get(t)

    def addMove(self, t, src, dst, w):
        self.path[t] = (src, dst, w)
        self.cost += w
        self.lenght += 1

    def checkSameDestination(self, dst, t):
        if t in self.path:
            if self.path[t][1] == dst:
                return True
        return False

    def checkSeatSwapping(self, dst, t):
        if t in self.path:
            if self.path[t][0] == dst:
                return True
        return False
    
    def checkCollision(self, dst, t):
        return self.checkSameDestination(dst, t) or self.checkSeatSwapping(dst, t)
    
    def printPath(self):
        # print start node end goal node
        print("\n--------------------")
        print("Start node: ", self.getFirstNode())
        print("Goal node: ", self.getLastNode())
        print("Path: ")
        for t in self.path:
            print(t, self.path[t])
