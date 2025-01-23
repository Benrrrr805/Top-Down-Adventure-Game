import os
import pytest
import pygame
import tempfile

from game.core.visual_component import VisualComponent
from game.validation.visual_component_validator import VisualComponentValidator


@pytest.fixture(scope="module", autouse=True)
def pygame_setup_teardown():
    """
    Initializes pygame once per module, and quits after tests to
    clean up resources.
    """
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()

@pytest.fixture
def valid_image_file(tmp_path):
    """
    Creates a placeholder file (named test_image.png) in a temporary directory
    to simulate an existing image file on disk.
    """
    image_file = tmp_path / "test_image.png"
    # Write any data to simulate an image file; it doesn't need to be real image data.
    image_file.write_text("fake_image_data")
    return str(image_file)

@pytest.fixture
def valid_visual_component(valid_image_file):
    """
    Constructs a VisualComponent with valid, initialized attributes
    so that all validators pass.
    """
    vc = VisualComponent("TestVisualComponent", False)

    # For base GameComponent fields inherited (if any),
    # you might need to populate them similarly to your previous tests.
    # e.g. vc.pygame = pygame, vc.screen = pygame.Surface((100, 100)), etc.

    # Specific VisualComponent fields
    vc.rect = pygame.Rect(0, 0, 100, 100)
    vc.surface = pygame.Surface((100, 100))
    vc.image_url = valid_image_file  # Ensure this points to a real path
    vc.background_color = (255, 255, 255, 255)
    vc.background_image = pygame.Surface((50, 50))  # or None if you want to test that path
    vc.width = 100
    vc.height = 200
    vc.x_coordinate = 10
    vc.y_coordinate = 20
    vc.text = "Sample text"
    vc.text_font = pygame.font.Font(None, 24)
    vc.text_size = 24
    vc.text_color = (0, 0, 0, 255)
    vc.text_position = (0, 0)
    vc.graphical_values_set = True

    return vc


def test_validate_is_visual_component(valid_visual_component):
    """Check that validate_is_visual_component passes for a real VisualComponent."""
    assert VisualComponentValidator.validate_is_visual_component(valid_visual_component)

def test_validate_is_visual_component_failure():
    """Check that validate_is_visual_component raises ValueError for non-VisualComponent."""
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_is_visual_component(object())

def test_validate_rect(valid_visual_component):
    """Check validate_rect with a valid pygame.Rect."""
    assert VisualComponentValidator.validate_rect(valid_visual_component)

def test_validate_rect_failure(valid_visual_component):
    """Check validate_rect raises ValueError if rect isn't a pygame.Rect (or is invalid)."""
    valid_visual_component.rect = "not_a_rect"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_rect(valid_visual_component)

def test_validate_surface(valid_visual_component):
    """Check validate_surface with a valid pygame.Surface."""
    assert VisualComponentValidator.validate_surface(valid_visual_component)

def test_validate_surface_failure(valid_visual_component):
    """Check validate_surface raises ValueError if surface isn't a pygame.Surface."""
    valid_visual_component.surface = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_surface(valid_visual_component)

def test_validate_image_url(valid_visual_component):
    """Check validate_image_url with a real file path."""
    assert VisualComponentValidator.validate_image_url(valid_visual_component)

def test_validate_image_url_failure_not_string(valid_visual_component):
    """Check validate_image_url raises ValueError if image_url isn't a string."""
    valid_visual_component.image_url = 123  # Not a string
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_image_url(valid_visual_component)

def test_validate_image_url_failure_missing_file(valid_visual_component):
    """Check validate_image_url raises ValueError if file doesn't exist."""
    valid_visual_component.image_url = "non_existent_file.png"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_image_url(valid_visual_component)

def test_validate_background_color(valid_visual_component):
    """Check validate_background_color with a valid tuple."""
    assert VisualComponentValidator.validate_background_color(valid_visual_component)

def test_validate_background_color_failure_type(valid_visual_component):
    """Check validate_background_color raises if background_color is not tuple."""
    valid_visual_component.background_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_background_color(valid_visual_component)

def test_validate_background_color_failure_length(valid_visual_component):
    """Check validate_background_color raises if tuple is not RGB or RGBA length."""
    valid_visual_component.background_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_background_color(valid_visual_component)

def test_validate_background_image(valid_visual_component):
    """Check validate_background_image with a pygame.Surface."""
    assert VisualComponentValidator.validate_background_image(valid_visual_component)

def test_validate_background_image_failure(valid_visual_component):
    """Check validate_background_image raises if background_image is not a pygame.Surface."""
    valid_visual_component.background_image = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_background_image(valid_visual_component)

def test_validate_width(valid_visual_component):
    """Check validate_width with an integer."""
    assert VisualComponentValidator.validate_width(valid_visual_component)

def test_validate_width_failure(valid_visual_component):
    """Check validate_width raises ValueError if width is not int or is None."""
    valid_visual_component.width = None
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_width(valid_visual_component)

    valid_visual_component.width = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_width(valid_visual_component)

def test_validate_height(valid_visual_component):
    """Check validate_height with an integer."""
    assert VisualComponentValidator.validate_height(valid_visual_component)

def test_validate_height_failure(valid_visual_component):
    """Check validate_height raises ValueError if height is not int or is None."""
    valid_visual_component.height = None
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_height(valid_visual_component)

    valid_visual_component.height = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_height(valid_visual_component)

def test_validate_x_coordinate(valid_visual_component):
    """Check validate_x_coordinate with an integer."""
    assert VisualComponentValidator.validate_x_coordinate(valid_visual_component)

def test_validate_x_coordinate_failure(valid_visual_component):
    """Check validate_x_coordinate raises if x_coordinate is None or not int."""
    valid_visual_component.x_coordinate = None
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_x_coordinate(valid_visual_component)
    valid_visual_component.x_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_x_coordinate(valid_visual_component)

def test_validate_y_coordinate(valid_visual_component):
    """Check validate_y_coordinate with an integer."""
    assert VisualComponentValidator.validate_y_coordinate(valid_visual_component)

def test_validate_y_coordinate_failure(valid_visual_component):
    """Check validate_y_coordinate raises if y_coordinate is None or not int."""
    valid_visual_component.y_coordinate = None
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_y_coordinate(valid_visual_component)
    valid_visual_component.y_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_y_coordinate(valid_visual_component)

def test_validate_text(valid_visual_component):
    """Check validate_text with a valid string."""
    assert VisualComponentValidator.validate_text(valid_visual_component)

def test_validate_text_failure(valid_visual_component):
    """Check validate_text raises ValueError if text is not None and not string."""
    valid_visual_component.text = 123
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text(valid_visual_component)

def test_validate_text_font(valid_visual_component):
    """Check validate_text_font with a valid pygame.font.Font."""
    assert VisualComponentValidator.validate_text_font(valid_visual_component)

def test_validate_text_font_failure(valid_visual_component):
    """Check validate_text_font raises ValueError if text_font is not a pygame.font.Font."""
    valid_visual_component.text_font = "not_a_font"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_font(valid_visual_component)

def test_validate_text_size(valid_visual_component):
    """Check validate_text_size with a valid integer."""
    assert VisualComponentValidator.validate_text_size(valid_visual_component)

def test_validate_text_size_failure(valid_visual_component):
    """Check validate_text_size raises ValueError if text_size is not None and not int."""
    valid_visual_component.text_size = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_size(valid_visual_component)

def test_validate_text_color(valid_visual_component):
    """Check validate_text_color with a valid tuple."""
    assert VisualComponentValidator.validate_text_color(valid_visual_component)

def test_validate_text_color_failure_type(valid_visual_component):
    """Check validate_text_color raises if text_color is not tuple."""
    valid_visual_component.text_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_color(valid_visual_component)

def test_validate_text_color_failure_length(valid_visual_component):
    """Check validate_text_color raises if tuple is not length 3 or 4."""
    valid_visual_component.text_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_color(valid_visual_component)

def test_validate_text_position(valid_visual_component):
    """Check validate_text_position with a valid tuple (x, y)."""
    assert VisualComponentValidator.validate_text_position(valid_visual_component)

def test_validate_text_position_failure(valid_visual_component):
    """Check validate_text_position raises ValueError if not a 2-element tuple."""
    valid_visual_component.text_position = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_position(valid_visual_component)

    valid_visual_component.text_position = (0, 0, 0)  # too many elements
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_text_position(valid_visual_component)

def test_validate_graphical_values_set(valid_visual_component):
    """Check validate_graphical_values_set with a boolean."""
    assert VisualComponentValidator.validate_graphical_values_set(valid_visual_component)

def test_validate_graphical_values_set_failure(valid_visual_component):
    """Check validate_graphical_values_set raises ValueError if not boolean."""
    valid_visual_component.graphical_values_set = "not_bool"
    with pytest.raises(ValueError):
        VisualComponentValidator.validate_graphical_values_set(valid_visual_component)

def test_validate_base_values(valid_visual_component):
    """Check validate_base_values passes with a fully valid VisualComponent."""
    assert VisualComponentValidator.validate_base_values(valid_visual_component)

def test_full_validate(valid_visual_component):
    """Check full_validate passes with a fully valid VisualComponent."""
    assert VisualComponentValidator.full_validate(valid_visual_component)
