from game.core.visual_component import VisualComponent
from game.validation.game_component_validator import GameComponentValidator
import pygame
import os
class VisualComponentValidator(GameComponentValidator):
    """
    A validator for VisualComponent objects.
    """
    @staticmethod
    def validate_base_values(visual_component: 'VisualComponent') -> bool:
        """
        Validate base GameComponent values, then optionally validate UI details.
        self.rect: Rect = None
        self.surface: Surface = None
        self.image_url: str = image_url
        self.background_color: tuple[int, int, int] = background_color
        self.background_image: Surface = None
        self.width: int = width
        self.height: int = height
        self.x_coordinate: int = x_coordinate
        self.y_coordinate: int = y_coordinate
        self.text: str = text
        self.text_font: Font = text_font
        self.text_size: int = text_size
        self.text_color: tuple[int, int, int] = text_color
        self.text_position: tuple[int, int] = text_position
        self.debug_color: tuple[int, int, int] = None
        self.graphical_values_set: bool = False
        """
        
        if visual_component.rect is not None and not isinstance(visual_component.rect, pygame.Rect):
            raise ValueError(f"Rect must be a pygame.Rect. - {visual_component.name}")
        if visual_component.surface is not None and not isinstance(visual_component.surface, pygame.Surface):
            raise ValueError(f"Surface must be a pygame.Surface. - {visual_component.name}")
        if not isinstance(visual_component.image_url, str):
            raise ValueError(f"Image URL must be a string. - {visual_component.name}")
        if not os.path.exists(visual_component.image_url):
            raise ValueError(f"Image URL does not exist. - {visual_component.name}")
        if visual_component.background_color is not None and not isinstance(visual_component.background_color, tuple):
            raise ValueError(f"Background color must be a tuple. - {visual_component.name}")
        if visual_component.background_image is not None and not isinstance(visual_component.background_image, pygame.Surface):
            raise ValueError(f"Background image must be a pygame.Surface. - {visual_component.name}")
        if visual_component.width is None:
            raise ValueError(f"GameComponent must have a width and height. - {visual_component.name}")
        if visual_component.height is None:
            raise ValueError(f"GameComponent must have a width and height. - {visual_component.name}")
        if visual_component.x_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {visual_component.name}")
        if visual_component.y_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {visual_component.name}")
        if visual_component.text is not None and not isinstance(visual_component.text, str):
            raise ValueError(f"Text must be a string. - {visual_component.name}")
        if visual_component.text_font is not None and not isinstance(visual_component.text_font, pygame.font.Font):
            raise ValueError(f"Text font must be a pygame.font.Font. - {visual_component.name}")
        if visual_component.text_size is not None and not isinstance(visual_component.text_size, int):
            raise ValueError(f"Text size must be an integer. - {visual_component.name}")
        if visual_component.text_color is not None and not isinstance(visual_component.text_color, tuple):
            raise ValueError(f"Text color must be a tuple. - {visual_component.name}")
        if visual_component.text_color is not None and len(visual_component.text_color) not in (3, 4):
            raise ValueError(f"Text color must be an RGB or RGBA tuple. - {visual_component.name}")
        if visual_component.text_position is not None and not isinstance(visual_component.text_position, tuple):
            raise ValueError(f"Text position must be a tuple. - {visual_component.name}")
        if visual_component.text_position is not None and len(visual_component.text_position) != 2:
            raise ValueError(f"Text position must be an (x, y) tuple. - {visual_component.name}")
        if visual_component.debug_color is not None and not isinstance(visual_component.debug_color, tuple):
            raise ValueError(f"Debug color must be a tuple. - {visual_component.name}")
        if visual_component.debug_color is not None and len(visual_component.debug_color) not in (3, 4):
            raise ValueError(f"Debug color must be an RGB or RGBA tuple. - {visual_component.name}")
        if not isinstance(visual_component.graphical_values_set, bool):
            raise ValueError(f"GameComponent: {visual_component.name} - Failed validation. pygame_values_set must be a boolean.")
        
        return True
    
    @staticmethod
    def full_validate(visual_component: 'VisualComponent') -> bool:
        VisualComponentValidator.validate_is_visual_component(visual_component)
        VisualComponentValidator.validate_base_values(visual_component)
        return True
        
    def validate_is_visual_component(visual_component: 'VisualComponent') -> bool:
        """
        Validates that the given object is a VisualComponent.
        """
        if not isinstance(visual_component, VisualComponent):
            raise ValueError(f'Expected: GameComponent. Recieved: {type(visual_component).__name__}')
        return True
