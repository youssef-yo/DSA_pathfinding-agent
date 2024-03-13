import pygame
from pygame.locals import *
import pygame_gui
import random
import sys

#TODO: Take controller as parameter in __init__
from generator.instanceGenerator import generateInstance
from solver.reachGoal import reachGoal


# Inizializzazione di Pygame
pygame.init()

# Define image
img_off_path = 'img/toggle-off.svg'
img_on_path = 'img/toggle-on.svg'

# Definizione dei colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
RED = (255, 0, 0)

# Definizione delle dimensioni della finestra
WIDTH = 1400
HEIGHT = 900

CELL_SIZE = 50

# Creazione della finestra
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Visualization")


# Definizione della classe per i bottoni
class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.Font(None, 20)
            text = font.render(self.text, 1, BLACK)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class ToggleButton:
    def __init__(self, x, y, img_off_path, img_on_path):
        self.x = x
        self.y = y
        self.img_off = pygame.image.load(img_off_path)
        self.img_on = pygame.image.load(img_on_path)
        self.state = True

    def draw(self, screen):
        screen.fill((255, 255, 255), (self.x, self.y, max(self.img_off.get_width(), self.img_on.get_width()), max(self.img_off.get_height(), self.img_on.get_height())))

        if self.state:
            screen.blit(self.img_on, (self.x, self.y))
        else:
            screen.blit(self.img_off, (self.x, self.y))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.img_off.get_width():
            if pos[1] > self.y and pos[1] < self.y + self.img_off.get_height():
                return True
        return False
    
    def toggle(self):
        self.state = not self.state
    
    def getState(self):
        return self.state



# Definiamo una funzione per creare un input text
def create_text_input_int(manager, pos, size):
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size), manager=manager)
    text_input.allowed_characters = '0123456789'

    return text_input

# Definiamo una funzione per creare un input text
def create_text_input_float(manager, pos, size):
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size), manager=manager)
    text_input.allowed_characters = '0123456789.'

    return text_input

# Funzione per creare una etichetta
def create_label(manager, pos, text):
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(pos, (200, 30)), text=text, manager=manager)
    # label.text_colour = (0, 0, 0)
    return label

# Definiamo una funzione per creare una checkbox
def create_checkbox(manager, pos, options):
    # checkbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(pos, (150, 30)), text=text, manager=manager)
    dropdown = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(pos, (150, 30)), starting_option=options[0], options_list=options, manager=manager)
    return dropdown

def initialize_color():
    # Definizione dei colori per i percorsi
    path_colors = [
        (0, 0, 255),   # Blue
        (255, 255, 0), # Yellow
        (255, 0, 255), # Magenta
        (0, 255, 255), # Cyan
        (128, 0, 0),   # Maroon
        (0, 128, 0),   # Green (Dark)
        (0, 0, 128),   # Navy
        (128, 128, 0), # Olive
        (128, 0, 128), # Purple
        (0, 128, 128), # Teal
        (128, 128, 128), # Gray
        (192, 192, 192), # Silver
        (128, 0, 0),   # Maroon (Dark)
        (0, 128, 0),   # Green (Dark)
        (0, 0, 128),   # Navy (Dark)
        (128, 128, 0), # Olive (Dark)
        (128, 0, 128), # Purple (Dark)
        (0, 128, 128)  # Teal (Dark)
    ]

    return path_colors

def generate_new_path(global_instance, toggle_relaxed_path_button):
    USE_RELAXED_PATH = toggle_relaxed_path_button.getState()

    if global_instance:
        path, minimumSpanningTree = reachGoal(global_instance, USE_RELAXED_PATH)

        if not path:
            print("No path found for new agent")
            return
        
        draw_single_path(path, (255, 0, 0))
    
    
# Funzione per generare una nuova istanza
def generate_instance(nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, max_input, n_agent_input, toggle_relaxed_path_button, toggle_reach_goal_button):

    # Reset the grid
    #TODO: create methods
    screen.fill(WHITE, (0, 0, 800, HEIGHT))

    # Qui chiami il controller e generi la nuova istanza
    if nrow_input.get_text() == '' or ncol_input.get_text() == '' or free_cell_ratio_input.get_text() == '' or agglomeration_factor_input.get_text() == '' or max_input.get_text() == '' or n_agent_input.get_text() == '':
        #TODO: handle error
        return
    
    #TODO: create methods to get the values
    NROWS = int(nrow_input.get_text())
    NCOLS = int(ncol_input.get_text())
    FREE_CELL_RATIO = float(free_cell_ratio_input.get_text())
    AGGLOMERATION_FACTOR = float(agglomeration_factor_input.get_text())
    MAX = int(max_input.get_text())
    N_AGENTS = int(n_agent_input.get_text())

    USE_RELAXED_PATH = toggle_relaxed_path_button.getState()
    USE_REACH_GOAL_EXISTING_AGENTS = toggle_reach_goal_button.getState()

    #TODO: max of row = 15, max of col = 18
    if NROWS <= 0 or NROWS >= 16 or  NCOLS <= 0 or NCOLS >= 19 or  FREE_CELL_RATIO <= 0 or FREE_CELL_RATIO > 1 or AGGLOMERATION_FACTOR < 0 or AGGLOMERATION_FACTOR > 1 or MAX <= 0 or N_AGENTS <= 0:
        return

    LIMIT_LENGTH_PATH = FREE_CELL_RATIO * NROWS * NCOLS

    #TODO: create text input
    MAX_ITERATION = 80 # max number of iteration to reset the creation of a single path
    MAX_TOTAL_RUN = 6 # max number of run to create a valid instance

    path_colors = initialize_color()

    instance, nIteration = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

    # set_instance(instance)

    if not instance:
        #TODO: handle error
        return
    if instance and nIteration < MAX_TOTAL_RUN: 
        draw_instance(instance, path_colors)
    return instance

def draw_instance(instance, path_colors):
    draw_grid(instance.getGrid())
    draw_paths(instance.getPaths(), path_colors)

def draw_grid(grid):
    grid_width = grid.getNcols()
    grid_height = grid.getNrows()
    for i in range(grid_height):
        for j in range(grid_width):
            pygame.draw.rect(screen, (0, 0, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if not grid.isFree(i, j):
                    pygame.draw.rect(screen, BLACK, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_paths(paths, path_colors):
    for path in paths:
        # Genera un colore casuale per il percorso
        color = random.choice(path_colors)
        path_colors.remove(color)

        draw_single_path(path, color)

        
def draw_single_path(path, color):
    # Estrai il primo e l'ultimo movimento del percorso
    start_move = path.getInit()
    end_move = path.getGoal()

    # Estrai le coordinate di inizio e fine
    x_start, y_start = start_move[0], start_move[1]
    x_end, y_end = end_move[0], end_move[1]

    # Disegna un cerchio rosso all'inizio del percorso
    pygame.draw.circle(screen, GREEN, ((x_start + 0.5) * CELL_SIZE, (y_start + 0.5) * CELL_SIZE), 6)
    # Disegna un cerchio blu alla fine del percorso
    pygame.draw.circle(screen, RED, ((x_end + 0.5) * CELL_SIZE, (y_end + 0.5) * CELL_SIZE), 6)

    # Disegna il percorso
    for t, move in path.getMoves():
        x_start, y_start = move.getSrc()
        x_end, y_end = move.getDst()
        pygame.draw.line(screen, color, ((x_start + 0.5) * CELL_SIZE, (y_start + 0.5) * CELL_SIZE), ((x_end + 0.5) * CELL_SIZE, (y_end + 0.5) * CELL_SIZE), 4)
        

# Funzione principale
def main():
    running = True
    clock = pygame.time.Clock()

    # Creazione del manager per gli elementi GUI
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Creazione dei bottoni
    generate_button = Button(LIGHT_BLUE, 1000, 50, 200, 50, 'Generate Instance')
    # new_agent_button = Button(LIGHT_BLUE, 1000, 150, 200, 50, 'New Agent')

    toggle_relaxed_path_button = ToggleButton(1200, 600, img_off_path, img_on_path)
    toggle_reach_goal_button = ToggleButton(1200, 650, img_off_path, img_on_path)


    # Creazione degli input text
    text_inputs = []
    labels = []

    # Creazione delle etichette
    nrow_label = create_label(manager, (850, 350), "N ROWS:")
    ncol_label = create_label(manager, (1050, 350), "N COLS:")
    free_cell_ratio_label = create_label(manager, (820, 400), "% Free Cell:")
    agglomeration_factor_label = create_label(manager, (820, 450), "Aggloremation:")
    n_agent_label = create_label(manager, (1050, 400), "N Agent:")
    max_label = create_label(manager, (1050, 450), "Max:")
    relaxed_label = create_label(manager, (1000, 600), "Use Relaxed Path:")
    reach_goal_label = create_label(manager, (1000, 650), "Use Reach Goal:")

    nrow_input = create_text_input_int(manager, (1000, 350), (100, 30))
    ncol_input = create_text_input_int(manager, (1200, 350), (100, 30))
    free_cell_ratio_input = create_text_input_float(manager, (1000, 400), (100, 30))
    agglomeration_factor_input = create_text_input_float(manager, (1000, 450), (100, 30))
    n_agent_input = create_text_input_int(manager, (1200, 400), (100, 30))
    max_input = create_text_input_int(manager, (1200, 450), (100, 30))

    text_inputs.extend([nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, n_agent_input, max_input])
    labels.extend([nrow_label, ncol_label, free_cell_ratio_label, agglomeration_factor_label, n_agent_label, max_label, relaxed_label, reach_goal_label])

    screen.fill(WHITE)
    # Draw separation line
    start_pos = (810, 0)  
    end_pos = (810, 900)  

    pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    #TODO: move to __init__
    global_instance = None
    while running:
        time_delta = clock.tick(60) / 1000.0

        # Disegno dei bottoni
        generate_button.draw(screen, BLACK)
        # new_agent_button.draw(screen, BLACK)

        # Gestione degli eventi per gli elementi GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if generate_button.is_over(pos):
                    global_instance = generate_instance(nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, max_input, n_agent_input, toggle_relaxed_path_button, toggle_reach_goal_button)
                    generate_new_path(global_instance, toggle_relaxed_path_button)
                # elif new_agent_button.is_over(pos):
                #     # generate_new_path(global_instance, toggle_relaxed_path_button)
                #     pass
                elif toggle_relaxed_path_button.is_over(pos):
                    toggle_relaxed_path_button.toggle()
                    
                elif toggle_reach_goal_button.is_over(pos):
                    toggle_reach_goal_button.toggle()
                    
            manager.process_events(event)

        toggle_relaxed_path_button.draw(screen)
        toggle_reach_goal_button.draw(screen)  
        # Aggiornamento e disegno degli elementi GUI
        manager.update(time_delta)
        manager.draw_ui(screen)


        pygame.display.update()

if __name__ == '__main__':
    main()