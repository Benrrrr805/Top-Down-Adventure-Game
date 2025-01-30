import pygame
class GameValuesManager:
    def __init__(self):

        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red':   (255, 0, 0),
            'green': (0, 255, 0),
            'blue':  (0, 0, 255),
        }

        self.screen_width = 800
        self.screen_height = 800
        self.fps = 60
        self.debug = True
        self.frame_rate = None
        self.show_fps = False
        self.debug_color = self.colors['black']
        self.title = "Top-Down Adventure Game"

        pygame.init()
        pygame.font.init()

        self.pygame = pygame
        self.display = pygame.display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.pygame.display.set_caption(self.title)
        self.clock = self.pygame.time.Clock()
        
