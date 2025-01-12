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

    def set_scene(self, game=None):
        self.link_child(self.main_container)
        self.main_container.link_child(self.main_menu)
        self.main_menu.link_children([new_game_button, load_game_button, settings_button, exit_button])
        self.set_game_values(game)
        self.set_game_values_for_children(self.game)
            
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
