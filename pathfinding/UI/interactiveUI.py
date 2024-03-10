import pygame
import numpy as np

# from solver.reachGoal import reachGoal

def drawPaths(window, cell_size, paths):
    for path in paths:
        color = list(np.random.randint(256, size=3))
        for move in path.getMoves().values():
            xStart, yStart = move.getSrc()
            xEnd, yEnd = move.getDst()
            # if (xStart, yStart) == path.getInit():
            #     pygame.draw.line(window, color, ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), 4)
            #     pygame.draw.rect(window, color, ((xStart + 0.5) * cell_size - 2, (yStart + 0.5) * cell_size - 2, 4, 4))
            # if (xEnd, yEnd) == path.getGoal():
            #     pygame.draw.line(window, color, ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), 4)
            #     pygame.draw.polygon(window, color, [(xStart * cell_size, yStart * cell_size), ((xStart + 1) * cell_size, yStart * cell_size), ((xStart + 0.5) * cell_size, (yStart - 0.5) * cell_size)], 0)
            pygame.draw.line(window, color, ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), ((xEnd + 0.5) * cell_size, (yEnd + 0.5) * cell_size), 4)

def initializeGrid(grid, grid_height, grid_width, cell_size, window):
    window.fill((255, 255, 255))
    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] == 1:
                    pygame.draw.rect(window, (0, 0, 0), (i * cell_size, j * cell_size, cell_size, cell_size))

def run_interactive_ui(grid, graph, paths):
    # New Agent variable
    newInit = None
    newGoal = None

    setInit = False
    setGoal = False

    # Initialize Pygame
    pygame.init()

    # Set the dimensions of the grid
    grid_height = len(grid)
    grid_width = len(grid[0])
    cell_size = 50

    # Set the dimensions of the window
    window_width = grid_width * cell_size + 300  # Increased window width to accommodate buttons
    window_height = grid_height * cell_size

    # Create the window
    window = pygame.display.set_mode((window_width, window_height))

    # Set obstacle
    # Plot the grid
    initializeGrid(grid, grid_height, grid_width, cell_size, window)

    # Draw the paths
    paths = paths[0:-1] # TODO: da non fare se si vuole vedere il nuovo path
    
    drawPaths(window, cell_size, paths)
            
    # Create buttons
    button_width = 80
    button_height = 30
    button_padding = 10
    button_x = window_width - button_width - button_padding
    button_y = button_padding

    btnSetInit = pygame.Rect(button_x, button_y, button_width, button_height)
    btnSetGoal = pygame.Rect(button_x, button_y + button_height + button_padding, button_width, button_height)
    btnFindPath = pygame.Rect(button_x, button_y + 3 * (button_height + button_padding), button_width, button_height)
    btnReset = pygame.Rect(button_x, button_y + 2 * (button_height + button_padding), button_width, button_height)

    # Add a text input
    inputRowRect = pygame.Rect(button_x, button_y + 4 * (button_height + button_padding), button_width, button_height)
    inputRowText = ''
    inputRowActive = False

    inputColRect = pygame.Rect(button_x, button_y + 5 * (button_height + button_padding), button_width, button_height)
    inputColText = ''
    inputColActive = False

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouse_pos = pygame.mouse.get_pos()

                # Calculate the cell position based on the mouse position
                cell_x = mouse_pos[0] // cell_size
                cell_y = mouse_pos[1] // cell_size

                if 0 <= cell_x < grid_width and 0 <= cell_y < grid_height:
                    if setInit:
                        if newInit:
                            pygame.draw.rect(window, (255, 255, 255), (newInit[0] * cell_size, newInit[1] * cell_size, cell_size, cell_size))
                        newInit = (cell_x, cell_y)
                        pygame.draw.rect(window, (0, 255, 0), (cell_x * cell_size, cell_y * cell_size, cell_size, cell_size))
                        print(f"New Init: {newInit}")
                        setInit = False
                    if setGoal:
                        if newGoal:
                            pygame.draw.rect(window, (255, 255, 255), (newGoal[0] * cell_size, newGoal[1] * cell_size, cell_size, cell_size))
                        newGoal = (cell_x, cell_y)
                        pygame.draw.rect(window, (255, 0, 0), (cell_x * cell_size, cell_y * cell_size, cell_size, cell_size))
                        print(f"New Goal: {newGoal}")
                        setGoal = False

                    # Set the color of the clicked cell to red
                    # pygame.draw.rect(window, (255, 0, 0), (cell_x * cell_size, cell_y * cell_size, cell_size, cell_size))

                # Check if the buttons are clicked
                if btnSetInit.collidepoint(event.pos):
                    print("Set Init")
                    setInit = True
                    setGoal = False

                if btnSetGoal.collidepoint(event.pos):
                    print("Set Goal")
                    setGoal = True
                    setInit = False

                if btnReset.collidepoint(event.pos):
                    print("Reset")
                    # if newInit:
                    #     pygame.draw.rect(window, (255, 255, 255), (newInit[0] * cell_size, newInit[1] * cell_size, cell_size, cell_size))
                    # if newGoal:
                    #     pygame.draw.rect(window, (255, 255, 255), (newGoal[0] * cell_size, newGoal[1] * cell_size, cell_size, cell_size))
                    initializeGrid(grid, grid_height, grid_width, cell_size, window)

                    drawPaths(window, cell_size, paths)
                    newInit = None
                    newGoal = None
                    setInit = False
                    setGoal = False

                if btnFindPath.collidepoint(event.pos):
                    pass
                    # if not newInit or not newGoal:
                    #     print("First set Init and Goal")
                    # else:
                    #     print("Find Path")
                    #     # # TODO: check for MVC correctness

                    #     # Wait for the controller response
                    #     path, _ = reachGoal(graph, paths, newInit, newGoal, 20, False)

                    #     # Process the response
                    #     if path:
                    #         # Path found, update the grid with the path
                    #         for move in path.getMoves().values():
                                
                    #             xStart, yStart = move.getSrc()
                    #             xEnd, yEnd = move.getDst()
                    #             pygame.draw.line(window, [255, 0, 0], ((xStart + 0.5) * cell_size, (yStart + 0.5) * cell_size), ((xEnd + 0.5) * cell_size, (yEnd + 0.5) * cell_size), 4)
                    #     else:
                    #         # No path found, display an error message
                    #         print("No path found")
                
                if inputRowRect.collidepoint(event.pos):
                    inputRowActive = True
                    inputColActive = False

                if inputColRect.collidepoint(event.pos):
                    inputRowActive = False
                    inputColActive = True

                # Handle text input events
                if event.type == pygame.KEYDOWN:
                    if inputRowActive:
                        if event.key == pygame.K_RETURN:
                            # Process the input row value
                            try:
                                inputRowValue = int(inputRowText)
                                # TODO: Process the input row value
                                print(f"Input Row: {inputRowValue}")
                            except ValueError:
                                print("Invalid input for row")
                            inputRowText = ''
                            inputRowActive = False
                        elif event.key == pygame.K_BACKSPACE:
                            inputRowText = inputRowText[:-1]
                        else:
                            inputRowText += event.unicode

                    if inputColActive:
                        if event.key == pygame.K_RETURN:
                            # Process the input col value
                            try:
                                inputColValue = int(inputColText)
                                # TODO: Process the input col value
                                print(f"Input Col: {inputColValue}")
                            except ValueError:
                                print("Invalid input for col")
                            inputColText = ''
                            inputColActive = False
                        elif event.key == pygame.K_BACKSPACE:
                            inputColText = inputColText[:-1]
                        else:
                            inputColText += event.unicode

                # Check if the input text boxes are clicked
                if inputRowRect.collidepoint(event.pos):
                    inputRowActive = True
                    inputColActive = False
                elif inputColRect.collidepoint(event.pos):
                    inputColActive = True
                    inputRowActive = False

            # Render the input text
            font = pygame.font.Font(None, 20)
            inputRowSurface = font.render(inputRowText, True, (0, 0, 0))
            inputColSurface = font.render(inputColText, True, (0, 0, 0))
            window.blit(inputRowSurface, (inputRowRect.x + 5, inputRowRect.y + 5))
            window.blit(inputColSurface, (inputColRect.x + 5, inputColRect.y + 5))
        # Draw the grid
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(window, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size), 1)

        # Draw the buttons with border
        pygame.draw.rect(window, (0, 0, 0), btnSetInit, 2)
        pygame.draw.rect(window, (0, 0, 0), btnSetGoal, 2)
        pygame.draw.rect(window, (0, 0, 0), btnFindPath, 2)
        pygame.draw.rect(window, (0, 0, 0), btnReset, 2)

        # Draw the input text
        pygame.draw.rect(window, (0, 0, 0), inputRowRect, 2)
        pygame.draw.rect(window, (0, 0, 0), inputColRect, 2)

        # Add text to the buttons
        font = pygame.font.Font(None, 20)
        text_init = font.render("Set Init", True, (0, 0, 0))
        text_goal = font.render("Set Goal", True, (0, 0, 0))
        text_path = font.render("Find Path", True, (0, 0, 0))
        text_reset = font.render("Reset", True, (0, 0, 0))

        window.blit(text_init, (button_x + 10, button_y + 5))
        window.blit(text_goal, (button_x + 10, button_y + button_height + button_padding + 5))
        window.blit(text_reset, (button_x + 10, button_y + 2*(button_height + button_padding) + 5))
        window.blit(text_path, (button_x + 10, button_y + 3*(button_height + button_padding) + 5))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

def run(grid, graph, paths):
    run_interactive_ui(grid, graph, paths)

# if __name__ == "__main__":
#     main() 