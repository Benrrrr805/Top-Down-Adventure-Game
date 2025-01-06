from game.core.game_resources import GameResources
from game.scenes.uiComponents.containers.main_container import main_container
from game.scenes.uiComponents.uiComponent import UIComponent
from game.scenes.uiComponents.menus.main_menu import main_menu, new_game_button, load_game_button, settings_button, exit_button
# from game.scenes.uiComponents.menus.settings_menu import settings_menu

# Main menu scene
class StartingScene:
    def __init__(self):
        # Sets more basic values.
        # Further initialization is done in the initialize method.
        self.screen = None
        self.display = None
        self.debug = None
        self.main_container = None
        self.initialized = False
        
    def initialize(self):
        if self.initialized:
            raise Exception("StartingScene already initialized")
        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.link(main_container, child=main_menu)
        self.link(main_menu, children=[new_game_button, load_game_button, settings_button, exit_button])
        self.init_main_container()
        self.init_main_menu()
        self.init_main_menu_buttons()

        self.initialized = True

    def link(self, parent, child=None, children=None):
        if child:
            parent.add_child(child)
            child.add_parent(parent)
        if children:
            for child in children:
                parent.add_child(child)
                child.add_parent(parent)

    def init_main_container(self):
        main_container.initialize()
        self.main_container = main_container
        
    def init_main_menu(self):
        main_menu.initialize()

    def init_main_menu_buttons(self):
        new_game_button.initialize()
        load_game_button.initialize()
        settings_button.initialize()
        exit_button.initialize()

    def handle_events(self):
        if not self.initialized:
            raise Exception("Must initialize StartingScene before handling events")
        self.main_container.handle_events()
            
    def update(self):
        if not self.initialized:
            raise Exception("Must initialize StartingScene before updating")
        self.main_container.update()
 
    def draw(self):
        if not self.initialized:
            raise Exception("Must initialize StartingScene before drawing")
        
        main_container_surface = self.main_container.draw()

        if main_container_surface is None:
            raise Exception("Main container surface is None")
        
        main_container_rect = self.main_container.get_rect()
        self.screen.fill((0, 0, 0))
        self.screen.blit(main_container_surface, main_container_rect)
        self.display.flip()
