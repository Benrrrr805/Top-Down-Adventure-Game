import pytest
import pygame
import os

from game.core.visual_component import VisualComponent
from game.validation.visual_component_validator import VisualComponentValidator


@pytest.fixture
def valid_pygame_env():
    """
    Fixture that sets up a minimal pygame environment.
    Quits pygame after the test completes.
    """
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    display = pygame.display
    yield {
        'pygame': pygame,
        'screen': screen,
        'display': display,
        'debug': False,
        'debug_color': (255, 0, 0),
    }
    pygame.quit()


@pytest.fixture
def valid_visual_component(valid_pygame_env):
    """
    Returns a fully valid VisualComponent, with all attributes set and
    game values loaded. By default, no background_image is given.
    """
    vc = VisualComponent(
        name="test_visual_comp",
        top_level=None,
        width=100,
        height=50,
        x_coordinate=10,
        y_coordinate=20,
        background_color=(255, 255, 255),
        text="Hello",
        text_size=24,
        text_color=(0, 0, 0),
    )
    # Load pygame references
    vc.set_game_values(valid_pygame_env)
    return vc

def test_validate_is_visual_component_with_valid(valid_visual_component):
    """Should pass with a real VisualComponent."""
    assert VisualComponentValidator.validate_is_visual_component(valid_visual_component) is True

def test_validate_is_visual_component_with_invalid():
    """Should raise ValueError if not a VisualComponent."""
    with pytest.raises(ValueError, match="Expected: GameComponent"):
        VisualComponentValidator.validate_is_visual_component("not a VC")

def test_validate_base_values_valid(valid_visual_component):
    """A completely valid VisualComponent should pass and return True."""

    assert VisualComponentValidator.validate_base_values(valid_visual_component) is True

def test_validate_base_values_pygame_values_set_not_bool(valid_visual_component):
    """Raises ValueError if pygame_values_set is not a boolean."""
    valid_visual_component.pygame_values_set = "not bool"
    with pytest.raises(ValueError, match="pygame_values_set must be a boolean"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_missing_width_or_height(valid_visual_component):
    """Raises ValueError if width or height is None."""
    valid_visual_component.width = None
    with pytest.raises(ValueError, match="must have a width and height"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_missing_x_or_y(valid_visual_component):
    """Raises ValueError if x or y is None."""
    valid_visual_component.x_coordinate = None
    with pytest.raises(ValueError, match="must have x and y coordinates"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_debug_color_not_tuple(valid_visual_component):
    """Raises ValueError if debug_color is not a tuple."""
    valid_visual_component.debug_color = "not a tuple"
    with pytest.raises(ValueError, match="Debug color must be a tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_debug_color_wrong_length(valid_visual_component):
    """Raises ValueError if debug_color has length not equal to 3 or 4."""
    valid_visual_component.debug_color = (255,)
    with pytest.raises(ValueError, match="Debug color must be an RGB or RGBA tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_text_not_string(valid_visual_component):
    """Raises ValueError if text is not a string."""
    valid_visual_component.text = 123  # not a string
    with pytest.raises(ValueError, match="Text must be a string"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_text_size_not_int(valid_visual_component):
    """Raises ValueError if text_size is not an integer."""
    valid_visual_component.text_size = "24"
    with pytest.raises(ValueError, match="Text size must be an integer"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_text_position_not_tuple(valid_visual_component):
    """Raises ValueError if text_position is not a tuple or has wrong size."""
    valid_visual_component.text_position = "not a tuple"
    with pytest.raises(ValueError, match="Text position must be a tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

    # Also check if tuple length != 2
    valid_visual_component.text_position = (10, 20, 30)
    with pytest.raises(ValueError, match="Text position must be an \\(x, y\\) tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_text_color_not_tuple(valid_visual_component):
    """Raises ValueError if text_color is not a tuple or has invalid length."""
    valid_visual_component.text_color = "not a tuple"
    with pytest.raises(ValueError, match="Text color must be a tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

    valid_visual_component.text_color = (255,)
    with pytest.raises(ValueError, match="Text color must be an RGB or RGBA tuple"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_pygame_is_none(valid_visual_component):
    """Raises ValueError if visual_component.pygame is None or not the pygame module."""
    valid_visual_component.pygame = None
    with pytest.raises(ValueError, match="VisualComponent must have a pygame instance"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_pygame_not_the_same_module(valid_visual_component):
    """Raises ValueError if visual_component.pygame is not the 'pygame' module object."""
    # We'll just assign an arbitrary object
    valid_visual_component.pygame = object()
    with pytest.raises(ValueError, match="VisualComponent must have a pygame instance"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_screen_is_none(valid_visual_component):
    """Raises ValueError if screen is None or not a pygame.Surface."""
    valid_visual_component.screen = None
    with pytest.raises(ValueError, match="VisualComponent must have a screen"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_screen_not_surface(valid_visual_component):
    """Raises ValueError if screen is not an actual pygame.Surface."""
    valid_visual_component.screen = "not a surface"
    with pytest.raises(ValueError, match="VisualComponent must have a screen"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_display_is_none(valid_visual_component):
    """Raises ValueError if display is None or not pygame.display."""
    valid_visual_component.display = None
    with pytest.raises(ValueError, match="VisualComponent must have a display"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_display_not_pygame_display(valid_visual_component):
    """Raises ValueError if display is not exactly pygame.display."""
    valid_visual_component.display = "not a display"
    with pytest.raises(ValueError, match="VisualComponent must have a display"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_rect_not_pygame_rect(valid_visual_component):
    """Raises ValueError if rect is not a pygame.Rect."""
    valid_visual_component.rect = "not a rect"
    with pytest.raises(ValueError, match="Rect must be a pygame.Rect"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_surface_not_pygame_surface(valid_visual_component):
    """Raises ValueError if surface is not a pygame.Surface."""
    valid_visual_component.surface = "not a surface"
    with pytest.raises(ValueError, match="Surface must be a pygame.Surface"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_background_image_not_surface(valid_visual_component):
    """Raises ValueError if background_image is not a pygame.Surface."""
    # Force the background_image to be something invalid
    valid_visual_component.background_image = "not an image"
    with pytest.raises(ValueError, match="Background image must be a pygame.Surface"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_validate_base_values_text_font_not_pygame_font(valid_visual_component):
    """Raises ValueError if text_font is not a pygame.font.Font."""
    valid_visual_component.text_font = "not a font object"
    with pytest.raises(ValueError, match="Text font must be a pygame.font.Font"):
        VisualComponentValidator.validate_base_values(valid_visual_component)

def test_full_validate_success(valid_visual_component):
    """full_validate should return True when everything is valid."""
    assert VisualComponentValidator.full_validate(valid_visual_component) is True

def test_full_validate_not_visual_component():
    """full_validate should first fail if not an actual VisualComponent."""
    with pytest.raises(ValueError, match="Expected: GameComponent"):
        # Pass an int, for example
        VisualComponentValidator.full_validate(42)

def test_full_validate_fails_base_values(valid_visual_component):
    """full_validate should fail when base values are invalid."""
    valid_visual_component.width = None
    with pytest.raises(ValueError, match="must have a width and height"):
        VisualComponentValidator.full_validate(valid_visual_component)
