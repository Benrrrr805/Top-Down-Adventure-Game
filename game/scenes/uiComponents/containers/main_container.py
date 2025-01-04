from game.scenes.uiComponents.uiComponent import UIComponent
from game.settings import BLACK

from game.scenes.uiComponents.menus.settings_menu import settings_menu
from game.scenes.uiComponents.menus.main_menu import main_menu

class MainContainer(UIComponent):
    def __init__(self, name, width, height, x_coordinate, y_coordinate, 
                 background_image=None, background_color = None, 
                 text=None, text_font=None, text_size=24, text_color=BLACK, text_position=None, 
                 active=True, need_to_update=True, debug_color=BLACK,
                 parent=None, children=None
                 ):
        super().__init__(name, width, height, x_coordinate, y_coordinate, 
                         background_image, background_color, 
                         text, text_font, text_size, text_color, text_position,
                         active, need_to_update, debug_color, 
                         parent, children)
        self.menus = {
            "main_menu": main_menu,
            "settings_menu": settings_menu
        }
        