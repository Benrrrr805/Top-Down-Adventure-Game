from game.scenes.uiComponents.buttons.button import Button
from game.scenes.uiComponents.menus.mainMenu import main_menu_width


button_width = 300
button_height = 50
button_x = main_menu_width / 2 - button_width / 2

exit_button = Button("exit_button", button_width, button_height, button_x, 480, text="Exit")