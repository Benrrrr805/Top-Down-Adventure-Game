from game.scenes.helpers.uiComponent import UIComponent
from game.settings import BLACK

class MainContainer(UIComponent):
    def __init__(self, name, width, height, x_coordinate, y_coordinate, background_image=None, background_color = None, active=True, need_to_update=True, debug_color=BLACK, parent=None, children=[]):
        super().__init__(name, width, height, x_coordinate, y_coordinate, background_image, background_color, active, need_to_update, debug_color, parent, children)
        