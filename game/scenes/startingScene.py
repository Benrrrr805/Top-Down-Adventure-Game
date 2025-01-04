from game.core.game_resources import GameResources
from game.scenes.uiComponents.containers.main_container import main_container

# Main menu scene
class StartingScene:
    def __init__(self):

        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.main_container = main_container

    def handle_events(self):
        self.main_container.handle_events()
            
    def update(self):
        self.main_container.update()
 
    def draw(self):
        main_container_surface = self.main_container.draw()
        main_container_rect = self.main_container.get_rect()
        self.screen.blit(main_container_surface, main_container_rect)
        self.display.flip()
