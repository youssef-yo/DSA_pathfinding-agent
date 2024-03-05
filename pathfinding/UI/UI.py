import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 
import networkx as nx

import numpy as np

def drawTree(minimumSpanningTree, path):
    G = nx.DiGraph()

    for state, value in minimumSpanningTree.items():
        parent = value.parentState.getNode() if value.parentState is not None else None
        if parent is not None:
            G.add_edge(parent, state[0])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=8, arrows=True)

    # Draw nodes in path in red
    for move in path.getMoves().values():
        src = move.src
        dst = move.dst
        nx.draw_networkx_nodes(G, pos, nodelist=[src, dst], node_color='red', node_size=500)

    plt.show()

def definePlotGrid(grid):
    # Extract the dimensions of the grid
    rows = len(grid)
    cols = len(grid[0])

    # Create a figure and axis object
    fig, ax = plt.subplots()

    # Plot the grid
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='black'))
            else:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, color='white', fill=False))

    # Set the aspect ratio and limits of the plot
    ax.set_aspect('equal')
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    ax.set_xticks(np.arange(0, cols + 1, 1))
    ax.set_yticks(np.arange(0, rows + 1, 1))

    return ax

def plotPathsStepByStep(ax, paths):
    # Print the paths on the plot one move at a time
    plt.grid()

    colors = []
    labels = []
    #plot all init and goal
    for i, path in enumerate(paths):
        color = list(np.random.random(size=3))
        colors.append(color)
        if (path.getInit() is not None):
            ax.plot(path.getInit()[1] + 0.5, path.getInit()[0] + 0.5, marker='*', markersize=10, color=color)
        if (path.getGoal() is not None):
            ax.plot(path.getGoal()[1] + 0.5, path.getGoal()[0] + 0.5, marker='^', markersize=10, color=color)
        if path == paths[-1]:
            labels.append(mpatches.Patch(color=colors[i], label='New Agent'))
        else:
            labels.append(mpatches.Patch(color=colors[i], label=f'Agent {i+1}'))
    
    plt.legend(handles=labels, bbox_to_anchor = (1.25, 0.6), loc='center right')

    t = 0
    keepGoing = True
    while keepGoing:
        plt.title(f'Time step {t}')

        keepGoing = False
        for i, path in enumerate(paths):
            move = path.getMove(t)
            if move is not None:
                keepGoing = True

                src = move.src
                dst = move.dst
                xStart = src[0]
                yStart = src[1]
                xEnd = dst[0]
                yEnd = dst[1]

                ax.plot([yStart + 0.5, yEnd + 0.5], [xStart + 0.5, xEnd + 0.5], color=colors[i], linewidth=2)
        t += 1
        plt.pause(0.2)
    plt.title(f'END at t={t}')
    return ax

def definePlotPaths(ax, paths):
    # Print the paths on the plot
    plt.grid()
    for path in paths:
        colors = []
        labels = []
        for i, path in enumerate(paths):
            color = list(np.random.random(size=3))
            colors.append(color)
            for move in path.getMoves().values():
                src = move.src
                dst = move.dst
                
                xStart = src[0]
                yStart = src[1]
                xEnd = dst[0]
                yEnd = dst[1]

                if (xStart, yStart) == path.getInit():
                    ax.plot(yStart + 0.5, xStart + 0.5, marker='*', markersize=10, color=colors[i])
                if (xEnd, yEnd) == path.getGoal():
                    ax.plot(yEnd + 0.5, xEnd + 0.5, marker='^', markersize=10, color=colors[i])
                ax.plot([yStart + 0.5, yEnd + 0.5], [xStart + 0.5, xEnd + 0.5], color=colors[i], linewidth=2)

                # Creating legend with color box 
            if path == paths[-1]:
                labels.append(mpatches.Patch(color=colors[i], label='New Agent'))
            else:
                labels.append(mpatches.Patch(color=colors[i], label=f'Agent {i+1}'))
        
        plt.legend(handles=labels, bbox_to_anchor = (1.25, 0.6), loc='center right')
 

        return ax
    
def run(grid, paths, minimumSpanningTree):
    # drawTree(minimumSpanningTree, paths[-1])
    
    ax = definePlotGrid(grid)
    # ax = definePlotPaths(ax, paths)
    ax = plotPathsStepByStep(ax, paths)

    plt.show()
