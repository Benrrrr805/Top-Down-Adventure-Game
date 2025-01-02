from game.scenes.uiComponents.menus.menu import Menu

settings_menu_width = 500
settings_menu_height = 600
settings_menu_x = 1792 / 2 - settings_menu_width / 2
settings_menu_y = 1024 / 2 - settings_menu_height / 2
settings_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
settings_menu_text = "Settings"
settings_menu_text_size = 48
settings_menu_text_position = (settings_menu_width // 2, 50)

settings_menu = Menu("settings_menu", settings_menu_width, settings_menu_height, settings_menu_x, settings_menu_y, settings_menu_background_image, text=settings_menu_text, text_size=settings_menu_text_size, text_position=settings_menu_text_position)