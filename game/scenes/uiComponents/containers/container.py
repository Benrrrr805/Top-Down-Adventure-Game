# from game.scenes.uiComponents.uiComponent import UIComponent
from game.core.game_component import GameComponent
from game.settings import BLACK

class Container(GameComponent):
    def __init__(self, name, top_level,
                 width, height, x_coordinate, y_coordinate, 
                 image_url=None, background_color = None, 
                 text=None, text_font=None, text_size=24, text_color=BLACK, text_position=None):
        super().__init__(name, top_level, True, 
                         width, height, x_coordinate, y_coordinate, 
                         image_url, background_color, 
                         text, text_font, text_size, text_color, text_position)
        