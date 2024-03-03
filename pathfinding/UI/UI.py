import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 

import numpy as np



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

def definePlotPaths(ax, paths):
    # Print the paths on the plot
    for path in paths:
        colors = []
        labels = []
        for i, path in enumerate(paths):
            color = list(np.random.random(size=3))
            colors.append(color)
            for src, dst, _ in path.path.values():
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
    
def run(grid, paths):
    ax = definePlotGrid(grid)
    ax = definePlotPaths(ax, paths)

    plt.grid()
    plt.show()
