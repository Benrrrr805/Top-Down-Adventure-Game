from game.scenes.uiComponents.uiComponent import UIComponent
from game.settings import BLACK
from game.core.game_resources import GameResources

class Button(UIComponent):
    def __init__(self, name, width, height, x_coordinate, y_coordinate, 
                 background_image=None, background_color = None, 
                 text=None, text_font=None, text_size=24, text_color=BLACK, text_position=None, 
                 active=True, need_to_update=True, debug_color=BLACK, 
                 parent=None, children=[]):
        super().__init__(name, width, height, x_coordinate, y_coordinate, 
                         background_image, background_color, 
                         text, text_font, text_size, text_color, text_position,
                         active, need_to_update, debug_color, 
                         parent, children)
        

    # def handle_events(self):
    #     if self.clicked():
    #         if self.name == "exit_button":
    #             GameResources.running = False
    #             print("Exiting the game")
    #             # pygame.quit()
    #         elif self.name == "settings_button":
    #             print("Settings button clicked")
    #             print(self.parent)
    #             print(self.parent.name)
    #             if self.parent is not None and self.parent.name == "main_menu":
    #                 print("setting parent is menu")
                    
    #                 if self.parent.parent is not None and self.parent.parent.name == "main_container":
    #                     print("setting parent parent is main_container")
    #                     if self.parent.parent.settings_menu is not None:
    #                         print("settings menu is not None")
    #                     self.parent.parent.add_child(self.parent.parent.settings_menu)
    #                     self.parent.delete()
                        
                # if parent.name == "menu":
                    # self.parent.parent.add_child(self.parent.parent.settings_menu)
                    # self.parent.delete()
                # self.parent.parent.add_child(self.parent.parent.settings_menu)
                # self.parent.delete()
                # self.parent.delete()
                # self.parent = None
                # self.parent = self.parent.parent
                # self.parent.add_child(self.parent.settings_menu)
                
        if self.active:
            return self.handle_events_()
        return None
