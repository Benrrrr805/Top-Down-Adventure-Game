import pytest
import json
import pygame
from pygame import Rect, Surface
from pygame.font import Font
from game.core.game_loop import Game

# Import your VisualComponent class here:
from game.core.visual_component import VisualComponent
from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.settings import BLACK

# ------------------------------------------------------------------------------
# Pytest Fixtures
# ------------------------------------------------------------------------------


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
        background_color=BLACK,
        text="Hello",
        text_size=24,
        text_color=BLACK,
        text_position=(100 // 2, 50 // 2)
    )
    game_values = Game().game_values
    vc.set_game_values(game_values)
    return vc

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

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

def test_to_dict(vc_base: VisualComponent):
    """
    Test to_dict returns a dictionary with the expected keys and values.
    """
    d = vc_base.to_dict()
    assert d["name"] == "TestVC"
    assert d["top_level"] is True
    assert d["active"] is False
    assert d["children"] == []
    assert d["parent"] is None
    assert d["event_queue"] == EventQueue(pygame, True).to_dict()
    assert d["graphical_values_set"] is False
    assert d["helper_functions"] == {}
    assert d["debug"] is True
    assert d["width"] == 100
    assert d["height"] == 50
    assert d["x_coordinate"] == 10
    assert d["y_coordinate"] == 20
    assert d["background_color"] == BLACK
    assert d["text"] == "Hello"
    assert d["text_size"] == 24
    assert d["text_color"] == BLACK
    assert d["text_position"] == (100 // 2, 50 // 2)

def test_str(vc_base: VisualComponent):
    """
    Test __str__ returns a string representation of the VisualComponent.
    """
    d = vc_base.to_dict()
    s = vc_base.__str__()
    assert s == json.dumps(d, indent=4)

def test_init(vc_base: VisualComponent):
    """
    Test VisualComponent's constructor and default values.
    """
    assert vc_base.name == "TestVC"
    assert vc_base.width == 100
    assert vc_base.height == 50
    assert vc_base.x_coordinate == 10
    assert vc_base.y_coordinate == 20
    assert vc_base.text == "Hello"
    assert vc_base.text_color is BLACK
    assert not vc_base.need_to_update
    assert vc_base.text_position == (100 // 2, 50 // 2)


def test_set_graphical_values(vc_base: VisualComponent):
    """
    Test setting the game values and ensure surfaces, rect, etc. get created
    """
    vc_base.set_graphical_values()
    assert vc_base.graphical_values_set
    assert isinstance(vc_base.text_font, Font)
    assert isinstance(vc_base.rect, Rect)
    assert isinstance(vc_base.surface, Surface)
    assert not vc_base.set_graphical_values()

def test_set_graphical_values_no_game_values(vc_base: VisualComponent):
    """
    Test that an exception is raised if game_values is None.
    """
    vc_base.reset_game_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base.set_graphical_values()
    assert "game values must already be set" in str(exc_info.value)


def test_set_graphical_values_nonexistent_image(vc_base: VisualComponent):
    """
    Test that an exception is raised if the image_url doesn't exist.
    """
    parent_vc: VisualComponent = VisualComponent(name="ParentVC", top_level=True)
    vc_base.parent = parent_vc
    vc_base.image_url = "nonexistent_file.png"

    with pytest.raises(ValueError) as exc_info:
        vc_base.set_graphical_values()
    assert "Background image does not exist" in str(exc_info.value)


def test_set_graphical_values_for_children(vc_base: VisualComponent):
    """
    Test that set_graphical_values_for_children calls set_graphical_values for child VisualComponents.
    """
    child_vc: VisualComponent = VisualComponent(name="ChildVC", top_level=False)
    child_vc.set_game_values(Game().game_values)
    vc_base.children.append(child_vc)

    # Before setting
    assert not child_vc.graphical_values_set

    vc_base.set_graphical_values_for_children()
    assert child_vc.graphical_values_set

def test_in_rect(vc_base: VisualComponent):
    """
    Test in_rect returns if point is outside, True if inside. Throws Error if values not set.
    """
    vc_base.set_graphical_values()
    vc_base.rect = Rect(10, 20, 100, 50)

    assert vc_base.in_rect((10, 20)) is True
    assert vc_base.in_rect((0, 0)) is False

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base.in_rect((0, 0))
    assert "Graphical and game values must be set" in str(exc_info.value)

def test__draw_background(vc_base: VisualComponent):
    """
    Test internal method _draw_background covers the branch of having a background color,
    having a background image, or neither.
    """
    vc_base.active = True
    vc_base.image_url = "assets/test_image.png"
    vc_base.set_graphical_values()

    # 1) background_image is not None
    assert vc_base._draw_background() is True

    # 2) background_image is None
    vc_base.background_image = None
    assert vc_base._draw_background() is True

    # 3) background_image is None and background_color is None
    vc_base.background_color = None
    assert vc_base._draw_background() is True

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base._draw_background()
    assert "Graphical and game values must be set" in str(exc_info.value)

def test__draw_debug_border(vc_base: VisualComponent):
    """
    Test internal method _draw_debug_border is called only if debug is True and color is set.
    """
    vc_base.set_graphical_values()

    vc_base.active = True
    assert vc_base._draw_debug_border() is True

    vc_base.debug = False
    assert vc_base._draw_debug_border() is True

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base._draw_debug_border()
    assert "Graphical and game values must be set" in str(exc_info.value)

def test__draw_children(vc_base: VisualComponent):
    """
    Test that each child that is a VisualComponent has its draw() method called.
    """

    child_vc: VisualComponent = VisualComponent(name="ChildVC", top_level=False, width=10, height=10)
    game_component: VisualComponent = GameComponent(name="TestGC", top_level=False)
    vc_base.link_children([child_vc, game_component])
    vc_base.enable()
    assert vc_base._draw_children() is True

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base._draw_children()
    assert "Graphical and game values must be set" in str(exc_info.value)
    vc_base.set_graphical_values()

    vc_base.reset_game_values_for_children()
    with pytest.raises(ValueError) as exc_info:
        vc_base._draw_children()
    assert "Graphical and game values must be set before drawing children" in str(exc_info.value)

def test_render_text(vc_base: VisualComponent):
    """
    Test rendering text with a given font, text, etc.
    """
    vc_base.active = True
    vc_base.text = "Hello World"
    vc_base.set_graphical_values()

    assert vc_base.render_text() is True

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base.render_text()
    assert "Graphical and game values must be set" in str(exc_info.value)


def test_render_text_no_text(vc_base: VisualComponent):
    """
    Test render_text returns immediately if text is None or empty.
    """
    vc_base.active = True
    vc_base.text = None
    vc_base.set_graphical_values()
    assert vc_base.render_text() is False

def test_render_text_not_active(vc_base: VisualComponent):
    """
    Test render_text raises if the component is not active.
    """
    vc_base.text = "Hello World"
    vc_base.active = False
    vc_base.set_graphical_values()

    with pytest.raises(ValueError) as exc_info:
        vc_base.render_text()
    assert "UIComponent must be enabled" in str(exc_info.value)

def test_draw(vc_base: VisualComponent):
    """
    Test draw() calls draw_() if active, otherwise raises.
    """
    vc_base.active = False
    with pytest.raises(ValueError) as exc_info:
        vc_base.draw()
    assert "Visual Component must be enabled" in str(exc_info.value)
    vc_base.need_to_update = False
    vc_base.active = True
    vc_base.set_graphical_values()
    assert isinstance(vc_base.draw(), Surface)
    vc_base.width = 0
    vc_base.height = 0
    assert vc_base.draw() is False

    vc_base.reset_graphical_values()
    with pytest.raises(ValueError) as exc_info:
        vc_base.draw()
    assert "Graphical and game values must be set" in str(exc_info.value)

def test_get_rect(vc_base: VisualComponent):
    """
    Test get_rect simply returns self.rect.
    """
    vc_base.rect = Rect(10, 20, 30, 40)
    assert vc_base.get_rect() == vc_base.rect

def test_text_font(vc_base: VisualComponent):
    """
    Test that text_font is set to a Font object if it's a string.
    """
    vc_base.text_font = "assets/fonts/ARIAL.TTF"
    vc_base.set_graphical_values()
    assert isinstance(vc_base.text_font, Font)

def test_image_url():
    """
    Test that image_url is loaded and scaled if it's a string.
    """
    component: VisualComponent = VisualComponent(name="TestVC", top_level=True, width=50, height=50, x_coordinate=0, y_coordinate=0, image_url="assets/test_image.png")
    component.set_game_values(Game().game_values)
    component.set_graphical_values()
    assert isinstance(component.background_image, Surface)

def test_reset_graphical_values(vc_base: VisualComponent):
    """
    Test that reset_graphical_values sets graphical_values_set to False and resets the graphical values.
    """
    vc_base.set_graphical_values()
    vc_base.reset_graphical_values()
    assert not vc_base.graphical_values_set
    assert vc_base.text_font is None
    assert vc_base.rect is None
    assert vc_base.surface is None

def test_reset_graphical_values_for_children(vc_base: VisualComponent):
    """
    Test that reset_graphical_values_for_children calls reset_graphical_values for child VisualComponents.
    """
    child_vc: VisualComponent = VisualComponent(name="ChildVC", top_level=False)
    child_vc.set_game_values(Game().game_values)
    vc_base.children.append(child_vc)

    # Before resetting
    assert not child_vc.graphical_values_set

    vc_base.set_graphical_values_for_children()
    vc_base.reset_graphical_values_for_children()
    assert not child_vc.graphical_values_set


def test_validate_is_visual_component(valid_visual_component):
    """Check that validate_is_visual_component passes for a real VisualComponent."""
    assert VisualComponent.validate_is_visual_component(valid_visual_component)

def test_validate_is_visual_component_failure():
    """Check that validate_is_visual_component raises ValueError for non-VisualComponent."""
    with pytest.raises(ValueError):
        VisualComponent.validate_is_visual_component(object())

def test_validate_rect(valid_visual_component):
    """Check validate_rect with a valid pygame.Rect."""
    assert VisualComponent.validate_rect(valid_visual_component)

def test_validate_rect_failure(valid_visual_component):
    """Check validate_rect raises ValueError if rect isn't a pygame.Rect (or is invalid)."""
    valid_visual_component.rect = "not_a_rect"
    with pytest.raises(ValueError):
        VisualComponent.validate_rect(valid_visual_component)

def test_validate_surface(valid_visual_component):
    """Check validate_surface with a valid pygame.Surface."""
    assert VisualComponent.validate_surface(valid_visual_component)

def test_validate_surface_failure(valid_visual_component):
    """Check validate_surface raises ValueError if surface isn't a pygame.Surface."""
    valid_visual_component.surface = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponent.validate_surface(valid_visual_component)

def test_validate_image_url(valid_visual_component):
    """Check validate_image_url with a real file path."""
    assert VisualComponent.validate_image_url(valid_visual_component)

def test_validate_image_url_failure_not_string(valid_visual_component):
    """Check validate_image_url raises ValueError if image_url isn't a string."""
    valid_visual_component.image_url = 123  # Not a string
    with pytest.raises(ValueError):
        VisualComponent.validate_image_url(valid_visual_component)

def test_validate_image_url_failure_missing_file(valid_visual_component):
    """Check validate_image_url raises ValueError if file doesn't exist."""
    valid_visual_component.image_url = "non_existent_file.png"
    with pytest.raises(ValueError):
        VisualComponent.validate_image_url(valid_visual_component)

def test_validate_background_color(valid_visual_component):
    """Check validate_background_color with a valid tuple."""
    assert VisualComponent.validate_background_color(valid_visual_component)

def test_validate_background_color_failure_type(valid_visual_component):
    """Check validate_background_color raises if background_color is not tuple."""
    valid_visual_component.background_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponent.validate_background_color(valid_visual_component)

def test_validate_background_color_failure_length(valid_visual_component):
    """Check validate_background_color raises if tuple is not RGB or RGBA length."""
    valid_visual_component.background_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponent.validate_background_color(valid_visual_component)

def test_validate_background_image(valid_visual_component):
    """Check validate_background_image with a pygame.Surface."""
    assert VisualComponent.validate_background_image(valid_visual_component)

def test_validate_background_image_failure(valid_visual_component):
    """Check validate_background_image raises if background_image is not a pygame.Surface."""
    valid_visual_component.background_image = "not_a_surface"
    with pytest.raises(ValueError):
        VisualComponent.validate_background_image(valid_visual_component)

def test_validate_width(valid_visual_component):
    """Check validate_width with an integer."""
    assert VisualComponent.validate_width(valid_visual_component)

def test_validate_width_failure(valid_visual_component):
    """Check validate_width raises ValueError if width is not int or is None."""
    valid_visual_component.width = None
    with pytest.raises(ValueError):
        VisualComponent.validate_width(valid_visual_component)

    valid_visual_component.width = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponent.validate_width(valid_visual_component)

def test_validate_height(valid_visual_component):
    """Check validate_height with an integer."""
    assert VisualComponent.validate_height(valid_visual_component)

def test_validate_height_failure(valid_visual_component):
    """Check validate_height raises ValueError if height is not int or is None."""
    valid_visual_component.height = None
    with pytest.raises(ValueError):
        VisualComponent.validate_height(valid_visual_component)

    valid_visual_component.height = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponent.validate_height(valid_visual_component)

def test_validate_x_coordinate(valid_visual_component):
    """Check validate_x_coordinate with an integer."""
    assert VisualComponent.validate_x_coordinate(valid_visual_component)

def test_validate_x_coordinate_failure(valid_visual_component):
    """Check validate_x_coordinate raises if x_coordinate is None or not int."""
    valid_visual_component.x_coordinate = None
    with pytest.raises(ValueError):
        VisualComponent.validate_x_coordinate(valid_visual_component)
    valid_visual_component.x_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponent.validate_x_coordinate(valid_visual_component)

def test_validate_y_coordinate(valid_visual_component):
    """Check validate_y_coordinate with an integer."""
    assert VisualComponent.validate_y_coordinate(valid_visual_component)

def test_validate_y_coordinate_failure(valid_visual_component):
    """Check validate_y_coordinate raises if y_coordinate is None or not int."""
    valid_visual_component.y_coordinate = None
    with pytest.raises(ValueError):
        VisualComponent.validate_y_coordinate(valid_visual_component)
    valid_visual_component.y_coordinate = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponent.validate_y_coordinate(valid_visual_component)

def test_validate_text(valid_visual_component):
    """Check validate_text with a valid string."""
    assert VisualComponent.validate_text(valid_visual_component)

def test_validate_text_failure(valid_visual_component):
    """Check validate_text raises ValueError if text is not None and not string."""
    valid_visual_component.text = 123
    with pytest.raises(ValueError):
        VisualComponent.validate_text(valid_visual_component)

def test_validate_text_font(valid_visual_component):
    """Check validate_text_font with a valid pygame.font.Font."""
    assert VisualComponent.validate_text_font(valid_visual_component)

def test_validate_text_font_failure(valid_visual_component):
    """Check validate_text_font raises ValueError if text_font is not a pygame.font.Font."""
    valid_visual_component.text_font = "not_a_font"
    with pytest.raises(ValueError):
        VisualComponent.validate_text_font(valid_visual_component)

def test_validate_text_size(valid_visual_component):
    """Check validate_text_size with a valid integer."""
    assert VisualComponent.validate_text_size(valid_visual_component)

def test_validate_text_size_failure(valid_visual_component):
    """Check validate_text_size raises ValueError if text_size is not None and not int."""
    valid_visual_component.text_size = "not_an_int"
    with pytest.raises(ValueError):
        VisualComponent.validate_text_size(valid_visual_component)

def test_validate_text_color(valid_visual_component):
    """Check validate_text_color with a valid tuple."""
    assert VisualComponent.validate_text_color(valid_visual_component)

def test_validate_text_color_failure_type(valid_visual_component):
    """Check validate_text_color raises if text_color is not tuple."""
    valid_visual_component.text_color = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponent.validate_text_color(valid_visual_component)

def test_validate_text_color_failure_length(valid_visual_component):
    """Check validate_text_color raises if tuple is not length 3 or 4."""
    valid_visual_component.text_color = (255, 255)
    with pytest.raises(ValueError):
        VisualComponent.validate_text_color(valid_visual_component)

def test_validate_text_position(valid_visual_component):
    """Check validate_text_position with a valid tuple (x, y)."""
    assert VisualComponent.validate_text_position(valid_visual_component)

def test_validate_text_position_failure(valid_visual_component):
    """Check validate_text_position raises ValueError if not a 2-element tuple."""
    valid_visual_component.text_position = "not_a_tuple"
    with pytest.raises(ValueError):
        VisualComponent.validate_text_position(valid_visual_component)

    valid_visual_component.text_position = (0, 0, 0)  # too many elements
    with pytest.raises(ValueError):
        VisualComponent.validate_text_position(valid_visual_component)

def test_validate_graphical_values_set(valid_visual_component):
    """Check validate_graphical_values_set with a boolean."""
    assert VisualComponent.validate_graphical_values_set(valid_visual_component)

def test_validate_graphical_values_set_failure(valid_visual_component):
    """Check validate_graphical_values_set raises ValueError if not boolean."""
    valid_visual_component.graphical_values_set = "not_bool"
    with pytest.raises(ValueError):
        VisualComponent.validate_graphical_values_set(valid_visual_component)

def test_validate_base_values(valid_visual_component):
    """Check validate_base_values passes with a fully valid VisualComponent."""
    assert VisualComponent.validate_base_values(valid_visual_component)

def test_full_validate(valid_visual_component):
    """Check full_validate passes with a fully valid VisualComponent."""
    assert VisualComponent.full_validate(valid_visual_component)
