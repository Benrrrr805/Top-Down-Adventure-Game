# Core game logic
import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game.scenes.startingScene import StartingScene
from game.core.game_resources import GameResources


class Game:
    def __init__(self):
        GameResources.display = pygame.display
        GameResources.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        GameResources.debug = True

        pygame.display.set_caption("Top-Down Adventure Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "startingScene"
        self.scene = None
        self.frame_rate = None
        

    def handle_events(self):
        for event in pygame.event.get():
            if self.is_terminated(event):
                self.closeWindow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.post(event)
        if self.scene:
            self.scene.handle_events()

    def closeWindow(self):
        self.running = False

    def is_terminated(self, event):
        return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    def update(self):
        if self.state == "startingScene" and self.scene == None:
            self.scene = StartingScene()
        self.scene.update()


    def draw(self):
        self.scene.draw()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            ticks = self.clock.tick()
            self.frame_rate = int(self.clock.get_fps())
            if self.frame_rate:
                if self.debug:
                    print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')
