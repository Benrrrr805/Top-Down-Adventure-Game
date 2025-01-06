# game/scenes/startingScene.py

from game.core.game_component import GameComponent
from game.scenes.uiComponents.containers.main_container import main_container
from game.scenes.uiComponents.uiComponent import UIComponent
from game.scenes.uiComponents.menus.main_menu import main_menu, new_game_button, load_game_button, settings_button, exit_button

class StartingScene(GameComponent):
    """
    Example of a Scene that is also a GameComponent,
    so it can have children (UIComponents, etc.) and
    can access the global references from the Game via self.get_game().
    """

    def __init__(self):
        super().__init__(name="StartingScene", top_level=False)
        self.main_container = None

    def initialize(self):
        super().initialize()
        
        # Access the root game
        game = self.get_game()
        if not game:
            raise Exception("No Game found in parent chain.")

        self.screen = game.screen
        self.display = game.display

        self.link(self, child=main_container)
        self.link(main_container, children=[main_menu, new_game_button, load_game_button, settings_button, exit_button])

        self.initialized = True


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
