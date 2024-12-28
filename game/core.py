# Core game logic
import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game.utils.tiled_map import TiledMap


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Top-Down Adventure Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Load Tiled map
        self.map = TiledMap('assets/maps/level1.tmx')
        self.map_surface = self.map.make_map_surface()
        self.map_rect = self.map_surface.get_rect()

    def handle_events(self):
        for event in pygame.event.get():
            if self.is_terminated(event):
                self.closeWindow()
        
            

    def closeWindow(self):
        self.running = False

    def is_terminated(self, event):
        return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)

    def update(self):
        # Update game objects here
        pass

    def draw(self):
        self.screen.blit(self.map_surface, (0, 0))  # Draw the map
        pygame.display.flip()  # Update the display

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
