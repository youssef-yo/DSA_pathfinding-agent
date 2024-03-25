import random

class Grid:
    def __init__(self, nrows, ncols) -> None:
        """
        nrows: number of rows
        ncols: number of columns
        freeCells: set of free cells
        """
        self.nrows = nrows
        self.ncols = ncols
        
        self.obstacleCells = set() # 

        self.occupiedCellsInTimeByAgent = dict() # key: cell, value: dict where key is time and value is agent id

    def getNrows(self):
        return self.nrows

    def getNcols(self):
        return self.ncols
    
    def getObstacleCells(self):
        return self.obstacleCells

    def getOccupiedCellsInTimeByAgent(self):
        return self.occupiedCellsInTimeByAgent
    
    def getTimesAndAgentsOccupiedInCell(self, r, c):
        return self.occupiedCellsInTimeByAgent.get((r,c), dict())

    def addTimeOccupiedInCellByAgent(self, cell, t, agent):
        if cell not in self.occupiedCellsInTimeByAgent:
            self.occupiedCellsInTimeByAgent[cell] = {t: agent}

        self.occupiedCellsInTimeByAgent[cell][t].add(agent)

    def getMaxTimeCellOccupied(self, cell):
        if cell in self.occupiedCellsInTimeByAgent:
            return max(self.occupiedCellsInTimeByAgent[cell].keys())
        
        return -1
    
    def isFree(self, r, c):
        return not self.isObstacle(r, c)
    
    def isObstacle(self, r, c):
        return (r,c) in self.obstacleCells
    
    def addObstacle(self, r, c):
        self.obstacleCells.add((r,c))

    def addRandomObstacle(self, nObstacle):
        for _ in range(nObstacle):
            r = random.randint(0, self.nrows-1)
            c = random.randint(0, self.ncols-1)

            while (r,c) in self.obstacleCells:
                r = random.randint(0, self.nrows-1)
                c = random.randint(0, self.ncols-1)

            self.addObstacle(r,c)
    
    def getLengthObstacles(self):
        return len(self.obstacleCells)
    
    #############################

    def getAgentIdInCellAtTimeT(self, cell, t):
        return self.occupiedCellsInTimeByAgent[(cell[0], cell[1])][t]
    
    def checkSameDestination(self, dst, t):    
        # t is relative to the move
        # t = 0 means that the initial move take the agent from position at time 0 to position at time 1
        if t+1 in self.occupiedCellsInTimeByAgent[(dst[0], dst[1])]:
            return True
        
        return False
    
    def checkSeatSwapping(self, src, dst, t):
        # if t in self.moves:
        #     if self.getMove(t).src == dst and self.getMove(t).dst == src:
        #         return True
        # return False

        if t+1 in self.occupiedCellsInTimeByAgent[(src[0], src[1])]:
            agentIdSrc = self.getAgentIdInCellAtTimeT(src, t)
            
            if t in self.occupiedCellsInTimeByAgent[(dst[0], dst[1])]:
                agentIdDst = self.getAgentIdInCellAtTimeT(dst, t)
                
                if agentIdSrc == agentIdDst:
                    return True
        
        return False
    
    def checkTrajectories(self, src, dst, t):   
        directions = [+1, -1]
        for dx in directions:
            tmpSameRow1 = self.occupiedCellsInTimeByAgent.get((src[0], src[1]+dx), None)
            if tmpSameRow1 and t in tmpSameRow1:
                idAgent1 = tmpSameRow1[t]

                tmpSameRow2 = self.occupiedCellsInTimeByAgent.get((dst[0], dst[1]-dx), None)
                if tmpSameRow2 and t in tmpSameRow2 and tmpSameRow2[t] == idAgent1:
                    return True
        
        for dx in directions:
            tmpSameRow1 = self.occupiedCellsInTimeByAgent.get((src[0]+dx, src[1]), None)
            if tmpSameRow1 and t in tmpSameRow1:
                idAgent1 = tmpSameRow1[t]

                tmpSameRow2 = self.occupiedCellsInTimeByAgent.get((dst[0]-dx, dst[1]), None)
                if tmpSameRow2 and t in tmpSameRow2 and tmpSameRow2[t] == idAgent1:
                    return True

        return False
            

    def checkCollision(self, src, dst, t):
        return self.checkSameDestination(dst, t) or self.checkSeatSwapping(src, dst, t) or self.checkTrajectories(src, dst, t)



    