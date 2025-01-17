import pygame
from pygame.surface import Surface
from pygame.font import Font
from pygame.rect import Rect
from pygame import display
from game.settings import BLACK, RED, BLUE
from game.core.game_component import GameComponent
from typing import Optional
import os


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
        self.need_to_update: bool = False    
        self.pygame: pygame = None
        self.screen: Surface = None
        self.display: display = None
        self.debug_color: tuple[int, int, int] = None
        
        self.width: int = width
        self.height: int = height
        self.x_coordinate: int = x_coordinate
        self.y_coordinate: int = y_coordinate
        self.image_url: str = image_url
        self.background_color: tuple[int, int, int] = background_color

        self.text: str = text
        self.text_font: Font = text_font
        self.text_size: int = text_size
        self.text_color: tuple[int, int, int] = text_color

        self.text_position: tuple[int, int] = (
            text_position if text_position else (width // 2, height // 2)
        )

        self.rect: Rect = None
        self.surface: Surface = None
        self.background_image: Surface = None

    # ----------------------------------------------------------------------
    # UI-Related Utility Functions (wrapped with graphics_enabled checks)
    # ----------------------------------------------------------------------

    def in_rect(self, coordinates: tuple[int, int]) -> bool:
        if self.rect is None:
            return False
        return self.rect.collidepoint(coordinates)

    def hovering(self) -> bool:
        """
        Return True if the mouse is over this component's rect.
        """
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before checking for hover. - {self.name}")
        mouse_pos: tuple[int, int] = self.pygame.mouse.get_pos()
        return self.in_rect(mouse_pos)

    def clicked(self) -> bool:
        """
        Return True if the mouse button is down *within* this component
        and no child component is also hovered.
        """
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before checking for click. - {self.name}")
        if not self.hovering():
            return False

        # If any child is also hovered, consider that the click belongs to the child
        for child in self.children:
            if isinstance(child, VisualComponent) and child.hovering():
                return False

        if self.hovering() and self.event_queue and self.event_queue.has_event('MOUSEBUTTONDOWN'):
            print(f"Clicked on UIComponent: {self.name}")
            self.event_queue.remove_event('MOUSEBUTTONDOWN')
            return True

        return False
    
    # ----------------------------------------------------------------------
    # Rendering Helpers
    # ----------------------------------------------------------------------
    def _draw_background(self) -> None:
        """
        Draws the component's background (image or color).
        """
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
        if self.debug and self.debug_color:
            self.pygame.draw.rect(
                self.surface, self.debug_color, (0, 0, self.width, self.height), 5
            )
        return True

    def _draw_children(self) -> None:
        """
        Draws all child components onto this surface.
        """
        for child in self.children:
            if not isinstance(child, VisualComponent):
                continue
            else:
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

        text_surface: Surface = self.text_font.render(self.text, True, self.text_color)
        text_rect: Rect = text_surface.get_rect()
        text_rect.topleft = self.text_position
        self.surface.blit(text_surface, text_rect)
        return True

    def draw_(self) -> Optional[Surface]:
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
    
    def set_game_values(self, game_values: 'dict') -> None:
        """
        Set references needed to access Pygame or global game resources.
        For UI usage, also create surfaces/rect if graphics_enabled = True.
        """
        if self.pygame_values_set:
            print(f"Game values already set for {self.name}. Skipping.")
            return
        else:
            print(f"Setting game values for {self.name}.")
        self.game_values = game_values
        self.pygame: pygame = game_values['pygame']
        self.screen: Surface = game_values['screen']
        self.display: display = game_values['display']
        self.debug: bool = game_values['debug']
        self.debug_color: tuple[int, int, int] = game_values['debug_color']
        self.game_values = game_values

        if self.parent and isinstance(self.parent, VisualComponent):
            # Offset coordinates by parent's coordinates
            self.x_coordinate: int = self.x_coordinate+self.parent.x_coordinate
            self.y_coordinate: int = self.y_coordinate+self.parent.y_coordinate

        # Create pygame Rect & Surface
        self.rect: Rect = self.pygame.Rect(self.x_coordinate, self.y_coordinate, self.width, self.height)
        self.surface: Surface = self.pygame.Surface((self.width, self.height), self.pygame.SRCALPHA)

        # Load or create the font
        if self.text_font and isinstance(self.text_font, str):
            self.text_font: Font = self.pygame.font.Font(self.text_font, self.text_size)
        else:
            # If None, use default system font
            self.text_font: Font = self.pygame.font.SysFont(None, self.text_size)

        # Attempt to load background image if provided
        if self.image_url is not None:
            if not os.path.exists(self.image_url):
                raise ValueError(f"Background image does not exist: {self.image_url} - {self.name}")
            img: Surface = self.pygame.image.load(self.image_url).convert_alpha()
            self.background_image: Surface = self.pygame.transform.scale(img, (self.width, self.height))

        self.pygame_values_set: bool = True

    def set_game_values_for_children(self, game_values: 'dict') -> None:
        for child in self.children:
            if isinstance(child, VisualComponent):
                child.set_game_values(game_values)
                child.set_game_values_for_children(game_values)

    def reset_game_values(self):
        self.pygame_values_set = False
        self.pygame = None
        self.screen = None
        self.display = None
        self.debug_color = None
        self.rect = None
        self.surface = None
        self.background_image = None
        self.text_font = None

    def reset_game_values_for_children(self):
        for child in self.children:
            if isinstance(child, VisualComponent):
                child.reset_game_values()
                child.reset_game_values_for_children()