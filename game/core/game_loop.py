import pygame
from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent
from game.scenes.startingScene import StartingScene
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, BLUE

class Game(GameComponent):
    def __init__(self):

        # Game settings
        self.debug = True
        self.frame_rate = None
        self.show_fps = False
        self.running = True
        self.debug_color = BLUE

        # Initialize PyGame
        pygame.init()
        pygame.font.init()

        # Set PyGame variables
        self.pygame = pygame
        self.display = pygame.display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pygame.display.set_caption("Top-Down Adventure Game")
        self.clock = self.pygame.time.Clock()

        # Create an EventQueue
        self.event_queue = EventQueue(self.pygame, self.debug)
        self.event_queue.init_queue()

        self.active = False
        self.helper_functions = {}
        self.top_level = True
        self.need_to_update = False
        self.name = "Game"
        self.children = None
        self.parent = None

        self.rect_x = 0
        self.rect_y = 0

    def closeWindow(self):
        self.running = False

    def is_terminated(self):
        if self.event_queue.has_event('QUIT'):
            return True
        elif self.event_queue.has_event('KEYDOWN', {'key': 27}):
            return True
        return False
    
    def handle_events(self):
        # Use the event queue
        self.event_queue.handle_events()

        if self.active:
            self.scene.handle_events()

        if self.is_terminated():
            self.closeWindow()

    def update(self):
        if self.active:
            self.scene.update()

        # Optionally run any helper functions with "update" context
        self.run_helper_functions("update")

    def draw(self):
        if self.active:
            self.scene.draw()

            # Optionally run any helper functions with "draw" context
            self.run_helper_functions("draw")

    def set_starting_scene(self):
        scene = StartingScene("Starting Scene",  False)
        self.link_child(scene)
        scene.set_scene(self)
        self.scene = scene
        self.enable()

    def run(self):
        self.set_starting_scene()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            ticks = self.clock.tick(1000)
            self.frame_rate = self.clock.get_fps()
            if self.show_fps and self.frame_rate:
                print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')

        self.pygame.quit()
