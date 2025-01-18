from game.core.visual_component import VisualComponent
from game.validation.game_component_validator import GameComponentValidator
import pygame
class VisualComponentValidator(GameComponentValidator):
    """
    A validator for VisualComponent objects.
    """
    @staticmethod
    def validate_base_values(visual_component: 'VisualComponent') -> bool:
        """
        Validate base GameComponent values, then optionally validate UI details.
        """
        if not isinstance(visual_component.pygame_values_set, bool):
            raise ValueError(f"GameComponent: {VisualComponent.name} - Failed validation. pygame_values_set must be a boolean.")

        if visual_component.width is None or visual_component.height is None:
            raise ValueError(f"GameComponent must have a width and height. - {visual_component.name}")
        if visual_component.x_coordinate is None or visual_component.y_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {visual_component.name}")
        if visual_component.debug_color is not None and not isinstance(visual_component.debug_color, tuple):
            raise ValueError(f"Debug color must be a tuple. - {visual_component.name}")
        if visual_component.debug_color is not None and len(visual_component.debug_color) not in (3, 4):
            raise ValueError(f"Debug color must be an RGB or RGBA tuple. - {visual_component.name}")
        if visual_component.text is not None and not isinstance(visual_component.text, str):
            raise ValueError(f"Text must be a string. - {visual_component.name}")
        if visual_component.text_size is not None and not isinstance(visual_component.text_size, int):
            raise ValueError(f"Text size must be an integer. - {visual_component.name}")
        if visual_component.text_position is not None and not isinstance(visual_component.text_position, tuple):
            raise ValueError(f"Text position must be a tuple. - {visual_component.name}")
        if visual_component.text_position is not None and len(visual_component.text_position) != 2:
            raise ValueError(f"Text position must be an (x, y) tuple. - {visual_component.name}")
        if visual_component.text_color is not None and not isinstance(visual_component.text_color, tuple):
            raise ValueError(f"Text color must be a tuple. - {visual_component.name}")
        if visual_component.text_color is not None and len(visual_component.text_color) not in (3, 4):
            raise ValueError(f"Text color must be an RGB or RGBA tuple. - {visual_component.name}")

        # Pygame specific checks
        if visual_component.pygame is None or not visual_component.pygame is pygame:
            raise ValueError(f"VisualComponent must have a pygame instance. - {visual_component.name}")
        if visual_component.screen is None or not isinstance(visual_component.screen, pygame.Surface):
            raise ValueError(f"VisualComponent must have a screen. - {visual_component.name}")
        if visual_component.display is None or not visual_component.display is pygame.display:
            raise ValueError(f"VisualComponent must have a display. - {visual_component.name}")
        if visual_component.rect is not None and not isinstance(visual_component.rect, pygame.Rect):
            raise ValueError(f"Rect must be a pygame.Rect. - {visual_component.name}")
        if visual_component.surface is not None and not isinstance(visual_component.surface, pygame.Surface):
            raise ValueError(f"Surface must be a pygame.Surface. - {visual_component.name}")
        if visual_component.background_image is not None and not isinstance(visual_component.background_image, pygame.Surface):
            raise ValueError(f"Background image must be a pygame.Surface. - {visual_component.name}")
        if visual_component.text_font is not None and not isinstance(visual_component.text_font, pygame.font.Font):
            raise ValueError(f"Text font must be a pygame.font.Font. - {visual_component.name}")
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
