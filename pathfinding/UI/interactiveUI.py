import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the grid
grid_width = 10
grid_height = 10
cell_size = 50

# Set the dimensions of the window
window_width = grid_width * cell_size + 100  # Increased window width to accommodate buttons
window_height = grid_height * cell_size

# Create the window
window = pygame.display.set_mode((window_width, window_height))

# Clear the window
window.fill((255, 255, 255))

# Create buttons
button_width = 80
button_height = 30
button_padding = 10
button_x = window_width - button_width - button_padding
button_y = button_padding

btnSetInit = pygame.Rect(button_x, button_y, button_width, button_height)
btnSetGoal = pygame.Rect(button_x, button_y + button_height + button_padding, button_width, button_height)

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
            
            if 0 < cell_x < grid_width and 0 < cell_y < grid_height:
                # Print the cell position
                print(f"Clicked on cell ({cell_x}, {cell_y})")

                # Set the color of the clicked cell to red
                pygame.draw.rect(window, (255, 0, 0), (cell_x * cell_size, cell_y * cell_size, cell_size, cell_size))
            
            # Check if the buttons are clicked
            if btnSetInit.collidepoint(event.pos):
                print("Set Init")
            elif btnSetGoal.collidepoint(event.pos):
                print("Set Goal")
    # Draw the grid
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(window, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size), 1)
    
    # Draw the buttons with border
    pygame.draw.rect(window, (0, 0, 0), btnSetInit, 2)
    pygame.draw.rect(window, (0, 0, 0), btnSetGoal, 2)

    # Add text to the buttons
    font = pygame.font.Font(None, 20)
    text_init = font.render("Set Init", True, (0, 0, 0))
    text_goal = font.render("Set Goal", True, (0, 0, 0))

    window.blit(text_init, (button_x + 10, button_y + 5))
    window.blit(text_goal, (button_x + 10, button_y + button_height + button_padding + 5))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()