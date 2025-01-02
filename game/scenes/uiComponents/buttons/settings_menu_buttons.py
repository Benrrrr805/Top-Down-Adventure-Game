from game.scenes.uiComponents.buttons.button import Button
from game.scenes.uiComponents.menus.settings_menu import settings_menu_width


button_width = 300
button_height = 50
button_x = settings_menu_width / 2 - button_width / 2

sound_button = Button("sound_button", button_width, button_height, button_x, 240, text="Sound")
music_button = Button("music_button", button_width, button_height, button_x, 320, text="Music")
back_button = Button("back_button", button_width, button_height, button_x, 480, text="Back")

