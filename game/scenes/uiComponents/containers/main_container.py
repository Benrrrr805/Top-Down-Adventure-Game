from game.scenes.uiComponents.containers.container import Container
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

main_container_background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"
main_container_width = SCREEN_WIDTH
main_container_height = SCREEN_HEIGHT
main_container = Container("main_container", False, main_container_width, main_container_height, 0, 0, main_container_background_image_url)