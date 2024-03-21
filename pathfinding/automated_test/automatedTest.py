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

    def executeEvaluationTest(self):
        global SEED, NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS
        #TODO: generate random or ask?
        SEED = 1234
        
        for i in range(1,4): # lista al posto di range [1, 2, 5, 10, 20, 100]
            NROWS = NCOLS = i * 5
            FREE_CELL_RATIO = 1 - 0.1 * (i - 1)
            AGGLOMERATION_FACTOR = 1 / i
            availableCells = NROWS * NCOLS * FREE_CELL_RATIO 
            for factorAgent in np.arange(0.1, 0.6, 0.2):
                N_AGENTS = int(math.ceil(availableCells * factorAgent))                 
                LIMIT_LENGTH_EXISTING_PATHS = max(int((availableCells - N_AGENTS) * 0.5), 1)
                MAX = int(math.ceil((availableCells + LIMIT_LENGTH_EXISTING_PATHS) * 0.3))

                print("I: ", i, "NROWS: ", NROWS, " N_AGENTS: ", N_AGENTS, " FREE_CELL_RATIO: ", FREE_CELL_RATIO, " AGGLOMERATION_FACTOR: ", AGGLOMERATION_FACTOR, " MAX: ", MAX, " LIMIT_LENGTH_EXISTING_PATHS: ", LIMIT_LENGTH_EXISTING_PATHS)
                
                self.defineCombination()
        return self.data
    
    def runSingleSimulation(self, typeRun, goalsInits, useReachGoalExistingAgents, useRelaxedPath):
        information = Information(SEED)
        information.startMonitoring()
            
        instance = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_EXISTING_PATHS, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        
        if not instance:
            print("Could not create instance.")
            information.stopMonitoring()
            information.setFailValues(FREE_CELL_RATIO, AGGLOMERATION_FACTOR, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
            # information.saveFailInformationToFile(NROWS, NCOLS, MAX)
            self.addRow(information.getFailRowInformation(typeRun, NROWS, NCOLS, MAX))

        else:
            path, minimumSpanningTree, closedSet = reachGoal(instance, useRelaxedPath)
            if path:
                instance.addPath(path)

                information.stopMonitoring()
                information.setValues(instance, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, path, minimumSpanningTree, closedSet, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
                # information.saveInformationToFile()
                self.addRow(information.getRowInformation(typeRun))

            else:
                print("No path found for new agent")
                information.stopMonitoring()
                information.setFailValues(FREE_CELL_RATIO, AGGLOMERATION_FACTOR, useRelaxedPath, useReachGoalExistingAgents, LIMIT_LENGTH_EXISTING_PATHS)
                # information.saveFailInformationToFile(NROWS, NCOLS, MAX)
                self.addRow(information.getFailRowInformation(typeRun, NROWS, NCOLS, MAX))
        
        return instance
    
    def defineCombination(self):
        goalsInits = None
        useReachGoalExistingAgents = False
        useRelaxedPath = False

        print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        typeRun = 0
        instance = self.runSingleSimulation(typeRun, goalsInits, useReachGoalExistingAgents, useRelaxedPath)

        self.freeMemory()
        #####

        if instance:
            goalsInits = instance.getGoalsInits()
        
        useReachGoalExistingAgents = False
        useRelaxedPath = True

        print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        typeRun = 1
        instance = self.runSingleSimulation(typeRun, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        self.freeMemory()
        #####

        if instance:
            goalsInits = instance.getGoalsInits()
        
        useReachGoalExistingAgents = True
        useRelaxedPath = False

        print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        typeRun = 2
        instance = self.runSingleSimulation(typeRun, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        self.freeMemory()
        #####

        if instance:
            goalsInits = instance.getGoalsInits()
        
        useReachGoalExistingAgents = True
        useRelaxedPath = True

        print("useReachGoalExistingAgents: ", useReachGoalExistingAgents, " useRelaxedPath: ", useRelaxedPath)
        typeRun = 3
        instance = self.runSingleSimulation(typeRun, goalsInits, useReachGoalExistingAgents, useRelaxedPath)
        self.freeMemory()


    

