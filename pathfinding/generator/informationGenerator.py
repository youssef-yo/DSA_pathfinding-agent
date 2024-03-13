import uuid
import os

class Information():

    def __init__(self, instance, freeCellRatio, agglomerationFactor, path, P, closedSet, executionTime, memoryUsage, relaxedPath, reachGoalExistingAgents):
        self.instance = instance
        self.freeCellRatio = freeCellRatio
        self.agglomerationFactor = agglomerationFactor
        self.path = path
        self.P = P
        self.closedSet = closedSet
        self.waitCounter = self.computeWaitMove(path)
        self.executionTime = executionTime
        self.totalMemory = self.computeMemoryUsage(memoryUsage)
        self.relaxedPath = relaxedPath
        self.reachGoalExistingAgents = reachGoalExistingAgents

    def computeWaitMove(self, path):
        waitCounter = 0
        for _, move in path.getMoves():
            if move.getSrc() == move.getDst():
                waitCounter += 1
        return waitCounter

    def computeMemoryUsage(self, memoryUsage):
        return sum(stat.size for stat in memoryUsage) / 1024
    
    def printInformation(self):
        if self.relaxedPath:
            print("Relaxed path UTILIZZATO")
        else:
            print("Relaxed path NON UTILIZZATO")

        if self.reachGoalExistingAgents:
            print("Reach goal UTILIZZATO per gli agenti preesistenti")
        else:
            print("Reach goal NON UTILIZZATO per gli agenti preesistenti")

        print("Numero di righe: ", self.instance.getGrid().getNrows())
        print("Numero di colonne: ", self.instance.getGrid().getNcols())
        print("Rapporto di celle libere: ", self.freeCellRatio)
        print("Fattore di agglomerazione: ", self.agglomerationFactor)
        print("Numero di agenti preesistenti: ", len(self.instance.getPaths()) - 1)
        print("Valore orizzonte temporale max: ", self.instance.getMaxLengthNewAgent())

        print("Stati in Open (e P): ", len(self.P))
        print("Stati espansi in Closed: ", len(self.closedSet))
        print("Lunghezza del percorso: ", self.path.getLength())
        print("Costo del percorso: ", self.path.getCost())
        print("Numero di wait move: ", self.waitCounter)
        print("Tempo di esecuzione: ", self.executionTime)
        print("Utilizzo di memoria: ", self.totalMemory , "KB")
    
    def saveInformationToFile(self):

        directory = "output"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, "information_" + str(uuid.uuid4())[:6] + ".txt")
        with open(filename, 'w') as file:
            if self.relaxedPath:
                file.write("Relaxed path UTILIZZATO\n")
            else:
                file.write("Relaxed path NON UTILIZZATO\n")
            
            if self.reachGoalExistingAgents:
                file.write("Reach goal UTILIZZATO per gli agenti preesistenti\n")
            else:
                file.write("Reach goal NON UTILIZZATO per gli agenti preesistenti\n")

            file.write("Numero di righe: " + str(self.instance.getGrid().getNrows()) + "\n")
            file.write("Numero di colonne: " + str(self.instance.getGrid().getNcols()) + "\n")
            file.write("Rapporto di celle libere: " + str(self.freeCellRatio) + "\n")
            file.write("Fattore di agglomerazione: " + str(self.agglomerationFactor) + "\n")
            file.write("Numero di agenti preesistenti: " + str(len(self.instance.getPaths()) - 1) + "\n")
            file.write("Valore orizzonte temporale max: " + str(self.instance.getMaxLengthNewAgent()) + "\n")

            file.write("Stati in Open (e P): " + str(len(self.P)) + "\n")
            file.write("Stati espansi in Closed: " + str(len(self.closedSet)) + "\n")
            file.write("Lunghezza del percorso: " + str(self.path.getLength()) + "\n")
            file.write("Costo del percorso: " + str(self.path.getCost()) + "\n")
            file.write("Numero di wait move: " + str(self.waitCounter) + "\n")
            file.write("Tempo di esecuzione: " + str(self.executionTime) + "\n")
            file.write("Utilizzo di memoria: " + str(self.totalMemory) + " KB\n")