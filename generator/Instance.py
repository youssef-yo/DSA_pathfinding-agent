import Graph

class Instance:

    def __init__(self, graph: Graph, paths, init, goal, max) -> None:
        self.graph = graph
        self.paths = paths
        self.init = init
        self.goal = goal
        self.max = max