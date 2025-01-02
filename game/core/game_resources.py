import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT
class GameResources:
    pygame.init()
    pygame.font.init()
    pygame = pygame
    display = pygame.display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    debug = True
    running = True
    pygame.display.set_caption("Top-Down Adventure Game")