
class Information():

    def __init__(self, path, P, closedSet):
        self.path = path
        self.P = P
        self.closedSet = closedSet
        self.waitCounter = self.computeWaitMove(path)

    def computeWaitMove(self, path):
        waitCounter = 0
        for _, move in path.getMoves():
            if move.getSrc() == move.getDst():
                waitCounter += 1
        return waitCounter
            
    def printInformation(self):
        print("Stati in Open (e P): ", len(self.P))
        print("Stati espansi in Closed: ", len(self.closedSet))
        print("Lunghezza del percorso: ", self.path.getLength())
        print("Costo del percorso: ", self.path.getCost())
        print("Numero di wait move: ", self.waitCounter)