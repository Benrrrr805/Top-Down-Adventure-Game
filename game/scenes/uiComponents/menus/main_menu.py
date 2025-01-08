from game.scenes.uiComponents.menus.menu import Menu
from game.scenes.uiComponents.buttons.button import Button
from game.settings import RED, SCREEN_WIDTH, SCREEN_HEIGHT


main_menu_width = SCREEN_WIDTH - 100
main_menu_height = SCREEN_HEIGHT - 100

main_menu_x = SCREEN_WIDTH / 2 - main_menu_width / 2
main_menu_y = SCREEN_HEIGHT / 2 - main_menu_height / 2

main_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
main_menu_text = "Main Menu"

main_menu_text_size = 48
main_menu_text_position = (main_menu_width // 2, 50)

button_width = main_menu_width / 2
button_height = main_menu_height / 8

button_margin = 20

button_x = main_menu_width / 2 - button_width / 2
new_game_button_y = 140
load_game_button_y = new_game_button_y + button_height + button_margin
settings_button_y = load_game_button_y + button_height + button_margin
exit_button_y = settings_button_y + button_height + button_margin

button_text_size = 24
button_text_position = (button_width // 2, button_height // 2)
button_background_color = None

new_game_button = Button("new_game_button", False, button_width, button_height,  button_x, new_game_button_y,
                         text="New Game", text_size=button_text_size, text_position=button_text_position, 
                        background_color=button_background_color)

load_game_button = Button("load_game_button", False, button_width, button_height, button_x, load_game_button_y,
                          text="Load Game", text_size=button_text_size, text_position=button_text_position,
                          background_color=button_background_color)

settings_button = Button("settings_button", False, button_width, button_height, button_x, settings_button_y,
                         text="Settings", text_size=button_text_size, text_position=button_text_position, 
                            background_color=button_background_color)

exit_button = Button("exit_button", False, button_width, button_height, button_x, exit_button_y,
                     text="Exit", text_size=button_text_size, text_position=button_text_position, 
                        background_color=button_background_color)

main_menu = Menu("main_menu", False, main_menu_width, main_menu_height, main_menu_x, main_menu_y, 
                 text=main_menu_text, text_size=main_menu_text_size, text_position=main_menu_text_position, 
                 image_url=main_menu_background_image)
