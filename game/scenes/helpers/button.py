import pygame
from game.settings import BLACK, RED
from game.core.game_resources import GameResources

class Button:
    def __init__(self, x_coordinate, y_coordinate, height, width, name):


        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.height = height
        self.width = width
        self.name = name


        self.rect = pygame.Rect(self.x_coordinate, self.y_coordinate, self.height, self.width)
        self.debug_color = BLACK


    def in_rect(self, coordinates):
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        # print("hovering: " + self.name)
        return self.in_rect(pygame.mouse.get_pos())
    
    def clicked(self):
        if not self.hovering():
            return False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
    
    def handle_events(self):
        if self.clicked():
            print("clicked: " + self.name)



    def update(self):
        if self.debug and self.hovering():
            self.debug_color = RED

    def  draw(self):
        if self.debug:
            pygame.draw.rect(self.screen, self.debug_color, self.rect, 5)


