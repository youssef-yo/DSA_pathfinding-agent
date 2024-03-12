import pygame
from pygame.locals import *
import pygame_gui

import sys

#TODO: Take controller as parameter in __init__
from generator.instanceGenerator import generateInstance

# Inizializzazione di Pygame
pygame.init()

# Definizione dei colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

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

# def handle_text_input_events(event, text_inputs):
#     for text_input in text_inputs:
#         if event.ui_element == text_input:
#             if event.type == pygame.USEREVENT:
#                 # if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
#                 #     # Memorizza il testo inserito nell'input text
#                 #     # text_input.old_text = text_input.get_text()
#                 #     pass
#                 # elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
#                 #     # Qui puoi eseguire azioni quando il testo nell'input text cambia (opzionale)
#                 #     pass
#                 if event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
#                     text_input.old_text = text_input.get_text()
#                     text_input.set_text('')


# Definiamo una funzione per creare un input text
def create_text_input(manager, pos, size):
    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size), manager=manager)
    text_input.allowed_characters = '0123456789'
    return text_input

# Funzione per creare una etichetta
def create_label(manager, pos, text):
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(pos, (200, 30)), text=text, manager=manager)
    return label

# Definiamo una funzione per creare una checkbox
def create_checkbox(manager, pos, text):
    # checkbox = pygame_gui.elements.UICheckBox(relative_rect=pygame.Rect(pos, (150, 30)), text=text, manager=manager)
    checkbox = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect(pos, (150, 30)), item_list = text, manager=manager)
    return checkbox

# Funzione per generare una nuova istanza
def generate_instance(nrow_input, ncol_input):

    # Reset the grid
    #TODO: create methods
    screen.fill(WHITE, (0, 0, WIDTH//2, HEIGHT))

    # Qui chiami il controller e generi la nuova istanza
    if nrow_input.get_text() == '' or ncol_input.get_text() == '':
        #TODO: handle error
        return
    
    NROWS = int(nrow_input.get_text())
    NCOLS = int(ncol_input.get_text())
    FREE_CELL_RATIO = 0.9
    AGGLOMERATION_FACTOR = 0.2
    MAX = 40

    N_AGENTS = 2
    LIMIT_LENGTH_PATH = FREE_CELL_RATIO * NROWS * NCOLS

    MAX_ITERATION = 80 # max number of iteration to reset the creation of a single path
    MAX_TOTAL_RUN = 6 # max number of run to create a valid instance

    USE_RELAXED_PATH = False
    USE_REACH_GOAL_EXISTING_AGENTS = False

    instance, nIteration = generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)

    if not instance:
        #TODO: handle error
        return
    draw_grid(instance.getGrid())
    #TODO: draw paths

def draw_grid(grid):
    grid_width = grid.getNcols()
    grid_height = grid.getNrows()
    for i in range(grid_height):
        for j in range(grid_width):
            pygame.draw.rect(screen, (0, 0, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if not grid.isFree(i, j):
                    pygame.draw.rect(screen, BLACK, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pass
# Funzione per cercare il percorso del nuovo agente
def find_path(init, goal):
    # Qui chiami il metodo del controller per cercare il percorso
    pass
# Funzione principale
def main():
    running = True
    clock = pygame.time.Clock()

    # Creazione del manager per gli elementi GUI
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    # Creazione dei bottoni
    generate_button = Button(GREEN, 1000, 50, 200, 50, 'Generate Instance')
    new_agent_button = Button(GREEN, 1000, 150, 200, 50, 'New Agent')
    find_path_button = Button(GREEN, 1000, 250, 200, 50, 'Find Path')

    # Creazione degli input text
    text_inputs = []
    labels = []

    # Creazione delle etichette
    nrow_label = create_label(manager, (850, 350), "N ROWS:")
    ncol_label = create_label(manager, (1050, 350), "N COLS:")
    free_cell_ratio_label = create_label(manager, (900, 400), "% Free Cell:")
    agglomeration_factor_label = create_label(manager, (1100, 400), "Aggloremation:")
    n_agent_label = create_label(manager, (900, 450), "N Agent:")
    max_label = create_label(manager, (1100, 450), "Max:")

    nrow_input = create_text_input(manager, (1000, 350), (100, 30))
    ncol_input = create_text_input(manager, (1200, 350), (100, 30))
    free_cell_ratio_input = create_text_input(manager, (1000, 400), (100, 30))
    agglomeration_factor_input = create_text_input(manager, (1200, 400), (100, 30))
    n_agent_input = create_text_input(manager, (1000, 450), (100, 30))
    max_input = create_text_input(manager, (1200, 450), (100, 30))

    text_inputs.extend([nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, n_agent_input, max_input])
    labels.extend([nrow_label, ncol_label, free_cell_ratio_label, agglomeration_factor_label, n_agent_label, max_label])


    # Creazione delle checkbox
    checkboxes = []
    checkboxes.append(create_checkbox(manager, (1000, 600), 'Use Relaxed Path'))
    checkboxes.append(create_checkbox(manager, (1200, 600), 'Use Reach Goal'))

    screen.fill(WHITE)
    while running:
        time_delta = clock.tick(60) / 1000.0

        # Disegno dei bottoni
        generate_button.draw(screen, BLACK)
        new_agent_button.draw(screen, BLACK)
        find_path_button.draw(screen, BLACK)

        # Gestione degli eventi per gli elementi GUI
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if generate_button.is_over(pos):
                    generate_instance(nrow_input, ncol_input)
                elif new_agent_button.is_over(pos):
                    # Qui gestisci la selezione delle caselle per init e goal
                    pass
                elif find_path_button.is_over(pos):
                    # Qui richiami la funzione per cercare il percorso del nuovo agente
                    pass
            manager.process_events(event)

        # Aggiornamento e disegno degli elementi GUI
        manager.update(time_delta)
        manager.draw_ui(screen)


        pygame.display.update()

if __name__ == '__main__':
    main()