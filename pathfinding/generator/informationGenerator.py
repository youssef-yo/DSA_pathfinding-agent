
class Information():

    def __init__(self, path, P, closedSet, executionTime, memoryUsage):
        self.path = path
        self.P = P
        self.closedSet = closedSet
        self.waitCounter = self.computeWaitMove(path)
        self.executionTime = executionTime
        self.totalMemory = self.computeMemoryUsage(memoryUsage)


    def computeWaitMove(self, path):
        waitCounter = 0
        for _, move in path.getMoves():
            if move.getSrc() == move.getDst():
                waitCounter += 1
        return waitCounter

    def computeMemoryUsage(self, memoryUsage):
        return sum(stat.size for stat in memoryUsage) / 1024

            
    def printInformation(self):
        print("Stati in Open (e P): ", len(self.P))
        print("Stati espansi in Closed: ", len(self.closedSet))
        print("Lunghezza del percorso: ", self.path.getLength())
        print("Costo del percorso: ", self.path.getCost())
        print("Numero di wait move: ", self.waitCounter)
        print("Tempo di esecuzione: ", self.executionTime)
        print("Utilizzo di memoria: ", self.totalMemory , "KB")