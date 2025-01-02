from game.scenes.uiComponents.buttons.button import Button
from game.scenes.uiComponents.menus.main_menu import main_menu_width


button_width = 300
button_height = 50
button_x = main_menu_width / 2 - button_width / 2

new_game_button = Button("new_game_button", button_width, button_height,  button_x, 120, text="New Game")
load_game_button = Button("load_game_button", button_width, button_height, button_x, 240, text="Load Game")
settings_button = Button("settings_button", button_width, button_height, button_x, 360, text="Settings")
exit_button = Button("exit_button", button_width, button_height, button_x, 480, text="Exit")