import pygame
import numpy as np

def run_interactive_ui(grid, paths):
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
    window_width = grid_width * cell_size + 100  # Increased window width to accommodate buttons
    window_height = grid_height * cell_size

    # Create the window
    window = pygame.display.set_mode((window_width, window_height))

    # Set obstacle
    # Plot the grid
    window.fill((255, 255, 255))
    for i in range(grid_height):
        for j in range(grid_width):
            if grid[i][j] == 1:
                    pygame.draw.rect(window, (0, 0, 0), (i * cell_size, j * cell_size, cell_size, cell_size))

    # Draw the paths
    colors = []
    for path in paths:
        color = list(np.random.randint(256, size=3))
        colors.append(color)
        print(color)
        for _, move in path.getMoves():
            pygame.draw.rect(window, color, (move.getDst()[0] * cell_size, move.getDst()[1] * cell_size, cell_size, cell_size))


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
                    pygame.draw.rect(window, (255, 255, 255), (newInit[0] * cell_size, newInit[1] * cell_size, cell_size, cell_size))
                    pygame.draw.rect(window, (255, 255, 255), (newGoal[0] * cell_size, newGoal[1] * cell_size, cell_size, cell_size))
                    newInit = None
                    newGoal = None
                    setInit = False
                    setGoal = False

                if btnFindPath.collidepoint(event.pos):
                    if not newInit or not newGoal:
                        print("First set Init and Goal")
                    else:
                        print("Find Path")
                        # # TODO: check for MVC correctness

                        # # Wait for the controller response
                        # response = controller_function(newInit, newGoal)  # Assuming you have a controller function that takes the initial and goal positions as arguments

                        # # Process the response
                        # if response:
                        #     # Path found, update the grid with the path
                        #     for position in response:
                        #         pygame.draw.rect(window, (0, 0, 255), (position[0] * cell_size, position[1] * cell_size, cell_size, cell_size))
                        # else:
                        #     # No path found, display an error message
                        #     print("No path found")

        # Draw the grid
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(window, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size), 1)

        # Draw the buttons with border
        pygame.draw.rect(window, (0, 0, 0), btnSetInit, 2)
        pygame.draw.rect(window, (0, 0, 0), btnSetGoal, 2)
        pygame.draw.rect(window, (0, 0, 0), btnFindPath, 2)
        pygame.draw.rect(window, (0, 0, 0), btnReset, 2)

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

def run(grid, paths):
    run_interactive_ui(grid, paths)

# if __name__ == "__main__":
#     main() 