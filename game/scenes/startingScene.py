from game.scenes.helpers.button import Button
from game.scenes.helpers.menu import Menu

# Main menu scene
class StartingScene:
    def __init__(self):
        
        self.new_game_button = Button(740, 465, 380, 100, "new_game")
        self.load_game_button = Button(740, 585, 380, 100, "load_game")
        self.setting_button = Button(740, 705, 380, 100, "settings")
        self.exit_button = Button(740, 825, 380, 100, "exit")
        self.buttons = [self.new_game_button, self.load_game_button, self.setting_button, self.exit_button]
        self.background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"
        self.menu = Menu(self.background_image_url, self.buttons)

    def handle_events(self):
        self.menu.handle_events()
            
        
    def update(self):
        self.menu.update()

 
    def draw(self):
        self.menu.draw()

