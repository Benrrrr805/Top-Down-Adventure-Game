import pygame
from game.settings import BLACK
from game.core.game_resources import GameResources

class Menu:
    def __init__(self, background_image, buttons):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug
        
      
        self.background_image = pygame.image.load(background_image).convert()
        self.buttons = buttons
        self.events = None


        self.mouse_pos = None
    def handle_events(self):
        for button in self.buttons:
            button.handle_events()                
        
    def update(self):
        for button in self.buttons:
            button.update()
 
    def draw(self):        
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0,0))

        for button in self.buttons:
            button.draw()

        self.display.flip()

