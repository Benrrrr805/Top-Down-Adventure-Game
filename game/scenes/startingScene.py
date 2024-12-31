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
        
        menu_x = 100
        menu_y = 100
        menu_width = 800
        menu_height = 600

        button_width = 300
        button_height = 100

        self.menu_background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"
        self.menu = Menu("startingScene", menu_width, menu_height, menu_x, menu_y, self.menu_background_image_url)

        # Buttons relative to the menu
        self.new_game_button = Button("new_game", button_width, button_height,  5, 120)
        self.load_game_button = Button("load_game", button_width, button_height, 120, 240)
        self.setting_button = Button("settings", button_width, button_height, 120, 360)
        self.exit_button = Button(exit, button_width, button_height, 120, 480)

        self.menu.add_child(self.new_game_button)
        self.menu.add_child(self.load_game_button)
        self.menu.add_child(self.setting_button)
        self.menu.add_child(self.exit_button)

    def handle_events(self):
        self.menu.handle_events()
            
    def update(self):
        self.menu.update()
 
    def draw(self):
        menu_surface = self.menu.draw()
        menu_rect = self.menu.get_rect()
        self.screen.blit(menu_surface, menu_rect)
        self.display.flip()
