from game.scenes.uiComponents.menus.menu import Menu
from game.scenes.uiComponents.buttons.button import Button

settings_menu_width = 500
settings_menu_height = 600
settings_menu_x = 1792 / 2 - settings_menu_width / 2
settings_menu_y = 1024 / 2 - settings_menu_height / 2
settings_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
settings_menu_text = "Settings"
settings_menu_text_size = 48
settings_menu_text_position = (settings_menu_width // 2, 50)
active = False

button_width = 300
button_height = 50
button_x = 500 / 2 - button_width / 2
button_text_size = 24
button_text_position = (button_width // 2, button_height // 2)
button_background_color = None

sound_button = Button("sound_button", button_width, button_height, button_x, 240, 
                      text="Sound", text_size=button_text_size, text_position=button_text_position, 
                      active=active, background_color=button_background_color)

music_button = Button("music_button", button_width, button_height, button_x, 320, 
                      text="Music", text_size=button_text_size, text_position=button_text_position, 
                      active=active, background_color=button_background_color)

back_button = Button("back_button", button_width, button_height, button_x, 480, 
                     text="Back", text_size=button_text_size, text_position=button_text_position, 
                     active=active, background_color=button_background_color)

darkness_button = Button("darkness_button", button_width, button_height, button_x, 400, 
                         text="Darkness", text_size=button_text_size, text_position=button_text_position, 
                         active=active, background_color=button_background_color)

show_fps_button = Button("show_fps_button", button_width, button_height, button_x, 400, 
                         text="Show FPS", text_size=button_text_size, text_position=button_text_position, 
                         active=active, background_color=button_background_color)

settings_menu = Menu("settings_menu", settings_menu_width, settings_menu_height, settings_menu_x, settings_menu_y, 
                     text=settings_menu_text, text_size=settings_menu_text_size, text_position=settings_menu_text_position, 
                     active=active, background_image=settings_menu_background_image)

settings_menu.add_child(sound_button)
settings_menu.add_child(music_button)
settings_menu.add_child(back_button)
settings_menu.add_child(darkness_button)
settings_menu.add_child(show_fps_button)

sound_button.add_parent(settings_menu)
music_button.add_parent(settings_menu)
back_button.add_parent(settings_menu)
darkness_button.add_parent(settings_menu)
show_fps_button.add_parent(settings_menu)
