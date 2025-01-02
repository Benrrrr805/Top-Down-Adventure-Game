# Core game logic
from game.scenes.startingScene import StartingScene
from game.core.game_resources import GameResources


class Game:
    def __init__(self):
        self.pygame = GameResources.pygame
        self.debug = GameResources.debug
        self.sreen = GameResources.screen
        self.display = GameResources.display
        self.clock = self.pygame.time.Clock()
        self.running = GameResources.running
        self.state = "startingScene"
        self.scene = None
        self.frame_rate = None
        self.show_fps = False

    def handle_events(self):
        for event in self.pygame.event.get():
            if self.is_terminated(event):
                self.closeWindow()
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                self.pygame.event.post(event)
        if self.scene:
            self.scene.handle_events()

    def closeWindow(self):
        GameResources.running = False
        self.running = False

    def is_terminated(self, event):
        return event.type == self.pygame.QUIT or (event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_ESCAPE)

    def update(self):
        if self.state == "startingScene" and self.scene == None:
            self.scene = StartingScene()
        self.scene.update()

    def draw(self):
        self.scene.draw()

    def run(self):
        while GameResources.running:
            self.handle_events()
            self.update()
            self.draw()
            ticks = self.clock.tick()
            self.frame_rate = int(self.clock.get_fps())
            if self.show_fps and self.frame_rate:
                print(f'frame_rate: {self.frame_rate}  -  milliseconds since last call: {ticks}')
        self.pygame.quit()