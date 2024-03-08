import math 

class Move:
    def __init__(self, src, dst, w) -> None:
        self.src = src
        self.dst = dst
        self.w = w

    def __str__(self):
        return "(" + str(self.src) + "," + str(self.dst) + "," + str(self.w) + ")"
    
    def getSrc(self):
        return self.src
    
    def getDst(self):
        return self.dst
    
    def getWeight(self):
        return self.w   


class Path:
    def __init__(self, init, goal) -> None:
        self.moves = {} # key = time t as integer, value: Move(src, dst, weight)
        self.init = init
        self.goal = goal
        self.cost = 0
        self.length = 0
    
    def getInit(self):
        return self.init
    
    def getGoal(self):
        return self.goal

    def getCost(self):
        return self.cost
    
    def getLength(self):
        return self.length
    
    def getMove(self, t):
        #TODO: throw exception if t not in self.path ?
        return self.moves.get(t)

    def getMoves(self):
        return self.moves

    def addMove(self, t, src, dst, w):
        self.moves[t] = Move(src, dst, w)
        self.cost += w
        self.length += 1

    def checkSameDestination(self, dst, t):
        if t in self.moves:
            if self.getMove(t).dst == dst:
                return True
        return False

    def checkSeatSwapping(self, src, dst, t):
        if t in self.moves:
            if self.getMove(t).src == dst and self.getMove(t).dst == src:
                return True
        return False
    
    def checkTrajectories(self, src, dst, t):
        if t not in self.moves:
            return False
        
        src_move_x = self.getMove(t).src[0]
        src_move_y = self.getMove(t).src[1]
        dst_move_x = self.getMove(t).dst[0]
        dst_move_y = self.getMove(t).dst[1]

        #check that one agent is up/down of the other
        if (src_move_y == src[1] and
             abs(src_move_x-src[0]) == 1):
            #check if they cross each other
            if (dst_move_y == dst[1] and
                abs(dst_move_x-dst[0]) == 1):
                return True
            
        #check that one agent is left/right of the other
        if (src_move_x == src[0] and
             abs(src_move_y-src[1]) == 1):
            #check if they cross each other
            if (dst_move_x == dst[0] and
                abs(dst_move_y-dst[1]) == 1):
                return True
            
        return False
    
    def checkCollision(self, src, dst, t):
        return self.checkSameDestination(dst, t) or self.checkSeatSwapping(src, dst, t) or self.checkTrajectories(src, dst, t)
    

    def concatenatePaths(self, path2):
        for t, move in path2.getMoves().items():
            self.addMove(t, move.src, move.dst, move.w)

        self.goal = path2.getGoal()

    @staticmethod
    def calculateWeight(src, dst):
        cardinalMoves = Path.getCardinalMoves() # Cardinal moves and self-loop have cost = 1
        diagonalMoves = Path.getDiagonalMoves() # Diagonal moves have cost = sqrt(2)

        if (dst[0] - src[0], dst[1] - src[1]) in cardinalMoves:
            return 1
        elif (dst[0] - src[0], dst[1] - src[1]) in diagonalMoves:
            return math.sqrt(2)
    
    @staticmethod
    def getCardinalMoves():
        return [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
    
    @staticmethod
    def getDiagonalMoves():
        return [(1,1), (-1,1), (-1,-1), (1,-1)]

    def printPath(self):
        # print start node end goal node
        print("\n--------------------")
        print("Start node: ", self.getInit())
        print("Goal node: ", self.getGoal())
        print("Path: ")
        t = 0
        while t < self.length:
            print(t, self.moves[t])
            t += 1
