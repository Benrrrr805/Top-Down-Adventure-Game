from game.scenes.helpers.button import Button
from game.scenes.helpers.menu import Menu
from game.core.game_resources import GameResources
import pygame

# Main menu scene
class StartingScene:
    def __init__(self):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug
        
        # Menu position
        menu_x = 100
        menu_y = 100

        button_width = 300
        button_height = 100


        # Buttons relative to the menu
        self.new_game_button = Button("new_game", button_width, button_height,  menu_x + 20, menu_y + 20)
        self.load_game_button = Button("load_game", button_width, button_height, menu_x + 20, menu_y + 140)
        self.setting_button = Button("settings", button_width, button_height, menu_x + 20, menu_y + 260)
        self.exit_button = Button(exit, button_width, button_height, menu_x + 20, menu_y + 380)

        self.buttons = [self.new_game_button, self.load_game_button, self.setting_button, self.exit_button]
        self.menu_background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"

        self.temp_url = self.menu_background_image_url
        self.menu = Menu("startingScene", 800, 600, menu_x, menu_y, self.menu_background_image_url, self.buttons)
        self.surfaces = []

    def handle_events(self):
        self.menu.handle_events()
            
        
    def update(self):
        self.menu.update()

 
    def draw(self):
        menu_surface = self.menu.draw()
        menu_rect = self.menu.get_rect()
        self.screen.blit(menu_surface, menu_rect)
        self.display.flip()

