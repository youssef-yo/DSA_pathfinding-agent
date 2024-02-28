class Path:
    def __init__(self, firstNode, lastNode) -> None:
        self.path = {} # key = time t as integer, value: (startnode, endnode, weight)
        self.firstNode = firstNode
        self.lastNode = lastNode
        self.cost = 0
        self.length = 0
    
    def getFirstNode(self):
        return self.firstNode
    
    def getLastNode(self):
        return self.lastNode

    def getCost(self):
        return self.cost
    
    def getLength(self):
        return self.length
    
    def getMove(self, t):
        return self.path.get(t)

    def addMove(self, t, src, dst, w):
        self.path[t] = (src, dst, w)
        self.cost += w
        self.length += 1

    def checkSameDestination(self, dst, t):
        if t in self.path:
            if self.path[t][1] == dst:
                return True
        return False

    def checkSeatSwapping(self, src, dst, t):
        if t in self.path:
            if self.path[t][0] == dst and self.path[t][1] == src:
                return True
        return False
    
    def checkTrajectories(self, src, dst, t):
        if t not in self.path:
            return False
        #check that one agent is up/down of the other
        if (self.path[t][0][1] == src[1] and
             abs(self.path[t][0][0]-src[0]) == 1):
            #check if they cross each other
            if (self.path[t][1][1] == dst[1] and
                abs(self.path[t][1][0]-dst[0]) == 1):
                return True
        #check that one agent is left/right of the other
        if (self.path[t][0][0] == src[0] and
             abs(self.path[t][0][1]-src[1]) == 1):
            #check if they cross each other
            if (self.path[t][1][0] == dst[0] and
                abs(self.path[t][1][1]-dst[1]) == 1):
                return True
        return False
    
    def checkCollision(self, src, dst, t):
        return self.checkSameDestination(dst, t) or self.checkSeatSwapping(src, dst, t) or self.checkTrajectories(src, dst, t)
    
    def printPath(self):
        # print start node end goal node
        print("\n--------------------")
        print("Start node: ", self.getFirstNode())
        print("Goal node: ", self.getLastNode())
        print("Path: ")
        for t in self.path:
            print(t, self.path[t])
