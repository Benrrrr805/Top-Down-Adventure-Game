from game.scenes.uiComponents.menus.menu import Menu
from game.scenes.uiComponents.buttons.button import Button

main_menu_width = 500
main_menu_height = 600
main_menu_x = 1792 / 2 - main_menu_width / 2
main_menu_y = 1024 / 2 - main_menu_height / 2
main_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
main_menu_text = "Main Menu"
main_menu_text_size = 48
main_menu_text_position = (main_menu_width // 2, 50)

button_width = 300
button_height = 50
button_x = main_menu_width / 2 - button_width / 2
button_text_size = 24
button_text_position = (button_width // 2, button_height // 2)
button_background_color = None
active = True

new_game_button = Button("new_game_button", button_width, button_height,  button_x, 120, 
                         text="New Game", text_size=button_text_size, text_position=button_text_position, 
                         active=active, background_color=button_background_color)

load_game_button = Button("load_game_button", button_width, button_height, button_x, 240, 
                          text="Load Game", text_size=button_text_size, text_position=button_text_position, 
                          active=active, background_color=button_background_color)

settings_button = Button("settings_button", button_width, button_height, button_x, 360, 
                         text="Settings", text_size=button_text_size, text_position=button_text_position, 
                         active=active, background_color=button_background_color)

exit_button = Button("exit_button", button_width, button_height, button_x, 480, 
                     text="Exit", text_size=button_text_size, text_position=button_text_position, 
                     active=active, background_color=button_background_color)

main_menu = Menu("main_menu", main_menu_width, main_menu_height, main_menu_x, main_menu_y, 
                 text=main_menu_text, text_size=main_menu_text_size, text_position=main_menu_text_position, 
                 active=active, background_image=main_menu_background_image)

def clicked_item(self):
    if self.active:
        if self.clicked() and self.name is not None:
            print(f"Clicked {self.name}")

new_game_button.add_helper_function(clicked_item)
load_game_button.add_helper_function(clicked_item)
settings_button.add_helper_function(clicked_item)
exit_button.add_helper_function(clicked_item)
main_menu.add_helper_function(clicked_item)

main_menu.add_child(new_game_button)
main_menu.add_child(load_game_button)
main_menu.add_child(settings_button)
main_menu.add_child(exit_button)

new_game_button.add_parent(main_menu)
load_game_button.add_parent(main_menu)
settings_button.add_parent(main_menu)
exit_button.add_parent(main_menu)
