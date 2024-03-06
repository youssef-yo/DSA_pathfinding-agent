import unittest
import math
from models.path import Path
from generator.graphGenerator import createGraphFromGrid
from generator.pathsGenerator import waitGoalToBeFree

class TestPath(unittest.TestCase):
    def setUp(self):
        self.path = Path((0, 0), (5, 5))
        self.path.addMove(1, (0, 0), (1, 0), 1)
        self.path.addMove(2, (1, 0), (2, 0), 1)
        self.path.addMove(3, (2, 0), (3, 0), 1)
        self.path.addMove(4, (3, 0), (4, 0), 1)
        self.path.addMove(5, (4, 0), (5, 0), 1)
        self.path.addMove(6, (5, 0), (5, 1), 1)
        self.path.addMove(7, (5, 1), (5, 2), 1)
        self.path.addMove(8, (5, 2), (5, 3), 1)
        self.path.addMove(9, (5, 3), (4, 4), math.sqrt(2))
        self.path.addMove(10, (4, 4), (5, 5), math.sqrt(2))

    def test_getInit(self):
        self.assertEqual(self.path.getInit(), (0, 0))

    def test_getGoal(self):
        self.assertEqual(self.path.getGoal(), (5, 5))

    def test_getCost(self):
        self.assertEqual(math.isclose(self.path.getCost(), (8+2*math.sqrt(2))), True)
        
    def test_getLength(self):
        self.assertEqual(self.path.getLength(), 10)

    def test_getMove(self):
        self.assertEqual(self.path.getMove(1).src, (0, 0))
        self.assertEqual(self.path.getMove(1).dst, (1, 0))
        self.assertEqual(self.path.getMove(1).w, 1)

    def test_getMoves(self):
        self.assertEqual(len(self.path.getMoves()), 10)

    def test_checkSameDestination(self):
        self.assertTrue(self.path.checkSameDestination((5, 5), 10))
        self.assertFalse(self.path.checkSameDestination((4, 4), 10))

    def test_checkSeatSwapping(self):
        self.assertTrue(self.path.checkSeatSwapping((5, 5), (4, 4), 10))
        self.assertFalse(self.path.checkSeatSwapping((5, 5), (5, 3), 10))

    def test_checkTrajectories(self):
        self.assertTrue(self.path.checkTrajectories((4, 3), (5, 4), 9)) #(5, 3), (4, 4)
        self.assertFalse(self.path.checkTrajectories((4, 3), (3, 3), 9))

    def test_checkCollision(self):
        self.assertTrue(self.path.checkCollision((4, 3), (5, 4), 9))
        self.assertFalse(self.path.checkCollision((5, 0), (5, 5), 5))

class TestGraphGenerator(unittest.TestCase):
    def test_empty_grid(self):
        grid = []
        graph = createGraphFromGrid(grid)
        self.assertEqual(graph, None)

    def test_grid_with_obstacles(self):
        grid = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        graph = createGraphFromGrid(grid)
        self.assertEqual(len(graph.getNodes()), 8)

    def test_grid_with_all_obstacles(self):
        grid = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        graph = createGraphFromGrid(grid)
        self.assertEqual(len(graph.getNodes()), 0)

    def test_grid_without_obstacles(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        graph = createGraphFromGrid(grid)
        self.assertEqual(len(graph.getNodes()), 9)
    
    def test_contain_vertex(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        graph = createGraphFromGrid(grid)
        self.assertEqual(graph.containsVertex((0, 0)), True)

    def test_addEdge(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        graph = createGraphFromGrid(grid)
        self.assertEqual(len(graph.getNeighbors((0, 0))), 4)

class TestPathsGenerator(unittest.TestCase):
    def test_waitGoalToBeFree(self):
        # Test case 1: No illegal moves
        move = None
        path = None
        paths = []
        t = 0
        tMax = 10
        current = None

        expected_t = 0
        expected_path = None

        result_t, result_path = waitGoalToBeFree(move, path, paths, t, tMax, current)

        self.assertEqual(result_t, expected_t)
        self.assertEqual(result_path, expected_path)

        # Test case 2: Illegal move exists
        move = None
        path = None
        paths = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
        t = 0
        tMax = 10
        current = (1, 1)

        expected_t = 2
        expected_path = None

        result_t, result_path = waitGoalToBeFree(move, path, paths, t, tMax, current)

        self.assertEqual(result_t, expected_t)
        self.assertEqual(result_path, expected_path)

if __name__ == '__main__':
    unittest.main()