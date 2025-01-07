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

    def __init__(self):
        super().__init__(name="StartingScene")
        self.main_container = None

    def initialize(self, parent, top_level):
        super().initialize(parent, top_level)
        
        # Access the root game
        game = self.get_game()
        if not game:
            raise Exception("No Game found in parent chain.")

        self.screen = game.screen
        self.display = game.display

        # Mark UIComponents initialized
        self.main_container = main_container
        self.main_container.initialize(self, top_level=False)
        self.set_main_menu()        
        self.initialized = True


    def set_main_menu(self):
        if not main_menu.initialized:
            main_menu.initialize(self.main_container)
            new_game_button.initialize(main_menu)
            load_game_button.initialize(main_menu)
            settings_button.initialize(main_menu)
            exit_button.initialize(main_menu)

        self.link(self.main_container, main_menu)
        self.link(main_menu, children=[new_game_button, load_game_button, settings_button, exit_button])

        if not main_menu.active:
            main_menu.enable()

        self.current_menu = main_menu

    def unset_main_menu(self):
        self.unlink(self.main_container, main_menu)
        main_menu.disable()
        self.unlink(main_menu, children=[new_game_button, load_game_button, settings_button, exit_button])
        self.main_container.need_to_update = True
        self.current_menu = None

    def set_settings_menu(self):
        if not settings_menu.initialized:
            settings_menu.initialize(self.main_container)
            sound_button.initialize(settings_menu)
            music_button.initialize(settings_menu)
            back_button.initialize(settings_menu)
            darkness_button.initialize(settings_menu)
            show_fps_button.initialize(settings_menu)

        self.link(self.main_container, settings_menu)
        self.link(settings_menu, children=[sound_button, music_button, back_button, darkness_button, show_fps_button])

        if not settings_menu.active:
            settings_menu.enable()

        self.current_menu = settings_menu        

    def unset_settings_menu(self):
        self.unlink(self.main_container, settings_menu)
        settings_menu.disable()
        self.unlink(settings_menu, children=[sound_button, music_button, back_button, darkness_button, show_fps_button])

        self.main_container.need_to_update = True
        self.current_menu = None


    def handle_events(self):
        if not self.initialized:
            raise Exception("Must initialize StartingScene before handling events")
        
        if main_menu.clicked():
            print(f"Main menu clicked - {main_menu.name}")

        if self.current_menu and settings_button.clicked():
            # if not settings_menu.initialized:
            self.unset_main_menu()
            self.set_settings_menu()
        
        if self.current_menu == settings_menu and back_button.clicked():
            self.unset_settings_menu()
            self.set_main_menu()

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
