from game.entities.uiComponents.containers.container import Container
from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT

main_container_background_image_url = "./assets/images/startingScene/starting_scene_background_1792x1024.png"
main_container_width = SCREEN_WIDTH
main_container_height = SCREEN_HEIGHT
main_container = Container(
    name="main_container", 
    top_level=False, 
    width=main_container_width, 
    height=main_container_height, 
    x_coordinate=0, 
    y_coordinate=0, 
    image_url=main_container_background_image_url)