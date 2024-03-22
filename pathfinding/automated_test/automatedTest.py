import gc
import math
import random
import numpy as np
from generator.informationGenerator import Information
from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal

class AutomatedTest():
    def __init__(self):
        self.data = []
        # self.seed = 1234

        # self.nrows = 0
        # self.ncols = 0
        # self.freeCellRatio = 0.0
        # self.agglomerationFactor = 0.0
        # self.nAgents = 0
        # self.max = 0
        # self.limitLengthExistingPaths = 0

    def freeMemory(self):
        gc.collect()

    def addRow(self, rowData):
        self.data.append(rowData)

    def executeEvaluationTest(self, seed):
        global SEED, NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS
        #TODO: generate random or ask?
        SEED = seed
        
        
        gridDimension = [250]
        # for i in range(1,6): # lista al posto di range [1, 2, 5, 10, 20, 100]
        for dim in gridDimension: # lista al posto di range [1, 2, 5, 10, 20, 100]
            NROWS = NCOLS = dim

            FREE_CELL_RATIO = 0.7
            AGGLOMERATION_FACTOR = 0.2
            
            # availableCells = NROWS * NCOLS * FREE_CELL_RATIO 
            LIMIT_LENGTH_EXISTING_PATHS = max(int((NROWS) * 0.5), 1)
            MAX = int(math.ceil((NROWS + NCOLS + LIMIT_LENGTH_EXISTING_PATHS)))

            for factorAgent in np.arange(0.4, 1.5, 0.2):
                # N_AGENTS = int(math.ceil(availableCells * factorAgent))
                N_AGENTS = int(math.ceil(NROWS* factorAgent))               

                # # TODO: fare un for anche per coefficiente di limitLengthExistingPaths
                # # LIMIT_LENGTH_EXISTING_PATHS = max(int((N_AGENTS) * 0.8), 1)
                # LIMIT_LENGTH_EXISTING_PATHS = max(int((N_AGENTS) * 0.8), 1)
                # # MAX = int(math.ceil((availableCells + LIMIT_LENGTH_EXISTING_PATHS) * 0.1))
                # MAX = int(math.ceil((NROWS + NCOLS + LIMIT_LENGTH_EXISTING_PATHS)))

                print("I: ", dim, "NROWS: ", NROWS, " N_AGENTS: ", N_AGENTS, " FREE_CELL_RATIO: ", FREE_CELL_RATIO, " AGGLOMERATION_FACTOR: ", AGGLOMERATION_FACTOR, " MAX: ", MAX, " LIMIT_LENGTH_EXISTING_PATHS: ", LIMIT_LENGTH_EXISTING_PATHS)
                
                for iRun in range(1,5):
                    print("iRun: ", iRun)
                    self.defineCombination()
            
            N_AGENTS = NROWS
            for limitLength in range(0.1, 0.6, 0.1):
                LIMIT_LENGTH_EXISTING_PATHS = max(int((N_AGENTS) * limitLength), 1)
                MAX = int(math.ceil((NROWS + NCOLS + LIMIT_LENGTH_EXISTING_PATHS)))
                for iRun in range(1,5):
                    print("iRun: ", iRun)
                    self.defineCombination()
        return self.data
    

    # def updateInformationValue(self, information, informationInstance):
    #     information.setExecutionTime(information.getExecutionTime() + informationInstance.getExecutionTime())
    #     information.setTotalMemory(information.getTotalMemory() + informationInstance.getTotalMemory())
    #     information.setPeakMemory(information.getPeakMemory() + informationInstance.getPeakMemory())

    def executeReachGoal(self, typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, information, informationInstance):
        path, minimumSpanningTree, closedSet = reachGoal(instance, useRelaxedPath)
        if path:
            instance.addPath(path)
            instance.setIsNewAgentAdded(True)

            information.stopMonitoring()
            information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
            # self.updateInformationValue(information, informationInstance)
            # information.saveInformationToFile()
            self.addRow(information.getRowInformation(typeRun, informationInstance))

        else:
            instance.setIsNewAgentAdded(False)
            print("No path found for new agent")
            information.stopMonitoring()
            # add time and memory
            information.setFailValues(FREE_CELL_RATIO, AGGLOMERATION_FACTOR, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
            # self.updateInformationValue(information, informationInstance)

            # information.saveFailInformationToFile(NROWS, NCOLS, MAX)
            self.addRow(information.getFailRowInformation(typeRun, NROWS, NCOLS, MAX, informationInstance))

    def runSingleSimultationWithInstance(self, typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, informationInstance):
        # rimuovo il percorso del new agent dall'istanza che mi è stata passata
        if instance.getIsNewAgentAdded():
            instance.removeLastPath()

        information = Information(SEED)
        information.startMonitoring()

        self.executeReachGoal(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, information, informationInstance)
        
        return instance

    def createInstance(self, useReachGoalExistingAgents, useRelaxedPath = False):
        information = Information(SEED)
        information.startMonitoring()

        goalsInits = None
        instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        
        information.stopMonitoring()

        return instance, information

    def runSingleSimulation(self, typeRun, instance, useReachGoalExistingAgents, useRelaxedPath):
        information = Information(SEED)
        information.startMonitoring()
        
        # al momento non ho un'istanza, quindi la genero
        goalsInits = None
        instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        
        # se non sono riuscito a generare l'istanza, termino
        if not instance:
            print("Could not create instance.")
            information.stopMonitoring()
            information.setFailValues(FREE_CELL_RATIO, AGGLOMERATION_FACTOR, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
            # information.saveFailInformationToFile(NROWS, NCOLS, MAX)
            self.addRow(information.getFailRowInformation(typeRun, NROWS, NCOLS, MAX))

        # l'istanza è stata generata correttamente
        else:
            self.executeReachGoal(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, information)
        
        return instance
    
    def defineCombination(self):
        instance = None

        # potremmo fare anche così:
        # creo prima l'istanza sono riuscito? si, esegui la simulazione, no, termina
        # Mi salvo il tempo neccessario per creare l'istanza, la aggiungo poi al tempo per eseguire ogni singola simulazione
        useReachGoalExistingAgents = False
        instance, informationInstance = self.createInstance(useReachGoalExistingAgents)
        # timeToInstance = information.getExecutionTime()
        # totalMemory = information.getTotalMemory()
        # pickMemory = information.getPeakMemory()

        self.freeMemory()

        if not instance:
            print("Instance not created")
        else:
            useRelaxedPath = False     
            print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
            typeRun = 0
            self.runSingleSimultationWithInstance(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, informationInstance)
            self.freeMemory()

            useRelaxedPath = True  
            print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
            typeRun = 1
            self.runSingleSimultationWithInstance(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath, informationInstance)
            self.freeMemory()



        ## TODO: RUN SECOND COMBINATION ONLY IF FIRST COMBINATION CREATED INSTANCE SUCCESSFULLY

        # print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        # typeRun = 0
        # instance = self.runSingleSimulation(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # self.freeMemory()
        # #####

        # useReachGoalExistingAgents = False
        # useRelaxedPath = True

        # print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        # typeRun = 1
        # if instance:
        #     instance = self.runSingleSimultationWithInstance(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # else:
        #     print("---->Creating instance for second combination")
        #     instance = self.runSingleSimulation(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # self.freeMemory()
        #####
        
        
        # useReachGoalExistingAgents = True
        # useRelaxedPath = False

        # print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        # typeRun = 2
        # if instance:
        #     instance = self.runSingleSimultationWithInstance(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # else:
        #     instance = self.runSingleSimulation(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # self.freeMemory()
        # #####
        
        # useReachGoalExistingAgents = True
        # useRelaxedPath = True

        # print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        # typeRun = 3
        # if instance:
        #     instance = self.runSingleSimultationWithInstance(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # else:
        #     instance = self.runSingleSimulation(typeRun, instance, useReachGoalExistingAgents, useRelaxedPath)
        # self.freeMemory()


    

