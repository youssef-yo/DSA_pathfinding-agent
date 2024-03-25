import collections

def findIslands(grid):
    obstacles = grid.getObstacleCells()

    if len(obstacles) == 0:
        return 

    rows, cols = grid.getNrows(), grid.getNcols()

    visit = set()
    islands = []
    nIslands = 0

    def bfs(r, c):
        q = collections.deque()
        visit.add((r, c))
        q.append((r, c))
        island = set()
        island.add((r, c))

        while q:
            row, col = q.popleft()
            directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]

            for dr, dc, in directions:
                r, c = row + dr,  col + dc
                if (r in range(rows) and
                    c in range(cols) and
                    (r, c) not in obstacles and
                    (r, c) not in visit):
                    q.append((r, c))
                    visit.add((r, c))
                    island.add((r, c))
        islands.append(island)

    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in obstacles and (r, c) not in visit:
                bfs(r, c)
                nIslands += 1
    return islands

def checkReachability(init, goal, islands):   
    for island in islands:
        if (init in island and goal not in island) or (goal in island and init not in island):
            return False
    return True