from game.core.visual_component import VisualComponent
from game.core.validation.visual_component_validation import VisualComponentValidation
import pytest

@pytest.fixture
def vc_base() -> VisualComponent:
    """
    Returns a base VisualComponent with simple parameters.
    """
    vc = VisualComponent(
        name="TestVC",
        top_level=True,
        width=100,
        height=50,
        x_coordinate=10,
        y_coordinate=20,
        background_color=(0, 0, 0),
        text="Hello",
        text_size=24,
        text_color=(0, 0, 0),
        text_position=(100 // 2, 50 // 2)
    )
    return vc

def test_validate_is_visual_component(vc_base):
    """Check that validate_is_visual_component passes for a real VisualComponent."""
    assert VisualComponentValidation.validate_is_visual_component(vc_base)

def test_validate_is_visual_component_failure():
    """Check that validate_is_visual_component raises ValueError for non-VisualComponent."""
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_is_visual_component(object())

def test_validate_rect(vc_base):
    """Check validate_rect with a valid pygame.Rect."""
    assert VisualComponentValidation.validate_rect(vc_base)

def test_validate_rect_failure(vc_base):
    """Check validate_rect raises ValueError if rect isn't a pygame.Rect (or is invalid)."""
    vc_base.rect = "not_a_rect"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_rect(vc_base)

def test_validate_surface(vc_base):
    """Check validate_surface with a valid pygame.Surface."""
    assert VisualComponentValidation.validate_surface(vc_base)

def test_validate_surface_failure(vc_base):
    """Check validate_surface raises ValueError if surface isn't a pygame.Surface."""
    vc_base.surface = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_surface(vc_base)

def test_validate_image_url(vc_base):
    """Check validate_image_url with a real file path."""
    assert VisualComponentValidation.validate_image_url(vc_base) is False

def test_validate_image_url_success(vc_base):
    """Check validate_image_url with a real file path."""
    vc_base.image_url = "assets/test_image.png"
    assert VisualComponentValidation.validate_image_url(vc_base)

def test_validate_image_url_failure_not_string(vc_base):
    """Check validate_image_url raises ValueError if image_url isn't a string."""
    vc_base.image_url = 123  # Not a string
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_image_url(vc_base)

def test_validate_image_url_failure_missing_file(vc_base):
    """Check validate_image_url raises ValueError if file doesn't exist."""
    vc_base.image_url = "non_existent_file.png"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_image_url(vc_base)

def test_validate_image_url_failure_no_image_url(vc_base):
    """Check validate_image_url raises ValueError if image_url is None."""
    vc_base.image_url = None
    assert VisualComponentValidation.validate_image_url(vc_base) is False

def test_validate_background_color(vc_base):
    """Check validate_background_color with a valid tuple."""
    assert VisualComponentValidation.validate_background_color(vc_base)

def test_validate_background_color_failure_type(vc_base):
    """Check validate_background_color raises if background_color is not tuple."""
    vc_base.background_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_background_color(vc_base)

def test_validate_background_color_failure_length(vc_base):
    """Check validate_background_color raises if tuple is not RGB or RGBA length."""
    vc_base.background_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_background_color(vc_base)

def test_validate_background_color_failure_no_background_color(vc_base):
    """Check validate_background_color raises if background_color is None."""
    vc_base.background_color = None
    assert VisualComponentValidation.validate_background_color(vc_base) is False

def test_validate_background_image(vc_base):
    """Check validate_background_image with a pygame.Surface."""
    assert VisualComponentValidation.validate_background_image(vc_base) is False

def test_validate_background_image_success():
    """Check validate_background_image with a pygame.Surface."""
    vc = VisualComponent(
        name="TestVC",
        top_level=True,
        width=100,
        height=50,
        x_coordinate=10,
        y_coordinate=20,
        text="Hello",
        text_size=24,
        text_color=(0, 0, 0),
        text_position=(100 // 2, 50 // 2),
        image_url="assets/test_image.png"
    )
    assert VisualComponentValidation.validate_background_image(vc)
def test_validate_background_image_failure(vc_base):
    """Check validate_background_image raises if background_image is not a pygame.Surface."""
    vc_base.background_image = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_background_image(vc_base)

def test_validate_background_image_failure_no_background_image(vc_base):
    """Check validate_background_image raises if background_image is None."""
    vc_base.background_image = None
    assert VisualComponentValidation.validate_background_image(vc_base) is False

def test_validate_width(vc_base):
    """Check validate_width with an integer."""
    assert VisualComponentValidation.validate_width(vc_base)

def test_validate_width_failure(vc_base):
    """Check validate_width raises ValueError if width is not int or is None."""
    vc_base.width = None
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_width(vc_base)

    vc_base.width = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_width(vc_base)

def test_validate_height(vc_base):
    """Check validate_height with an integer."""
    assert VisualComponentValidation.validate_height(vc_base)

def test_validate_height_failure(vc_base):
    """Check validate_height raises ValueError if height is not int or is None."""
    vc_base.height = None
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_height(vc_base)

    vc_base.height = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_height(vc_base)

def test_validate_x_coordinate(vc_base):
    """Check validate_x_coordinate with an integer."""
    assert VisualComponentValidation.validate_x_coordinate(vc_base)

def test_validate_x_coordinate_failure(vc_base):
    """Check validate_x_coordinate raises if x_coordinate is None or not int."""
    vc_base.x_coordinate = None
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_x_coordinate(vc_base)
    vc_base.x_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_x_coordinate(vc_base)

def test_validate_y_coordinate(vc_base):
    """Check validate_y_coordinate with an integer."""
    assert VisualComponentValidation.validate_y_coordinate(vc_base)

def test_validate_y_coordinate_failure(vc_base):
    """Check validate_y_coordinate raises if y_coordinate is None or not int."""
    vc_base.y_coordinate = None
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_y_coordinate(vc_base)
    vc_base.y_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_y_coordinate(vc_base)

def test_validate_text(vc_base):
    """Check validate_text with a valid string."""
    assert VisualComponentValidation.validate_text(vc_base)

def test_validate_text_failure(vc_base):
    """Check validate_text raises ValueError if text is not None and not string."""
    vc_base.text = 123
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text(vc_base)

def test_validate_text_font(vc_base):
    """Check validate_text_font with a valid pygame.font.Font."""
    assert VisualComponentValidation.validate_text_font(vc_base)

def test_validate_text_font_failure(vc_base):
    """Check validate_text_font raises ValueError if text_font is not a pygame.font.Font."""
    vc_base.text_font = "not_a_font"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_font(vc_base)

def test_validate_text_size(vc_base):
    """Check validate_text_size with a valid integer."""
    assert VisualComponentValidation.validate_text_size(vc_base)

def test_validate_text_size_failure(vc_base):
    """Check validate_text_size raises ValueError if text_size is not None and not int."""
    vc_base.text_size = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_size(vc_base)

def test_validate_text_color(vc_base):
    """Check validate_text_color with a valid tuple."""
    assert VisualComponentValidation.validate_text_color(vc_base)

def test_validate_text_color_failure_type(vc_base):
    """Check validate_text_color raises if text_color is not tuple."""
    vc_base.text_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_color(vc_base)

def test_validate_text_color_failure_length(vc_base):
    """Check validate_text_color raises if tuple is not length 3 or 4."""
    vc_base.text_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_color(vc_base)

def test_validate_text_color_failure_no_text_color(vc_base):
    """Check validate_text_color raises if text_color is None."""
    vc_base.text_color = None
    assert VisualComponentValidation.validate_text_color(vc_base) is False

def test_validate_text_position(vc_base):
    """Check validate_text_position with a valid tuple (x, y)."""
    assert VisualComponentValidation.validate_text_position(vc_base)

def test_validate_text_position_failure(vc_base):
    """Check validate_text_position raises ValueError if not a 2-element tuple."""
    vc_base.text_position = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_position(vc_base)

    vc_base.text_position = (0, 0, 0)  # too many elements
    with pytest.raises(ValueError):
        VisualComponentValidation.validate_text_position(vc_base)

def test_validate_text_position_failure_no_text_position(vc_base):
    """Check validate_text_position raises ValueError if text_position is None."""
    vc_base.text_position = None
    assert VisualComponentValidation.validate_text_position(vc_base) is False

def test_validate_base_values(vc_base):
    """Check validate_base_values passes with a fully valid VisualComponent."""
    assert VisualComponentValidation.validate_base_values(vc_base)

def test_full_validate(vc_base):
    """Check full_validate passes with a fully valid VisualComponent."""
    assert VisualComponentValidation.full_validate(vc_base)
