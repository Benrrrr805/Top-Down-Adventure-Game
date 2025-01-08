# game/scenes/startingScene.py

from game.core.game_component import GameComponent
from game.scenes.uiComponents.containers.main_container import main_container
from game.scenes.uiComponents.menus.main_menu import main_menu, new_game_button, load_game_button, settings_button, exit_button
from game.scenes.uiComponents.menus.settings_menu import settings_menu, sound_button, music_button, back_button, darkness_button, show_fps_button
class StartingScene(GameComponent):
    """
    Example of a Scene that is also a GameComponent,
    so it can have children (UIComponents, etc.) and
    can access the global references from the Game via self.get_game().
    """

    def __init__(self, name, top_level=False):
        super().__init__(name, top_level)
        self.count = 0
        self.game = None
        self.main_container = main_container
        self.main_menu = main_menu

    def create_main_container(self):
        self.main_container = main_container

    def set_main_container(self):
        self.link(self, main_container)

    def set_main_menu(self):
        self.link(self.main_container, main_menu)

    def unset_main_menu(self):
        self.unlink(self.main_container, main_menu)

    def link_main_menu_to_children(self):
        self.link(main_menu, [new_game_button, load_game_button, settings_button, exit_button])
        
    def handle_events(self):
        if not self.active:
            raise ValueError("StartingScene is not active.")
        self.main_container.handle_events()

    def update(self):
        if not self.active:
            raise ValueError("StartingScene is not active.")
        self.main_container.update()

    def draw(self):
        if not self.active:
            raise ValueError("StartingScene is not active.")
        main_container_surface = self.main_container.draw()
        main_container_rect = self.main_container.get_rect()
        self.screen.fill(self.debug_color)
        self.screen.blit(main_container_surface, main_container_rect)
        self.display.flip()
