from game.scenes.uiComponents.menus.menu import Menu
from game.scenes.uiComponents.buttons.button import Button
from game.core.game_resources import GameResources
from game.settings import WHITE, GREEN, RED


event_queue = GameResources.event_queue
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
button_background_color = RED
active = True

new_game_button = Button("new_game_button", button_width, button_height,  button_x, 120, 
                         text="New Game", text_size=button_text_size, text_position=button_text_position, 
                        background_color=button_background_color, image_url=main_menu_background_image)

load_game_button = Button("load_game_button", button_width, button_height, button_x, 240, 
                          text="Load Game", text_size=button_text_size, text_position=button_text_position, 
                        image_url=main_menu_background_image)

settings_button = Button("settings_button", button_width, button_height, button_x, 360, 
                         text="Settings", text_size=button_text_size, text_position=button_text_position, 
                         image_url=main_menu_background_image)

exit_button = Button("exit_button", button_width, button_height, button_x, 480, 
                     text="Exit", text_size=button_text_size, text_position=button_text_position, 
                     image_url=main_menu_background_image)


main_menu = Menu("main_menu", main_menu_width, main_menu_height, main_menu_x, main_menu_y, 
                 text=main_menu_text, text_size=main_menu_text_size, text_position=main_menu_text_position, 
                 image_url=main_menu_background_image)

