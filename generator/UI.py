import matplotlib.pyplot as plt
from main import gridGenerator, graphGenerator
from instanceGenerator import main

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


    # ax.grid(True, color='black', linestyle='-', linewidth=1)

    # Call the main function in instanceGenerator.py
    paths = main(2,20, graph)

    # Print the paths on the plot
    for path in paths:
        colors = ['red', 'blue', 'green', 'yellow', 'orange']  # Add more colors if needed
        for i, path in enumerate(paths):
            for src, dst, _ in path.path.values():
                xStart = src[0]
                yStart = src[1]
                xEnd = dst[0]
                yEnd = dst[1]
                # ax.plot([yStart + 0.5, yEnd + 0.5], [xStart + 0.5, xEnd + 0.5], color=colors[i], linewidth=2)
                ax.plot([yStart, yEnd], [xStart, xEnd], color=colors[i], linewidth=2)

        # Add a legend for the paths
        legend_labels = [f'Path {i+1}' for i in range(len(paths))]
        ax.legend(legend_labels)

    plt.grid()
    # Show the updated plot
    plt.show()
    

nrows, ncols = 3, 3
freeCellRatio = 0.8
# Assuming you have a grid generated in gridGenerator
grid = gridGenerator(nrows,ncols, freeCellRatio)
graph = graphGenerator(nrows, ncols, freeCellRatio)
# Plot the grid using the plot_grid function
plot_grid(grid, graph)


