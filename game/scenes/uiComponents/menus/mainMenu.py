from game.scenes.uiComponents.menus.menu import Menu

main_menu_width = 500
main_menu_height = 600
main_menu_x = 1792 / 2 - main_menu_width / 2
main_menu_y = 1024 / 2 - main_menu_height / 2
main_menu_background_image = "./assets/images/UI/Panel/Window/Big.png"
main_menu_text = "Main Menu"
main_menu_text_size = 48
main_menu_text_position = (main_menu_width // 2, 50)

main_menu = Menu("main_menu", main_menu_width, main_menu_height, main_menu_x, main_menu_y, main_menu_background_image, text=main_menu_text, text_size=main_menu_text_size, text_position=main_menu_text_position)
