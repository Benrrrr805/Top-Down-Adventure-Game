# game/core/game_loop.py (or wherever your Game class was)

import pygame
from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent
from game.scenes.startingScene import StartingScene
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Game(GameComponent):
    def __init__(self):
        super().__init__(name="Game", top_level=True)

        # Initialize pygame once (instead of using GameResources)
        pygame.init()
        pygame.font.init()

        # Store references as instance properties
        self.pygame = pygame
        self.display = pygame.display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # or your SCREEN_WIDTH, SCREEN_HEIGHT
        self.debug = True
        self.running = True

        # Window caption
        pygame.display.set_caption("Top-Down Adventure Game")

        # Create an EventQueue
        self.event_queue = EventQueue()
        self.event_queue.initialize(self.pygame, self.debug)

        # Game states
        self.clock = self.pygame.time.Clock()
        self.state = "startingScene"
        self.scene = None
        self.frame_rate = None
        self.show_fps = False

        # Mark ourselves initialized
        self.initialize()  # or do it explicitly later
        print("Game initialized")

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

        if self.scene:
            self.scene.handle_events()

        if self.is_terminated():
            self.closeWindow()

    def update(self):
        # Lazy-load or create the scene
        if self.state == "startingScene" and self.scene is None:
            self.scene = StartingScene() 
            self.link(self, child=self.scene)
            self.scene.initialize()

        if self.scene:
            self.scene.update()

        # Optionally run any helper functions with "update" context
        self.run_helper_functions("update")

    def draw(self):
        if self.scene:
            self.scene.draw()
            # Optionally run any helper functions with "draw" context
            self.run_helper_functions("draw")


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            ticks = self.clock.tick()
            self.frame_rate = int(self.clock.get_fps())
            if self.show_fps and self.frame_rate:
                print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')

        self.pygame.quit()
