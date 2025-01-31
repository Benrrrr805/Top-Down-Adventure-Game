from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import os

if TYPE_CHECKING:
    from game.core.visual_component import VisualComponent

class VisualComponentValidation:
    """
    A class to validate VisualComponent objects.
    """
    @staticmethod
    def validate_rect(visual_component: 'VisualComponent') -> bool:
        if visual_component.rect is not None and not isinstance(visual_component.rect, pygame.Rect):
            raise ValueError(f"Rect must be a pygame.Rect. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_surface(visual_component: 'VisualComponent') -> bool:
        if visual_component.surface is not None and not isinstance(visual_component.surface, pygame.Surface):
            raise ValueError(f"Surface must be a pygame.Surface. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_image_url(visual_component: 'VisualComponent') -> bool:
        if not visual_component.image_url:
            return False
        if visual_component.image_url is not None and not isinstance(visual_component.image_url, str):
            raise ValueError(f"Image URL must be a string. - {visual_component.name}")
        if not os.path.exists(visual_component.image_url):
            raise ValueError(f"Image URL does not exist. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_background_color(visual_component: 'VisualComponent') -> bool:
        if not visual_component.background_color:
            return False
        if visual_component.background_color is not None and not isinstance(visual_component.background_color, tuple):
            raise ValueError(f"Background color must be a tuple. - {visual_component.name}")
        if len(visual_component.background_color) not in (3, 4):
            raise ValueError(f"Background color must be an RGB or RGBA tuple. - {visual_component.name}")
        return True

    @staticmethod
    def validate_background_image(visual_component: 'VisualComponent') -> bool:
        if not visual_component.background_image:
            return False
        if visual_component.background_image is not None and not isinstance(visual_component.background_image, pygame.Surface):
            raise ValueError(f"Background image must be a pygame.Surface. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_width(visual_component: 'VisualComponent') -> bool:
        if visual_component.width is None:
            raise ValueError(f"GameComponent must have a width and height. - {visual_component.name}")
        if not isinstance(visual_component.width, int):
            raise ValueError(f"Width must be an integer. - {visual_component.name}")
        return True

    @staticmethod
    def validate_height(visual_component: 'VisualComponent') -> bool:
        if visual_component.height is None:
            raise ValueError(f"GameComponent must have a width and height. - {visual_component.name}")
        if not isinstance(visual_component.height, int):
            raise ValueError(f"Height must be an integer. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_x_coordinate(visual_component: 'VisualComponent') -> bool:
        if visual_component.x_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {visual_component.name}")
        if not isinstance(visual_component.x_coordinate, int):
            raise ValueError(f"{type(visual_component.x_coordinate)}X coordinate must be an integer. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_y_coordinate(visual_component: 'VisualComponent') -> bool:
        if visual_component.y_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {visual_component.name}")
        if not isinstance(visual_component.y_coordinate, int):
            raise ValueError(f"Y coordinate must be an integer. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_text(visual_component: 'VisualComponent') -> bool:
        if visual_component.text is not None and not isinstance(visual_component.text, str):
            raise ValueError(f"Text must be a string. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_text_font(visual_component: 'VisualComponent') -> bool:
        if visual_component.text_font is not None and not isinstance(visual_component.text_font, pygame.font.Font):
            raise ValueError(f"Text font must be a pygame.font.Font. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_text_size(visual_component: 'VisualComponent') -> bool:
        if visual_component.text_size is not None and not isinstance(visual_component.text_size, int):
            raise ValueError(f"Text size must be an integer. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_text_color(visual_component: 'VisualComponent') -> bool:
        if not visual_component.text_color:
            return False
        if visual_component.text_color is not None and not isinstance(visual_component.text_color, tuple):
            raise ValueError(f"Text color must be a tuple. - {visual_component.name}")
        if len(visual_component.text_color) not in (3, 4):
            raise ValueError(f"Text color must be an RGB or RGBA tuple. - {visual_component.name}")
        return True
    
    @staticmethod
    def validate_text_position(visual_component: 'VisualComponent') -> bool:
        if not visual_component.text_position:
            return False
        if visual_component.text_position is not None and not isinstance(visual_component.text_position, tuple):
            raise ValueError(f"Text position must be a tuple. - {visual_component.name}")
        if len(visual_component.text_position) != 2:
            raise ValueError(f"Text position must be an (x, y) tuple. - {visual_component.name}")
        return True

    @staticmethod
    def validate_base_values(visual_component: 'VisualComponent') -> bool:
        VisualComponentValidation.validate_rect(visual_component)
        VisualComponentValidation.validate_surface(visual_component)
        VisualComponentValidation.validate_image_url(visual_component)
        VisualComponentValidation.validate_background_color(visual_component)
        VisualComponentValidation.validate_background_image(visual_component)
        VisualComponentValidation.validate_width(visual_component)
        VisualComponentValidation.validate_height(visual_component)
        VisualComponentValidation.validate_x_coordinate(visual_component)
        VisualComponentValidation.validate_y_coordinate(visual_component)
        VisualComponentValidation.validate_text(visual_component)
        VisualComponentValidation.validate_text_font(visual_component)
        VisualComponentValidation.validate_text_size(visual_component)
        VisualComponentValidation.validate_text_color(visual_component)
        VisualComponentValidation.validate_text_position(visual_component)
        return True        
    
    @staticmethod
    def full_validate(visual_component: 'VisualComponent') -> bool:
        VisualComponentValidation.validate_is_visual_component(visual_component)
        VisualComponentValidation.validate_base_values(visual_component)
        return True
    
    @staticmethod
    def validate_is_visual_component(visual_component: 'VisualComponent') -> bool:
        """
        Validates that the given object is a VisualComponent.
        """
        if not type(visual_component).__name__ == 'VisualComponent':
            raise ValueError(f'Expected: VisualComponent. Recieved: {type(visual_component).__name__}')
        return True
