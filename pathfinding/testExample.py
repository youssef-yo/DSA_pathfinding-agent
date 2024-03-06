# create test for pathfinding

import unittest
from solver import reconstructPath
from models.path import Path
from UI.UI import run
from generator.instanceGenerator import generateInstance
from generator.graphGenerator import createGraphFromGrid   
from solver.reachGoal import start

import math

class TestReconstructPath(unittest.TestCase):    
    def defineGrid(m, n):
        grid = [[0] * n for _ in range(m)]

        grid[1][7] = 1
        grid[2][1] = 1
        grid[1][6] = 1
        grid[3][1] = 1
        grid[4][1] = 1
        grid[5][1] = 1  
        grid[3][5] = 1
        grid[4][5] = 1
        grid[5][5] = 1
        grid[7][2] = 1
        grid[7][3] = 1
        grid[7][4] = 1

        return grid
        
    cells = [[(8, 0), (7, 1), (6, 2), (5, 2), (4,2)], [(8, 7), (8, 6), (8, 5), (8, 4), (8, 3)], [(1, 1), (2, 2), (3, 3), (3, 4)]]

    paths = []
    moves = []
    for i in range(3):
        paths.append(Path(cells[i][0], cells[i][-1]))
        for j in range(len(cells[i]) - 1):
            paths[i].addMove(j, cells[i][j], cells[i][j+1], paths[i].calculateWeight(cells[i][j], cells[i][j+1]))

    for p in paths:
        p.printPath()

    grid = defineGrid(10, 8)
    init = (9, 3)
    goal = (5, 3)

    graph = createGraphFromGrid(grid)
    #instance = Instance(grid, graph, paths, init, goal, maxLengthPathNewAgent)

    newPath, minSpanningTree = start(graph, paths, init, goal, 40)
    paths.append(newPath)
    run(grid, paths, minSpanningTree)
