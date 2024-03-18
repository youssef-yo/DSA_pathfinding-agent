# create test for pathfinding

import unittest
from solver import reconstructPath
from models.path import Path
from UI.UI import run
from generator.instanceGenerator import generateInstance
from generator.graphGenerator import createGraphFromGrid   
from solver.reachGoal import reachGoal
from models.grid import Grid
from models.instance import Instance

import math

class TestReconstructPath(unittest.TestCase):    
    def defineGrid(m, n):
        grid = Grid(m, n)

        grid.addObstacle(1, 7)
        grid.addObstacle(2, 1)
        grid.addObstacle(1, 6)
        grid.addObstacle(3, 1)
        grid.addObstacle(4, 1)
        grid.addObstacle(5, 1)
        grid.addObstacle(3, 5)
        grid.addObstacle(4, 5)
        grid.addObstacle(5, 5)
        grid.addObstacle(7, 2)
        grid.addObstacle(7, 3)
        grid.addObstacle(7, 4)

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
    #instance = Instance(grid, graph: Graph, paths, init, goal, max, maxTimeGoalOccupied)

    useRelaxedPath = False
    instance = Instance(grid, graph, paths, init, goal, 40, -1)
    newPath, minSpanningTree, closedSet = reachGoal(instance, useRelaxedPath)
    paths.append(newPath)
    run(grid, paths, minSpanningTree)
