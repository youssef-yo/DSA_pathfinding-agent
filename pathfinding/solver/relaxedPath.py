import heapq
from .reconstructPath import reconstructBidirectionalPath
from collections import defaultdict 
from models.state import State

#TODO create a class?
# def aStarBidirectional(graph, start, goal, heuristic, maxLengthNewAgent, startTime):
#         # Initialize minimum known distance from each node to start and goal respectively
#         distStart = {start: 0}
#         distGoal = {goal: 0}
        
#         # Heaps for nodes visited from start and goal respectively
#         heapStart = [(0, start)]
#         heapGoal = [(0, goal)]
        
#         # Sets to keep track of visited nodes from start and goal respectively
#         closedStart = set()
#         closedGoal = set()
        
#         t = startTime
#         # While there are nodes to visit from both sides
#         while heapStart and heapGoal:
#             # Start side
#             _, currentStart = heapq.heappop(heapStart)
#             closedStart.add(currentStart)
            
#             # Check if the node has also been visited from the goal side
#             if currentStart in closedGoal:
#                 return currentStart
#                 # return reconstructPath(start, currentStart, distStart, goal, distGoal, startTime)
            
#             # Scan neighbors of the current node
#             for edge in graph.getNeighbors(currentStart):
#                 neighbor = edge.dst
#                 weight = edge.weight
#                 if neighbor not in closedStart:
#                     # Update distance from the start node
#                     new_dist = distStart[currentStart] + weight
#                     if neighbor not in distStart or new_dist < distStart[neighbor]:
#                         distStart[neighbor] = new_dist
#                         heapq.heappush(heapStart, (new_dist + heuristic[(neighbor, goal)], neighbor))
            
#             # Goal side
#             _, currentGoal = heapq.heappop(heapGoal)
#             closedGoal.add(currentGoal)
            
#             # Check if the node has also been visited from the start side
#             if currentGoal in closedStart:
#                 return currentGoal
#                 # return reconstructPath(start, currentStart, distStart, goal, distGoal)
            
#             # Scan neighbors of the current node
#             for edge in graph.getNeighbors(currentGoal):
#                 neighbor = edge.dst
#                 weight = edge.weight
#                 if neighbor not in closedGoal:
#                     # Update distance from the goal node
#                     new_dist = distGoal[currentGoal] + weight
#                     if neighbor not in distGoal or new_dist < distGoal[neighbor]:
#                         distGoal[neighbor] = new_dist
#                         heapq.heappush(heapGoal, (new_dist + heuristic[(neighbor, goal)], neighbor))
        
#         # If no path found, return None
#         return None

def aStarBidirectional(graph, start, goal, heuristic, maxLengthNewAgent, startTime):
        # Initialize minimum known distance from each node to start and goal respectively
        distStart = {start: 0}
        distGoal = {goal: 0}
        
        # Heaps for nodes visited from start and goal respectively
        heapStart = [(0, start, startTime, None)] # (f, node, t, parent)
        heapGoal = [(0, goal, startTime, None)] # (f, node, t, parent)
        
        # Sets to keep track of visited nodes from start and goal respectively
        closedStart = dict()
        closedGoal = dict()
        
        # startP = defaultdict(State)
        # goalP = defaultdict(State)

        # While there are nodes to visit from both sides
        while heapStart and heapGoal:
            # Start side
            _, currentStart, tStart, parentNode = heapq.heappop(heapStart)
            # closedStart.add((currentStart, tStart))
            closedStart[currentStart] = (tStart, parentNode)
            
            # Check if the node has also been visited from the goal side
            if currentStart in closedGoal:
                # return currentStart
                pathStart =  reconstructBidirectionalPath(start, currentStart, closedStart, 0, tStart)
                pathGoal =  reconstructBidirectionalPath(goal, currentStart, closedGoal, 0, tGoal)

                t = tGoal - 1
                currentT = tStart - 1
                while pathGoal.existMoveAtTimeT(t):
                    move = pathGoal.getMove(t)
                    pathStart.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                    t -= 1
                    currentT += 1
                return pathStart
            # Scan neighbors of the current node
            for edge in graph.getNeighbors(currentStart):
                neighbor = edge.dst
                weight = edge.weight
                if neighbor not in closedStart: #TODO da controllare t+1 qua?
                    # Update distance from the start node
                    new_dist = distStart[currentStart] + weight
                    if neighbor not in distStart or new_dist < distStart[neighbor]:
                        distStart[neighbor] = new_dist
                        heapq.heappush(heapStart, (new_dist + heuristic[(neighbor, goal)], neighbor, tStart+1, currentStart))
            
            # Goal side
            _, currentGoal, tGoal, parentGoal = heapq.heappop(heapGoal)
            # closedGoal.add(currentGoal)
            closedGoal[currentGoal] = (tGoal, parentGoal)
            
            # Check if the node has also been visited from the start side
            if currentGoal in closedStart:
                pathStart =  reconstructBidirectionalPath(start, currentStart, closedStart, 0, tStart)
                pathGoal =  reconstructBidirectionalPath(goal, currentStart, closedGoal, 0, tGoal)

                t = tStart - 1
                currentT = tGoal - 1
                while pathStart.existMoveAtTimeT(t):
                    move = pathStart.getMove(t)
                    pathGoal.addMove(currentT + 1, move.getDst(), move.getSrc(), move.getWeight())
                    t -= 1
                    currentT += 1
                return pathGoal
            
            # Scan neighbors of the current node
            for edge in graph.getNeighbors(currentGoal):
                neighbor = edge.dst
                weight = edge.weight
                if neighbor not in closedGoal:
                    # Update distance from the goal node
                    new_dist = distGoal[currentGoal] + weight
                    if neighbor not in distGoal or new_dist < distGoal[neighbor]:
                        distGoal[neighbor] = new_dist
                        heapq.heappush(heapGoal, (new_dist + heuristic[(neighbor, goal)], neighbor, tGoal+1, currentGoal))
        
        # If no path found, return None
        return None