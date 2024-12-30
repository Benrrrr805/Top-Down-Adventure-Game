# Core game logic
import os
import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from game.utils.tiled_map import TiledMap
from game.scenes.menu import MenuScene
from game.core.game_resources import GameResources


class Game:
    def __init__(self):
        GameResources.display = pygame.display
        GameResources.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        GameResources.debug = True

        pygame.display.set_caption("Top-Down Adventure Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "main_menu"
        self.scene = None
        

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
        if self.state == "main_menu":
            self.scene = MenuScene()
        self.scene.update()


    def draw(self):
        self.scene.draw()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
