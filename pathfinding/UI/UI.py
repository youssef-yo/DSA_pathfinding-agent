import matplotlib.pyplot as plt
from generator.main import gridGenerator, graphGeneratorFromGrid
from generator.instanceGenerator import createPaths
import numpy as np

def plot_grid(grid, graph):
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


    # ax.grid(True, color='black', linestyle='-', linewidth=1)

    # Call the main function in instanceGenerator.py
    paths = createPaths(4,20, graph)

    # Print the paths on the plot
    for path in paths:
        colors = ['red', 'blue', 'green', 'yellow', 'orange']  # Add more colors if needed
        for i, path in enumerate(paths):
            for src, dst, _ in path.path.values():
                xStart = src[0]
                yStart = src[1]
                xEnd = dst[0]
                yEnd = dst[1]

                if (xStart, yStart) == path.getFirstNode():
                    ax.plot(yStart + 0.5, xStart + 0.5, marker='*', markersize=10, color=colors[i])
                if (xEnd, yEnd) == path.getLastNode():
                    ax.plot(yEnd + 0.5, xEnd + 0.5, marker='^', markersize=10, color=colors[i])
                ax.plot([yStart + 0.5, yEnd + 0.5], [xStart + 0.5, xEnd + 0.5], color=colors[i], linewidth=2)
                # ax.plot([yStart, yEnd], [xStart, xEnd], color=colors[i], linewidth=2)

        # Add a legend for the paths
        legend_labels = [f'Path {i+1}' for i in range(len(paths))]
        ax.legend(legend_labels)

    plt.grid()
    # Show the updated plot
    plt.show()
    
def run():
    nrows, ncols = 5, 5
    freeCellRatio = 0.6
    # Assuming you have a grid generated in gridGenerator
    grid = gridGenerator(nrows,ncols, freeCellRatio)

    graph = graphGeneratorFromGrid(grid)

    graph.printGraph()
    # Plot the grid using the plot_grid function
    plot_grid(grid, graph)
