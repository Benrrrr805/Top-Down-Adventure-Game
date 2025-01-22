import pytest
import json
from pygame import Rect, Surface
from pygame.font import Font
from game.core.game_loop import Game

# Import your VisualComponent class here:
from game.core.visual_component import VisualComponent
from game.core.game_component import GameComponent
from game.settings import BLACK

# ------------------------------------------------------------------------------
# Pytest Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def game_values() -> dict:
    
    game = Game()
    return game.game_values

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
    assert d["event_queue"] is None
    assert d["graphical_values_set"] is False
    assert d["helper_functions"] == {}
    assert d["debug"] is False
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
    assert vc_base.pygame == game_values['pygame']
    assert vc_base.screen == game_values['screen']
    assert vc_base.display == game_values['display']
    assert vc_base.debug_color == game_values['debug_color']
    assert vc_base.debug == game_values['debug']
    assert isinstance(vc_base.text_font, Font)
    assert isinstance(vc_base.rect, Rect)
    assert isinstance(vc_base.surface, Surface)
    assert vc_base.set_graphical_values() is None


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
    vc_base.children.append(child_vc)

    # Before setting
    assert not child_vc.graphical_values_set

    vc_base.set_graphical_values_for_children()
    assert child_vc.graphical_values_set

def test_in_rect(vc_base: VisualComponent):
    """
    Test in_rect returns False if rect is None or if point is outside, True if inside.
    """
    assert vc_base.in_rect((0, 0)) is False

    vc_base.rect = Rect(10, 20, 100, 50)

    assert vc_base.in_rect((10, 20)) is True
    assert vc_base.in_rect((0, 0)) is False

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

def test__draw_debug_border(vc_base: VisualComponent):
    """
    Test internal method _draw_debug_border is called only if debug is True and color is set.
    """
    vc_base.set_graphical_values()

    vc_base.active = True
    assert vc_base._draw_debug_border() is True

    vc_base.debug = False
    assert vc_base._draw_debug_border() is True

# def test__draw_children(vc_base: VisualComponent):
#     """
#     Test that each child that is a VisualComponent has its draw() method called.
#     """

#     child_vc: VisualComponent = VisualComponent(name="ChildVC", top_level=False, width=10, height=10)
#     game_component: VisualComponent = GameComponent(name="TestGC", top_level=False)
#     vc_base.link_children([child_vc, game_component])
#     vc_base.set_graphical_values()
#     vc_base.set_graphical_values_for_children()
#     vc_base.enable()
#     assert vc_base._draw_children() is True

def test_render_text(vc_base: VisualComponent):
    """
    Test rendering text with a given font, text, etc.
    """
    vc_base.active = True
    vc_base.text = "Hello World"
    vc_base.set_graphical_values()

    assert vc_base.render_text() is True

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
    game = Game()
    
    vc_base.text_font = "assets/fonts/ARIAL.TTF"
    vc_base.set_graphical_values()
    print(vc_base.text_font)
    print(game_values)
    assert isinstance(vc_base.text_font, Font)

def test_image_url():
    """
    Test that image_url is loaded and scaled if it's a string.
    """
    component: VisualComponent = VisualComponent(name="TestVC", top_level=True, width=50, height=50, x_coordinate=0, y_coordinate=0, image_url="assets/test_image.png")
    component.set_graphical_values()
    assert isinstance(component.background_image, Surface)
