import pygame
from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent
from game.scenes.startingScene import StartingScene
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLUE

class Game(GameComponent):
    def __init__(self):
        super().__init__("Game", True)
        self.event_queue = EventQueue(self.pygame, self.debug)
        self.running = True

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
            if self.show_fps:
                print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')

        self.pygame.quit()
