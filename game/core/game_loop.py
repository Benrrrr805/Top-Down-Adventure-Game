import pygame
from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent
from game.scenes.startingScene import StartingScene
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE

class Game(GameComponent):
    def __init__(self):
        super().__init__("Main", True)
        self.debug = True
        self.frame_rate = None
        self.show_fps = False
        self.running = True
        self.debug_color = BLUE
        self.graphics_enabled = False

        pygame.init()
        pygame.font.init()

        self.pygame = pygame
        self.display = pygame.display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pygame.display.set_caption("Top-Down Adventure Game")
        self.clock = self.pygame.time.Clock()

        self.event_queue = EventQueue(self.pygame, self.debug)
        self.event_queue.init_queue()

        self.active = False
        self.helper_functions = {}
        self.top_level = True
        self.need_to_update = False
        self.name = "Game"
        self.game_values_set = True

        self.game_values = {
            'pygame': self.pygame,
            'screen': self.screen,
            'display': self.display,
            'debug': self.debug,
            'debug_color': self.debug_color,
            'event_queue': self.event_queue,
        }

    def closeWindow(self):
        self.running = False

    def is_terminated(self):
        if self.event_queue.has_event('QUIT'):
            return True
        elif self.event_queue.has_event('KEYDOWN', {'key': 27}):
            return True
        return False
    
    def handle_events(self):
        self.event_queue.handle_events()

        if self.active:
            self.scene.handle_events()

        if self.is_terminated():
            self.closeWindow()

    def update(self):
        if self.active:
            self.scene.update()

        self.run_helper_functions("update")

    def draw(self):
        if self.active:
            self.scene.draw()

            self.run_helper_functions("draw")

    def set_scene(self, scene: 'StartingScene'):
        self.link_child(scene)
        scene.set_scene()
        self.scene = scene
        self.enable()
        return True

    def run(self):
        self.set_scene(StartingScene("Starting Scene", False))
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            ticks = self.clock.tick(1000)
            self.frame_rate = self.clock.get_fps()
            if self.show_fps and self.frame_rate:
                print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')

        self.pygame.quit()
