from game.core.game_resources import GameResources
from game.scenes.uiComponents.buttons.newGame import new_game_button
from game.scenes.uiComponents.buttons.loadGame import load_game_button
from game.scenes.uiComponents.buttons.settings import settings_button
from game.scenes.uiComponents.buttons.exit import exit_button
from game.scenes.uiComponents.menus.mainMenu import main_menu
from game.scenes.uiComponents.containers.mainContainer import main_container

# Main menu scene
class StartingScene:
    def __init__(self):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.main_container = main_container
        self.main_menu = main_menu
        self.new_game_button = new_game_button
        self.load_game_button = load_game_button
        self.settings_button = settings_button
        self.exit_button = exit_button

        self.main_menu.add_child(self.new_game_button)
        self.main_menu.add_child(self.load_game_button)
        self.main_menu.add_child(self.settings_button)
        self.main_menu.add_child(self.exit_button)
        self.main_container.add_child(self.main_menu)

    def handle_events(self):
        self.main_container.handle_events()
            
    def update(self):
        self.main_container.update()
 
    def draw(self):
        main_container_surface = self.main_container.draw()
        main_container_rect = self.main_container.get_rect()
        self.screen.blit(main_container_surface, main_container_rect)
        self.display.flip()
