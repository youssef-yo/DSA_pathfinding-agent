import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the grid
grid_width = 10
grid_height = 10
cell_size = 50

# Set the dimensions of the window
window_width = grid_width * cell_size
window_height = grid_height * cell_size

# Create the window
window = pygame.display.set_mode((window_width, window_height))

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
            
            # Print the cell position
            print(f"Clicked on cell ({cell_x}, {cell_y})")
    
    # Clear the window
    window.fill((255, 255, 255))
    
    # Draw the grid
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(window, (0, 0, 0), (x * cell_size, y * cell_size, cell_size, cell_size), 1)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()