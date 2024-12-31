from game.scenes.helpers.uiComponent import UIComponent

class Menu(UIComponent):
    def __init__(self, name, width, height, x_coordinate, y_coordinate, background_image=None, children=[]):
        super().__init__(name, width, height, x_coordinate, y_coordinate, background_image, children)
        