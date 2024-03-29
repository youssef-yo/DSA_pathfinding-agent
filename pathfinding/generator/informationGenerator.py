import uuid
import os
import time
import tracemalloc
import pathlib


class Information():

    def __init__(self, seed):
        self.seed = seed
        self.startTime = None
        self.instance = None
        self.freeCellRatio = None
        self.agglomerationFactor = None
        self.path = None
        self.P = None
        self.closedSet = None
        self.waitCounter = None
        self.executionTime = None
        self.totalMemory = None
        self.peakMemory = None
        self.relaxedPath = None
        self.reachGoalExistingAgents = None
        self.limitLengthExistingPaths = None
        self.lengthExistingPaths = None
        

    def startMonitoring(self):
        self.startTime = self.getCurrentTime()
        tracemalloc.start()

    def stopMonitoring(self):
        self.executionTime = self.getCurrentTime() - self.startTime
        self.totalMemory, self.peakMemory = self.computeMemoryUsage()


    def getCurrentTime(self):
        return time.time()

    def getInstance(self):
        return self.instance
    
    def getFreeCellRatio(self):
        return self.freeCellRatio

    
    def getAgglomerationFactor(self):
        return self.agglomerationFactor
    
    def getPath(self):
        return self.path
    
    def getP(self):
        return self.P
    
    def getClosedSet(self):
        return self.closedSet
    
    def getWaitCounter(self):
        return self.waitCounter
    
    def getExecutionTime(self):
        return self.executionTime
    
    def getTotalMemory(self):
        return self.totalMemory

    def getPeakMemory(self):
        return self.peakMemory
    
    def getRelaxedPath(self):
        return self.relaxedPath
    
    def getReachGoalExistingAgents(self):
        return self.reachGoalExistingAgents
    
    def setSeed(self, seed):   
        self.seed = seed

    def setExecutionTime(self, executionTime):
        self.executionTime = executionTime
    
    def setTotalMemory(self, totalMemory):
        self.totalMemory = totalMemory
    
    def setPeakMemory(self, peakMemory):
        self.peakMemory = peakMemory

    def computeMemoryUsage(self):
        # Stop memory monitoring
        tracedMemory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        avgMemory = tracedMemory[0] / 1000
        peakMemory = tracedMemory[1] / 1000
        return avgMemory, peakMemory
    
    def setValues(self, instance, freeCellRatio, agglomerationFactor, path, P, closedSet, relaxedPath, reachGoalExistingAgents, limitLengthExistingPaths):
        self.instance = instance
        self.freeCellRatio = freeCellRatio
        self.agglomerationFactor = agglomerationFactor
        self.path = path
        self.P = P
        self.closedSet = closedSet
        self.waitCounter = self.computeWaitMove(path)
        self.relaxedPath = relaxedPath
        self.reachGoalExistingAgents = reachGoalExistingAgents
        self.lengthExistingPaths = self.instance.getPaths()[0].getLength()
        self.limitLengthExistingPaths = limitLengthExistingPaths

    def setFailValues(self, freeCellRatio, agglomerationFactor, relaxedPath, reachGoalExistingAgents, limitLengthExistingPaths):
        self.freeCellRatio = freeCellRatio
        self.agglomerationFactor = agglomerationFactor
        self.relaxedPath = relaxedPath
        self.reachGoalExistingAgents = reachGoalExistingAgents
        self.limitLengthExistingPaths = limitLengthExistingPaths

    def computeWaitMove(self, path):
        if not path:
            return None
        waitCounter = 0
        for _, move in path.getMoves():
            if move.getSrc() == move.getDst():
                waitCounter += 1
        return waitCounter
    
    def printInformation(self):
        print("Seed: ", self.seed)
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
        print("Lunghezza Agenti Preesistenti: ", self.lengthExistingPaths)
        print("Lunghezza Max Agenti Preesistenti: ", self.limitLengthExistingPaths)
        for i, p in enumerate(self.instance.getPaths()[:-1]):
            print("Lunghezza Percorso ", i, ":" , p.getLength())

        print("Valore orizzonte temporale max: ", self.instance.getMaxLengthNewAgent())

        print("Init nuovo Agente: ", self.instance.getInit())
        print("Goal nuovo Agente: ", self.instance.getGoal())
        print("Stati in Open (e P): ", len(self.P))
        print("Stati espansi in Closed: ", len(self.closedSet))
        print("Lunghezza del percorso: ", self.path.getLength())
        print("Costo del percorso: ", self.path.getCost())
        print("Numero di wait move: ", self.waitCounter)
        print("Tempo di esecuzione: ", self.executionTime)
        print("Utilizzo di memoria: ", self.totalMemory , "KB")
        print("Picco di memoria: ", self.peakMemory , "KB")
    
    def saveInformationToFile(self):
        directory = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output")
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, "information_" + str(uuid.uuid4())[:6] + ".txt")
        with open(filename, 'w') as file:
            file.write("Seed: " + str(self.seed) + "\n")
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
            file.write("Lunghezza Agenti Preesistenti: " + str(self.lengthExistingPaths) + "\n")
            file.write("Lunghezza Max Agenti Preesistenti: " + str(self.limitLengthExistingPaths) + "\n")
            for i, p in enumerate(self.instance.getPaths()[:-1]):
                file.write("Lunghezza Percorso " + str(i) + ":" + str(p.getLength()) + "\n")
            file.write("Valore orizzonte temporale max: " + str(self.instance.getMaxLengthNewAgent()) + "\n")

            file.write("Init nuovo Agente: " + str(self.instance.getInit()) + "\n")
            file.write("Goal nuovo Agente: " + str(self.instance.getGoal()) + "\n")
            file.write("Stati in Open (e P): " + str(len(self.P)) + "\n")
            file.write("Stati espansi in Closed: " + str(len(self.closedSet)) + "\n")
            file.write("Lunghezza del percorso: " + str(self.path.getLength()) + "\n")
            file.write("Costo del percorso: " + str(self.path.getCost()) + "\n")
            file.write("Numero di wait move: " + str(self.waitCounter) + "\n")
            file.write("Tempo di esecuzione: " + str(self.executionTime) + "\n")
            file.write("Utilizzo di memoria: " + str(self.totalMemory) + " KB\n")
            file.write("Picco di memoria: " + str(self.peakMemory) + " KB\n")
    
    def saveFailInformationToFile(self, nrows, ncols, maxLengthNewAgent):
        directory = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "output")
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = os.path.join(directory, "information_" + str(uuid.uuid4())[:6] + ".txt")
        with open(filename, 'w') as file:
            file.write("FAIL\n")
            file.write("Seed: " + str(self.seed) + "\n")
            if self.relaxedPath:
                file.write("Relaxed path UTILIZZATO\n")
            else:
                file.write("Relaxed path NON UTILIZZATO\n")
            
            if self.reachGoalExistingAgents:
                file.write("Reach goal UTILIZZATO per gli agenti preesistenti\n")
            else:
                file.write("Reach goal NON UTILIZZATO per gli agenti preesistenti\n")

            file.write("Numero di righe: " + str(nrows) + "\n")
            file.write("Numero di colonne: " + str(ncols) + "\n")
            file.write("Rapporto di celle libere: " + str(self.freeCellRatio) + "\n")
            file.write("Fattore di agglomerazione: " + str(self.agglomerationFactor) + "\n")
            file.write("Valore orizzonte temporale max: " + str(maxLengthNewAgent) + "\n")

            file.write("Tempo di esecuzione: " + str(self.executionTime) + "\n")
            file.write("Utilizzo di memoria: " + str(self.totalMemory) + " KB\n")
            file.write("Picco di memoria: " + str(self.peakMemory) + " KB\n")
    
    def getRowInformation(self, typeRun, informationInstance):     
        rowData = {
            'seed': self.seed,
            'type': typeRun,
            'row': self.instance.getGrid().getNrows(),
            'col': self.instance.getGrid().getNcols(),
            'freeCellRatio': self.freeCellRatio,
            'agglomerationFactor': self.agglomerationFactor,
            'nAgents': len(self.instance.getPaths()) - 1,
            'lengthExistingPaths': self.lengthExistingPaths,
            'limitLengthExistingPaths': self.limitLengthExistingPaths,
            'executionTime': self.executionTime,
            'totalMemory': self.totalMemory,
            'peakMemory': self.peakMemory,
            'maxLengthNewAgent': self.instance.getMaxLengthNewAgent(),
            'initNewAgent': self.instance.getInit(),
            'goalNewAgent': self.instance.getGoal(),
            'nStatesVisited': len(self.P),
            'nStatesClosed': len(self.closedSet),
            'pathLength': self.path.getLength(),
            'pathCost': self.path.getCost(),
            'waitCounter': self.waitCounter,
            'executionTimeInstance': informationInstance.getExecutionTime(),
            'totalMemoryInstance': informationInstance.getTotalMemory(),
            'peakMemoryInstance': informationInstance.getPeakMemory()
        }

        return rowData

    def getFailRowInformation(self, typeRun, nrows, ncols, maxLengthNewAgent, informationInstance):     
        rowData = {
            'seed': self.seed,
            'type': typeRun,
            'row': nrows,
            'col': ncols,
            'freeCellRatio': self.freeCellRatio,
            'agglomerationFactor': self.agglomerationFactor,
            'nAgents': None,
            'lengthExistingPaths': None,
            'limitLengthExistingPaths': self.limitLengthExistingPaths,
            'executionTime': self.executionTime,
            'totalMemory': self.totalMemory,
            'peakMemory': self.peakMemory,
            'maxLengthNewAgent': maxLengthNewAgent,
            'initNewAgent': None,
            'goalNewAgent': None,
            'nStatesVisited': None,
            'nStatesClosed': None,
            'pathLength': None,
            'pathCost': None,
            'waitCounter': self.waitCounter,
            'executionTimeInstance': informationInstance.getExecutionTime(),
            'totalMemoryInstance': informationInstance.getTotalMemory(),
            'peakMemoryInstance': informationInstance.getPeakMemory()
        }

        return rowData

    