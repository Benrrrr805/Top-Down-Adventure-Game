import pygame
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, RED
from game.scenes.helpers.button import Button
from game.core.game_resources import GameResources
# Main menu scene
class MenuScene:
    def __init__(self):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug
        
        self.new_game_button = Button(740, 465, 380, 100, "new_game")
        self.load_game_button = Button(740, 585, 380, 100, "load_game")
        self.setting_button = Button(740, 705, 380, 100, "settings")
        self.exit_button = Button(740, 825, 380, 100, "exit")
        self.buttons = [self.new_game_button, self.load_game_button, self.setting_button, self.exit_button]
        self.events = None


        self.mouse_pos = None
    def handle_events(self):
        for button in self.buttons:
            button.handle_events()                
        
    def update(self):
        for button in self.buttons:
            button.update()
 
    def draw(self):
        image = pygame.image.load("./assets/images/mainMenu/main_menu_screen_1792x1024.png")
        self.screen.fill(BLACK)
        self.screen.blit(image, (0,0))

        for button in self.buttons:
            button.draw()

        self.display.flip()

