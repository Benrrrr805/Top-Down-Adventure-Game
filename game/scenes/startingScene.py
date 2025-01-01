from game.scenes.helpers.button import Button
from game.scenes.helpers.menu import Menu
from game.scenes.helpers.main_container import MainContainer
from game.core.game_resources import GameResources
from game.settings import RED
import pygame

# Main menu scene
class StartingScene:
    def __init__(self):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.main_container_width = 1792
        self.main_container_height = 1024

        menu_width = 500
        menu_height = 600
        menu_x = self.main_container_width / 2 - menu_width / 2
        menu_y = self.main_container_height / 2 - menu_height / 2

        button_width = 300
        button_height = 50
        button_x = menu_width / 2 - button_width / 2

        self.main_container_background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"
        
        
        self.main_container = MainContainer("main_container", self.main_container_width, self.main_container_height, 0, 0, self.main_container_background_image_url)
        self.menu = Menu("menu", menu_width, menu_height, menu_x, menu_y)

        # Buttons relative to the menu
        self.new_game_button = Button("new_game", button_width, button_height,  button_x, 120)
        self.load_game_button = Button("load_game", button_width, button_height, button_x, 240)
        self.setting_button = Button("settings", button_width, button_height, button_x, 360)
        self.exit_button = Button("exit", button_width, button_height, button_x, 480)

        self.menu.add_child(self.new_game_button)
        self.menu.add_child(self.load_game_button)
        self.menu.add_child(self.setting_button)
        self.menu.add_child(self.exit_button)
        self.main_container.add_child(self.menu)

    def handle_events(self):
        self.main_container.handle_events()
            
    def update(self):
        self.main_container.update()
 
    def draw(self):
        main_container_surface = self.main_container.draw()
        main_container_rect = self.main_container.get_rect()
        self.screen.blit(main_container_surface, main_container_rect)
        self.display.flip()
