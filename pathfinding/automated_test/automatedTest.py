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
        
        
        gridDimension = [5, 10, 25, 50, 100, 250]
        for dim in gridDimension:
            NROWS = NCOLS = dim

            FREE_CELL_RATIO = 0.7
            AGGLOMERATION_FACTOR = 0.2
            
            LIMIT_LENGTH_EXISTING_PATHS = max(int((NROWS) * 0.5), 1)
            MAX = int(math.ceil((NROWS + NCOLS + LIMIT_LENGTH_EXISTING_PATHS)))

            for factorAgent in np.arange(0.4, 1.5, 0.2):
                N_AGENTS = int(math.ceil(NROWS* factorAgent))               

                print("I: ", dim, "NROWS: ", NROWS, " N_AGENTS: ", N_AGENTS, " FREE_CELL_RATIO: ", FREE_CELL_RATIO, " AGGLOMERATION_FACTOR: ", AGGLOMERATION_FACTOR, " MAX: ", MAX, " LIMIT_LENGTH_EXISTING_PATHS: ", LIMIT_LENGTH_EXISTING_PATHS)
                
                for iRun in range(1,5):
                    print("iRun: ", iRun)
                    self.defineCombination()
            
            N_AGENTS = NROWS
            for limitLength in np.arange(0.1, 0.6, 0.1):
                LIMIT_LENGTH_EXISTING_PATHS = max(int(math.ceil((N_AGENTS) * limitLength)), 1)
                MAX = int(math.ceil((NROWS + NCOLS + LIMIT_LENGTH_EXISTING_PATHS)))

                print("I: ", dim, "NROWS: ", NROWS, " N_AGENTS: ", N_AGENTS, " FREE_CELL_RATIO: ", FREE_CELL_RATIO, " AGGLOMERATION_FACTOR: ", AGGLOMERATION_FACTOR, " MAX: ", MAX, " LIMIT_LENGTH_EXISTING_PATHS: ", LIMIT_LENGTH_EXISTING_PATHS)
                
                for iRun in range(1,5):
                    print("iRun: ", iRun)
                    self.defineCombination()
        return self.data

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

        useReachGoalExistingAgents = False
        instance, informationInstance = self.createInstance(useReachGoalExistingAgents)

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

    

