import pytest
import pygame

from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.validation.game_component_validator import GameComponentValidator

@pytest.fixture(scope="module", autouse=True)
def pygame_setup_teardown():
    """
    Initializes pygame once per module and quits after tests to
    avoid hanging or leftover pygame resources.
    """
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def valid_game_component():
    """
    Creates and returns a GameComponent instance with all attributes
    set to valid values, suitable for passing all validators.
    Adjust as needed if your GameComponent has a specific constructor.
    """
    gc = GameComponent()
    gc.name = "TestComponent"

    # Core attributes
    gc.pygame = pygame
    gc.screen = pygame.Surface((100, 100))
    gc.display = pygame.display
    gc.event_queue = EventQueue()

    # Helper functions
    gc.helper_functions = {
        "example_function": lambda x: x
    }

    # game_values dictionary
    gc.game_values = {
        'pygame': pygame,
        'screen': pygame.Surface((50, 50)),
        'display': pygame.display,
        'event_queue': EventQueue(),
        'debug': True,
        'debug_color': (255, 255, 255)
    }

    # Various booleans and debug color
    gc.debug_color = (0, 0, 0)
    gc.active = True
    gc.game_values_set = True
    gc.debug = True
    gc.need_to_update = False

    return gc

def test_validate_is_game_component(valid_game_component):
    """Test that validate_is_game_component succeeds with a real GameComponent."""
    assert GameComponentValidator.validate_is_game_component(valid_game_component)

def test_validate_is_game_component_failure():
    """Test that validate_is_game_component raises ValueError if not a GameComponent."""
    not_a_game_component = object()  # or any other non-GameComponent instance
    with pytest.raises(ValueError):
        GameComponentValidator.validate_is_game_component(not_a_game_component)

def test_validate_base_values(valid_game_component):
    """Test validate_base_values with all valid data."""
    assert GameComponentValidator.validate_base_values(valid_game_component)

def test_validate_pygame(valid_game_component):
    """Test validate_pygame with valid attributes."""
    assert GameComponentValidator.validate_pygame(valid_game_component)

def test_validate_pygame_failure(valid_game_component):
    """Test validate_pygame raises ValueError when pygame is None or incorrect."""
    valid_game_component.pygame = None
    with pytest.raises(ValueError):
        GameComponentValidator.validate_pygame(valid_game_component)

def test_validate_screen(valid_game_component):
    """Test validate_screen with valid attributes."""
    assert GameComponentValidator.validate_screen(valid_game_component)

def test_validate_screen_failure(valid_game_component):
    """Test validate_screen raises ValueError when the screen is invalid."""
    valid_game_component.screen = None
    with pytest.raises(ValueError):
        GameComponentValidator.validate_screen(valid_game_component)

def test_validate_display(valid_game_component):
    """Test validate_display with valid attributes."""
    assert GameComponentValidator.validate_display(valid_game_component)

def test_validate_display_failure(valid_game_component):
    """Test validate_display raises ValueError when display is invalid."""
    valid_game_component.display = None
    with pytest.raises(ValueError):
        GameComponentValidator.validate_display(valid_game_component)

def test_validate_event_queue(valid_game_component):
    """Test validate_event_queue with valid attributes."""
    assert GameComponentValidator.validate_event_queue(valid_game_component)

def test_validate_event_queue_failure(valid_game_component):
    """Test validate_event_queue raises ValueError when event_queue is invalid."""
    valid_game_component.event_queue = None
    with pytest.raises(ValueError):
        GameComponentValidator.validate_event_queue(valid_game_component)

def test_validate_helper_functions(valid_game_component):
    """Test validate_helper_functions with valid data."""
    assert GameComponentValidator.validate_helper_functions(valid_game_component)

def test_validate_helper_functions_failure(valid_game_component):
    """Test validate_helper_functions raises ValueError for non-callable items."""
    valid_game_component.helper_functions = {"broken_func": 123}
    with pytest.raises(ValueError):
        GameComponentValidator.validate_helper_functions(valid_game_component)

def test_validate_game_values(valid_game_component):
    """Test validate_game_values with valid data."""
    assert GameComponentValidator.validate_game_values(valid_game_component)

def test_validate_game_values_failure_missing_key(valid_game_component):
    """Test validate_game_values raises ValueError if a required key is missing."""
    del valid_game_component.game_values['debug']  # remove required key
    with pytest.raises(ValueError):
        GameComponentValidator.validate_game_values(valid_game_component)

def test_validate_debug_color(valid_game_component):
    """Test validate_debug_color with valid data."""
    assert GameComponentValidator.validate_debug_color(valid_game_component)

def test_validate_debug_color_failure_length(valid_game_component):
    """Test validate_debug_color raises ValueError for invalid color tuple length."""
    valid_game_component.debug_color = (255, 255)  # invalid length
    with pytest.raises(ValueError):
        GameComponentValidator.validate_debug_color(valid_game_component)

def test_validate_active(valid_game_component):
    """Test validate_active with valid data."""
    assert GameComponentValidator.validate_active(valid_game_component)

def test_validate_active_failure(valid_game_component):
    """Test validate_active raises ValueError when active is not boolean."""
    valid_game_component.active = "not a bool"
    with pytest.raises(ValueError):
        GameComponentValidator.validate_active(valid_game_component)

def test_validate_game_values_set(valid_game_component):
    """Test validate_game_values_set with valid data."""
    assert GameComponentValidator.validate_game_values_set(valid_game_component)

def test_validate_game_values_set_failure(valid_game_component):
    """Test validate_game_values_set raises ValueError when not boolean."""
    valid_game_component.game_values_set = "not a bool"
    with pytest.raises(ValueError):
        GameComponentValidator.validate_game_values_set(valid_game_component)

def test_validate_debug(valid_game_component):
    """Test validate_debug with valid data."""
    assert GameComponentValidator.validate_debug(valid_game_component)

def test_validate_debug_failure(valid_game_component):
    """Test validate_debug raises ValueError when debug is not boolean."""
    valid_game_component.debug = "not a bool"
    with pytest.raises(ValueError):
        GameComponentValidator.validate_debug(valid_game_component)

def test_validate_need_to_update(valid_game_component):
    """Test validate_need_to_update with valid data."""
    assert GameComponentValidator.validate_need_to_update(valid_game_component)

def test_validate_need_to_update_failure(valid_game_component):
    """Test validate_need_to_update raises ValueError when need_to_update is not boolean."""
    valid_game_component.need_to_update = "not a bool"
    with pytest.raises(ValueError):
        GameComponentValidator.validate_need_to_update(valid_game_component)

