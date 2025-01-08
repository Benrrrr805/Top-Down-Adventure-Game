from game.scenes.uiComponents.menus.menu import Menu
from game.scenes.uiComponents.buttons.button import Button
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

settings_menu_width = SCREEN_WIDTH - 100
settings_menu_height = SCREEN_HEIGHT - 100

settings_menu_x = SCREEN_WIDTH / 2 - settings_menu_width / 2
settings_menu_y = SCREEN_HEIGHT / 2 - settings_menu_height / 2

settings_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
settings_menu_text = "Settings"

settings_menu_text_size = 48
settings_menu_text_position = (settings_menu_width // 2, 50)

button_width = settings_menu_width / 2
button_height = settings_menu_height / 8

button_margin = 20

button_x = settings_menu_width / 2 - button_width / 2
sound_button_y = 140
music_button_y = sound_button_y + button_height + button_margin
darkness_button_y = music_button_y + button_height + button_margin
show_fps_button_y = darkness_button_y + button_height + button_margin
back_button_y = show_fps_button_y + button_height + button_margin


button_text_size = 24
button_text_position = (button_width // 2, button_height // 2)
button_background_color = None

sound_button = Button("sound_button", False,
                      button_width, button_height, button_x, sound_button_y,
                      text="Sound", text_size=button_text_size, text_position=button_text_position, 
                      background_color=button_background_color)

music_button = Button("music_button", False,
                      button_width, button_height, button_x, music_button_y,
                      text="Music", text_size=button_text_size, text_position=button_text_position, 
                      background_color=button_background_color)

back_button = Button("back_button", False,
                     button_width, button_height, button_x, back_button_y,
                     text="Back", text_size=button_text_size, text_position=button_text_position, 
                     background_color=button_background_color)

darkness_button = Button("darkness_button", False,
                         button_width, button_height, button_x, darkness_button_y,
                         text="Darkness", text_size=button_text_size, text_position=button_text_position, 
                         background_color=button_background_color)

show_fps_button = Button("show_fps_button", False,
                         button_width, button_height, button_x, show_fps_button_y,
                         text="Show FPS", text_size=button_text_size, text_position=button_text_position, 
                         background_color=button_background_color)

settings_menu = Menu("settings_menu", False,
                     settings_menu_width, settings_menu_height, settings_menu_x, settings_menu_y, 
                     text=settings_menu_text, text_size=settings_menu_text_size, text_position=settings_menu_text_position, 
                     image_url=settings_menu_background_image)
