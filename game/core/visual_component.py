import pygame
from pygame.surface import Surface
from pygame.font import Font
from pygame.rect import Rect
from pygame import display
from game.settings import BLACK, RED, BLUE
from game.core.game_component import GameComponent
from game.core.node import Node
from typing import Optional
import os
import json


class VisualComponent(GameComponent):
    def __init__(
        self, name, top_level,
        width: int = 0, height: int = 0, x_coordinate: int = 0, y_coordinate: int = 0,
        image_url: str = None, background_color: tuple[int, int, int] = None,
        text: str = None, text_font: Font = None, text_size: int = 24,
        text_color: tuple[int, int, int] = BLACK, text_position: tuple[int, int] = None,
        children=None, parent=None
    ):
        super().__init__(name, top_level, children, parent)
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
        self.graphical_values_set: bool = False

    def __str__(self):
        # Pretty-print the dictionary with 4-space indentation
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        game_component_data = super().to_dict()
        visual_component_data = {
            "rect": type(self.rect).__name__,
            "surface": type(self.surface).__name__,
            "image_url": self.image_url,
            "background_color": self.background_color,
            "background_image": type(self.background_image).__name__,
            "width": self.width,
            "height": self.height,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "text": self.text,
            "text_font": type(self.text_font).__name__,
            "text_size": self.text_size,
            "text_color": self.text_color,
            "text_position": self.text_position,

            "graphical_values_set": self.graphical_values_set
        }
        game_component_data.update(visual_component_data)
        return game_component_data
    # ----------------------------------------------------------------------
    # UI-Related Utility Functions (wrapped with graphics_enabled checks)
    # ----------------------------------------------------------------------

    def in_rect(self, coordinates: tuple[int, int]) -> bool:
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError(f"Graphical and game values must be set before checking for rect. - {self.name}")
        return self.rect.collidepoint(coordinates)
        
    # ----------------------------------------------------------------------
    # Rendering Helpers
    # ----------------------------------------------------------------------
    def _draw_background(self) -> None:
        """
        Draws the component's background (image or color).
        """
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError("Graphical and game values must be set before drawing background.")
        if self.background_image is not None:
            self.surface.blit(self.background_image, (0, 0))
        elif self.background_color is not None:
            self.surface.fill(self.background_color)
        else:
            # Transparent background
            self.surface.fill((0, 0, 0, 0))
        return True

    def _draw_debug_border(self) -> None:
        """
        Draws a debug border if debug mode is active.
        """
        print(f"Debug: {self.debug}, Debug Color: {self.debug_color}")
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError("Graphical and game values must be set before drawing debug border.")
        if self.debug and self.debug_color:
            self.pygame.draw.rect(
                self.surface, self.debug_color, (0, 0, self.width, self.height), 5
            )
        return True

    def _draw_children(self) -> None:
        """
        Draws all child components onto this surface.
        """
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError("Graphical and game values must be set before drawing children.")
        for child in self.children:
            if not isinstance(child, VisualComponent):
                continue
            else:
                if not child.graphical_values_set or not child.game_values_set:
                    raise ValueError(f"Graphical and game values must be set before drawing children. - {child.name}")
                child_surface: Surface = child.draw()
                if child_surface is not None:
                    x: int = child.x_coordinate - self.x_coordinate
                    y: int = child.y_coordinate - self.y_coordinate
                    self.surface.blit(child_surface, (x, y))
                child.need_to_update = False
        return True

    # ----------------------------------------------------------------------
    # Rendering (Only if graphics_enabled)
    # ----------------------------------------------------------------------
    def render_text(self) -> None:
        if not self.text:
            return False
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before rendering text. - {self.name}")
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError(f"Graphical and game values must be set before rendering text. - {self.name}")
        text_surface: Surface = self.text_font.render(self.text, True, self.text_color)
        text_rect: Rect = text_surface.get_rect()
        text_rect.topleft = self.text_position
        self.surface.blit(text_surface, text_rect)
        return True

    def draw_(self) -> Optional[Surface]:
        if not self.graphical_values_set or not self.game_values_set:
            raise ValueError(f"Graphical and game values must be set before drawing. - {self.name}")
        if self.width == 0 or self.height == 0:
            return False

        # If we haven't changed anything, return the existing surface
        if not self.need_to_update:
            return self.surface

        print(f"Drawing UIComponent: {self.name}")

        # Step 1: Draw background
        self._draw_background()

        # Step 2: Render text
        self.render_text()

        # Step 3: Possibly draw debug border
        self._draw_debug_border()

        # Step 4: Run any "draw" helper functions
        self.run_helper_functions("draw")

        # Step 5: Draw children
        self._draw_children()

        self.need_to_update = False

        return self.surface

    def draw(self) -> Surface:
        if not self.active:
            raise ValueError(f"Visual Component must be enabled before drawing. - {self.name}")
        return self.draw_()

    def get_rect(self) -> Optional[Rect]:
        return self.rect
    

# ------------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------------

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
    def validate_graphical_values_set(visual_component: 'VisualComponent') -> bool:
        if not isinstance(visual_component.graphical_values_set, bool):
            raise ValueError(f"GameComponent: {visual_component.name} - Failed validation. pygame_values_set must be a boolean.")
        return True

    @staticmethod
    def validate_base_values(visual_component: 'VisualComponent') -> bool:
        VisualComponent.validate_rect(visual_component)
        VisualComponent.validate_surface(visual_component)
        VisualComponent.validate_image_url(visual_component)
        VisualComponent.validate_background_color(visual_component)
        VisualComponent.validate_background_image(visual_component)
        VisualComponent.validate_width(visual_component)
        VisualComponent.validate_height(visual_component)
        VisualComponent.validate_x_coordinate(visual_component)
        VisualComponent.validate_y_coordinate(visual_component)
        VisualComponent.validate_text(visual_component)
        VisualComponent.validate_text_font(visual_component)
        VisualComponent.validate_text_size(visual_component)
        VisualComponent.validate_text_color(visual_component)
        VisualComponent.validate_text_position(visual_component)
        VisualComponent.validate_graphical_values_set(visual_component)
        return True        
    
    @staticmethod
    def full_validate(visual_component: 'VisualComponent') -> bool:
        VisualComponent.validate_is_visual_component(visual_component)
        VisualComponent.validate_base_values(visual_component)
        return True
    
    @staticmethod
    def validate_is_visual_component(visual_component: 'VisualComponent') -> bool:
        """
        Validates that the given object is a VisualComponent.
        """
        if not isinstance(visual_component, VisualComponent):
            raise ValueError(f'Expected: GameComponent. Recieved: {type(visual_component).__name__}')
        return True
