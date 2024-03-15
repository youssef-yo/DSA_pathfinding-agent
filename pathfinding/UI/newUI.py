import pygame
from pygame.locals import *
import pygame_gui
import random
import sys

# Define image
img_off_path = 'pathfinding/UI/img/toggle-off.svg'
img_on_path = 'pathfinding/UI/img/toggle-on.svg'
img_repeat_path = 'pathfinding/UI/img/arrow-clockwise.svg'
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

class ImageButton(Button):
    def __init__(self, color, x, y, img_path):
        self.img = pygame.image.load(img_path)
        super().__init__(color, x, y, self.img.get_width(), self.img.get_height())

    def draw(self, screen, outline=None):
        super().draw(screen, outline)
        screen.blit(self.img, (self.x, self.y))

    def is_over(self, pos):
        return super().is_over(pos)

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
        
class UI:
    def __init__(self, instanceController, reachGoalController, informationController):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pathfinding for new Agent")

        self.instanceController = instanceController
        self.reachGoalController = reachGoalController

        self.instance = None

        self.information = informationController.Information()

    def setInstance(self, instance):
        self.instance = instance

    # Definiamo una funzione per creare un input text
    def create_text_input_int(self, manager, pos, size):
        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size), manager=manager)
        text_input.allowed_characters = '0123456789'

        return text_input

    # Definiamo una funzione per creare un input text
    def create_text_input_float(self, manager, pos, size):
        text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(pos, size), manager=manager)
        text_input.allowed_characters = '0123456789.'

        return text_input

    # Funzione per creare una etichetta
    def create_label(self, manager, pos, text):
        label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(pos, (200, 30)), text=text, manager=manager)
        # label.text_colour = (0, 0, 0)
        return label
    
    @staticmethod
    def initialize_color(n_paths):

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

        colors = []
        for _ in range(n_paths):
            color = random.choice(path_colors)
            path_colors.remove(color)
            colors.append(color)
        return colors

    def generate_new_path(self, reachGoalController, global_instance, toggle_relaxed_path_button):
        USE_RELAXED_PATH = toggle_relaxed_path_button.getState()

        if global_instance:
            #TODO: scommenta quando crei le classi per i controller
            # path, minimumSpanningTree = reachGoalController.reachGoal(global_instance, USE_RELAXED_PATH)
            path, P, closedSet = reachGoalController(global_instance, USE_RELAXED_PATH)

            if not path:
                print("No path found for new agent")
                return None, None, None
            
            return path, P, closedSet
        return None, None, None
        
    
    def reset_grid(self):
        self.screen.fill(WHITE, (0, 0, 800, HEIGHT))

    # Funzione per generare una nuova istanza
    def generate_instance(self, instanceController, nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, max_input, n_agent_input, toggle_relaxed_path_button, toggle_reach_goal_button):
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

        self.information.startMonitoring()
        #TODO: scommenta quando crei le classi
        # instance, nIteration = instanceController.generateInstance(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)
        instance, nIteration = instanceController(NROWS, NCOLS, FREE_CELL_RATIO, AGGLOMERATION_FACTOR, N_AGENTS, MAX, LIMIT_LENGTH_PATH, MAX_ITERATION, MAX_TOTAL_RUN, USE_REACH_GOAL_EXISTING_AGENTS, USE_RELAXED_PATH)
        if not instance:
            #TODO: handle error
            return
        if instance and nIteration < MAX_TOTAL_RUN: 
            return instance
        return

    def draw_instance(self, instance, path_colors):
        self.draw_paths(instance.getPaths(), path_colors)    

    def draw_grid(self, grid):
        grid_width = grid.getNcols()
        grid_height = grid.getNrows()
        for i in range(grid_height):
            for j in range(grid_width):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                if not grid.isFree(i, j):
                        pygame.draw.rect(self.screen, BLACK, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_paths(self, paths, path_colors):
        for i, path in enumerate(paths):
            self.draw_single_path(path, path_colors[i])

    def draw_init_goal(self, path):
        # Estrai il primo e l'ultimo movimento del percorso
        start_move = path.getInit()
        end_move = path.getGoal()

        # Estrai le coordinate di inizio e fine
        x_start, y_start = start_move[0], start_move[1]
        x_end, y_end = end_move[0], end_move[1]

        # Disegna un cerchio verde all'inizio del percorso
        pygame.draw.circle(self.screen, GREEN, ((x_start + 0.5) * CELL_SIZE, (y_start + 0.5) * CELL_SIZE), 6)

        # Disegna una X rossa alla fine del percorso (goal)
        x_goal = (x_end + 0.5) * CELL_SIZE
        y_goal = (y_end + 0.5) * CELL_SIZE
        pygame.draw.line(self.screen, RED, (x_goal - 5, y_goal - 5), (x_goal + 5, y_goal + 5), 6)
        pygame.draw.line(self.screen, RED, (x_goal + 5, y_goal - 5), (x_goal - 5, y_goal + 5), 6)
        # Disegna un cerchio rosso alla fine del percorso
        # pygame.draw.circle(screen, RED, ((x_end + 0.5) * CELL_SIZE, (y_end + 0.5) * CELL_SIZE), 6)
        
    def draw_single_path(self, path, color):
        
        self.draw_init_goal(path)
        # Disegna il percorso
        for t, move in path.getMoves():
            x_start, y_start = move.getSrc()
            x_end, y_end = move.getDst()
            pygame.draw.line(self.screen, color, ((x_start + 0.5) * CELL_SIZE, (y_start + 0.5) * CELL_SIZE), ((x_end + 0.5) * CELL_SIZE, (y_end + 0.5) * CELL_SIZE), 4)
            

    def draw_step_by_step(self, paths):
        path_colors = UI.initialize_color(len(paths))
        path_colors.pop()
        path_colors.append(RED)

        for path in paths:
            self.draw_init_goal(path)

        self.draw_moves(paths, path_colors)

    def draw_moves(self, paths, path_colors):
        t = 0
        keepGoing = True

        while keepGoing:
            keepGoing = False
            for i, path in enumerate(paths):
                move = path.getMove(t)
                if move:
                    keepGoing = True
                    x_start, y_start = move.getSrc()
                    x_end, y_end = move.getDst()
                    pygame.draw.line(self.screen, path_colors[i], ((x_start + 0.5) * CELL_SIZE, (y_start + 0.5) * CELL_SIZE), ((x_end + 0.5) * CELL_SIZE, (y_end + 0.5) * CELL_SIZE), 4)
                    
            pygame.display.update()
            pygame.time.wait(500)  # Add a delay to see the moves step by step

            t += 1
    
    def initialize_information(self, instance, freeCellRatio, agglomerationFactor, path, P, closedSet, relaxedPath, reachGoalExistingAgents):
        self.information.setValues(instance, freeCellRatio, agglomerationFactor, path, P, closedSet, relaxedPath, reachGoalExistingAgents)
    

    def clean_information(self):
        self.screen.fill(WHITE, (820, 700, 400, 200))

    def draw_information(self):
        lengthP = len(self.information.getP())
        lengthClosedSet = len(self.information.getClosedSet())
        pathLength = self.information.getPath().getLength()
        pathCost = self.information.getPath().getCost()
        waitCounter = self.information.getWaitCounter()
        executionTime = self.information.getExecutionTime()
        totalMemory = self.information.getTotalMemory()

        # Define text labels
        labels = [
            f"Max time goal occupied: {self.instance.getMaxTimeGoalOccupied()}",
            f"Length of the path: {pathLength}",
            f"Length of P: {lengthP}",
            f"Length of ClosedSet: {lengthClosedSet}",
            f"Wait Counter: {waitCounter}",
            f"Execution Time: {executionTime}",
            f"Path Cost: {pathCost}",
            f"Total Memory: {totalMemory} KB"
        ]

        # Define text positions
        text_pos = (820, 700)
        line_spacing = 20

        # Draw new information
        for i, label in enumerate(labels):
            text_surface = pygame.font.Font(None, 20).render(label, True, BLACK)
            self.screen.blit(text_surface, (text_pos[0], text_pos[1] + i * line_spacing))

    def draw_error(self, error):
        # Draw error message
        error_font = pygame.font.Font(None, 30)
        error_text = error_font.render(error, True, RED)
        error_rect = error_text.get_rect(center=(400, 400))
        self.screen.blit(error_text, error_rect)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        # Creazione del manager per gli elementi GUI
        manager = pygame_gui.UIManager((WIDTH, HEIGHT))

        # Creazione dei bottoni
        generate_button = Button(LIGHT_BLUE, 1000, 50, 200, 50, 'Generate Instance')
        toggle_step_by_step_button = ToggleButton(1150, 120, img_off_path, img_on_path)

        repeat_button = ImageButton(WHITE, 820, 50, img_repeat_path)
        # new_agent_button = Button(LIGHT_BLUE, 1000, 150, 200, 50, 'New Agent')

        toggle_relaxed_path_button = ToggleButton(1200, 600, img_off_path, img_on_path)
        toggle_reach_goal_button = ToggleButton(1200, 650, img_off_path, img_on_path)
        
        # Creazione degli input text
        text_inputs = []
        labels = []

        # Creazione delle etichette
        nrow_label = self.create_label(manager, (850, 350), "N ROWS:")
        ncol_label = self.create_label(manager, (1050, 350), "N COLS:")
        free_cell_ratio_label = self.create_label(manager, (820, 400), "% Free Cell:")
        agglomeration_factor_label = self.create_label(manager, (820, 450), "Aggloremation:")
        n_agent_label = self.create_label(manager, (1050, 400), "N Agent:")
        max_label = self.create_label(manager, (1050, 450), "Max:")
        relaxed_label = self.create_label(manager, (1000, 600), "Use Relaxed Path:")
        reach_goal_label = self.create_label(manager, (1000, 650), "Use Reach Goal:")
        step_by_step_label = self.create_label(manager, (950, 120), "Step By Step:")

        nrow_input = self.create_text_input_int(manager, (1000, 350), (100, 30))
        ncol_input = self.create_text_input_int(manager, (1200, 350), (100, 30))
        free_cell_ratio_input = self.create_text_input_float(manager, (1000, 400), (100, 30))
        agglomeration_factor_input = self.create_text_input_float(manager, (1000, 450), (100, 30))
        n_agent_input = self.create_text_input_int(manager, (1200, 400), (100, 30))
        max_input = self.create_text_input_int(manager, (1200, 450), (100, 30))

        text_inputs.extend([nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, n_agent_input, max_input])
        labels.extend([nrow_label, ncol_label, free_cell_ratio_label, agglomeration_factor_label, n_agent_label, max_label, relaxed_label, reach_goal_label, step_by_step_label])

        self.screen.fill(WHITE)

        # Draw separation line
        start_pos = (810, 0)  
        end_pos = (810, 900)  
        pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 2)

        toggle_relaxed_path_button.draw(self.screen)
        toggle_reach_goal_button.draw(self.screen)  
        toggle_step_by_step_button.draw(self.screen)  

        while running:
            time_delta = clock.tick(60) / 1000.0

            # Disegno dei bottoni
            generate_button.draw(self.screen, BLACK)
            repeat_button.draw(self.screen, BLACK)
            # new_agent_button.draw(self.screen, BLACK)

            # Gestione degli eventi per gli elementi GUI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if generate_button.is_over(pos):
                        self.setInstance(None)
                        self.clean_information()
                        self.reset_grid()
                        instance = self.generate_instance(self.instanceController, nrow_input, ncol_input, free_cell_ratio_input, agglomeration_factor_input, max_input, n_agent_input, toggle_relaxed_path_button, toggle_reach_goal_button)
                        self.setInstance(instance)

                        if self.instance:
                            self.draw_grid(self.instance.getGrid())
                            path_colors = UI.initialize_color(len(self.instance.getPaths())) 

                            if toggle_step_by_step_button.getState():
                                new_path, P, closedSet = self.generate_new_path(self.reachGoalController, self.instance, toggle_relaxed_path_button)
                                self.information.stopMonitoring()
                                if new_path:
                                    self.instance.addPath(new_path)

                                    paths = self.instance.getPaths()
                                    self.draw_step_by_step(paths)
                            else:
                                self.draw_instance(self.instance, path_colors)
                                new_path, P, closedSet = self.generate_new_path(self.reachGoalController, self.instance, toggle_relaxed_path_button)
                                self.information.stopMonitoring()
                                if new_path:
                                    self.instance.addPath(new_path)
                                    self.draw_single_path(new_path, RED)
                            self.initialize_information(self.instance, float(free_cell_ratio_input.get_text()), float(agglomeration_factor_input.get_text()), new_path, P, closedSet, toggle_relaxed_path_button.getState(), toggle_reach_goal_button.getState())
                            self.draw_information()
                        else:
                            self.draw_error("Error with input parameters or couldn't find any valid paths")
                    # elif new_agent_button.is_over(pos):
                    #     # generate_new_path(global_instance, toggle_relaxed_path_button)
                    #     pass
                    elif repeat_button.is_over(pos):
                        if toggle_step_by_step_button.getState():
                            if self.instance:
                                self.reset_grid()
                                self.draw_grid(self.instance.getGrid())
                                self.draw_step_by_step(self.instance.getPaths())
                    elif toggle_relaxed_path_button.is_over(pos):
                        toggle_relaxed_path_button.toggle()
                        toggle_relaxed_path_button.draw(self.screen)
                    elif toggle_reach_goal_button.is_over(pos):
                        toggle_reach_goal_button.toggle()
                        toggle_reach_goal_button.draw(self.screen)  
                    elif toggle_step_by_step_button.is_over(pos):
                        toggle_step_by_step_button.toggle()
                        toggle_step_by_step_button.draw(self.screen)  

                        
                manager.process_events(event)
            # Aggiornamento e disegno degli elementi GUI
            manager.update(time_delta)
            manager.draw_ui(self.screen)


            pygame.display.update()
