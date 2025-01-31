from game.core.game_component import GameComponent
from game.core.validation.game_component_validation import GameComponentValidation
from game.core.event_queue import EventQueue
import pygame
import pytest


@pytest.fixture
def valid_game_component():
    """
    Creates and returns a GameComponent instance with all attributes
    set to valid values, suitable for passing all validators.
    Adjust as needed if your GameComponent has a specific constructor.
    """
    gc = GameComponent("TestComponent", False)
    gc.event_queue = EventQueue(pygame, True)

    # Helper functions
    gc.helper_functions = {
        "example_function": lambda x: x
    }

    gc.active = True
    gc.need_to_update = False

    return gc

def test_validate_is_game_component(valid_game_component: GameComponent):
    """Test that validate_is_game_component succeeds with a real GameComponent."""
    assert GameComponentValidation.validate_is_game_component(valid_game_component)

def test_validate_is_game_component_failure():
    """Test that validate_is_game_component raises ValueError if not a GameComponent."""
    not_a_game_component = object()  # or any other non-GameComponent instance
    with pytest.raises(ValueError):
        GameComponentValidation.validate_is_game_component(not_a_game_component)

def test_validate_base_values(valid_game_component: GameComponent):
    """Test validate_base_values with all valid data."""
    assert GameComponentValidation.validate_base_values(valid_game_component)

def test_validate_pygame(valid_game_component: GameComponent):
    """Test validate_pygame with valid attributes."""
    assert GameComponentValidation.validate_pygame(valid_game_component)

def test_validate_pygame_failure(valid_game_component: GameComponent):
    """Test validate_pygame raises ValueError when pygame is None or incorrect."""
    valid_game_component.pygame = None
    with pytest.raises(ValueError):
        GameComponentValidation.validate_pygame(valid_game_component)

def test_validate_screen(valid_game_component: GameComponent):
    """Test validate_screen with valid attributes."""
    assert GameComponentValidation.validate_screen(valid_game_component)

def test_validate_screen_failure(valid_game_component: GameComponent):
    """Test validate_screen raises ValueError when the screen is invalid."""
    valid_game_component.screen = None
    with pytest.raises(ValueError):
        GameComponentValidation.validate_screen(valid_game_component)

def test_validate_display(valid_game_component: GameComponent):
    """Test validate_display with valid attributes."""
    assert GameComponentValidation.validate_display(valid_game_component)

def test_validate_display_failure(valid_game_component: GameComponent):
    """Test validate_display raises ValueError when display is invalid."""
    valid_game_component.display = None
    with pytest.raises(ValueError):
        GameComponentValidation.validate_display(valid_game_component)

def test_validate_event_queue(valid_game_component: GameComponent):
    """Test validate_event_queue with valid attributes."""
    assert GameComponentValidation.validate_event_queue(valid_game_component)

def test_validate_event_queue_failure(valid_game_component: GameComponent):
    """Test validate_event_queue raises ValueError when event_queue is invalid."""
    valid_game_component.event_queue = None
    with pytest.raises(ValueError):
        GameComponentValidation.validate_event_queue(valid_game_component)

def test_validate_helper_functions(valid_game_component: GameComponent):
    """Test validate_helper_functions with valid data."""
    assert GameComponentValidation.validate_helper_functions(valid_game_component)

def test_validate_helper_functions_failure(valid_game_component: GameComponent):
    valid_game_component.helper_functions = {"not_callable": 123}
    with pytest.raises(ValueError):
        GameComponentValidation.validate_helper_functions(valid_game_component)
    valid_game_component.helper_functions = "Not a dict"
    with pytest.raises(ValueError):
        GameComponentValidation.validate_helper_functions(valid_game_component)

def test_validate_debug_color(valid_game_component: GameComponent):
    """Test validate_debug_color with valid data."""
    assert GameComponentValidation.validate_debug_color(valid_game_component)

def test_validate_debug_color_failure(valid_game_component: GameComponent):
    valid_game_component.debug_color = (0, 0)  # Invalid length
    with pytest.raises(ValueError):
        GameComponentValidation.validate_debug_color(valid_game_component)

def test_validate_active(valid_game_component: GameComponent):
    """Test validate_active with valid data."""
    assert GameComponentValidation.validate_active(valid_game_component)

def test_validate_active_failure(valid_game_component: GameComponent):
    valid_game_component.active = "Not a bool"
    with pytest.raises(ValueError):
        GameComponentValidation.validate_active(valid_game_component)

def test_validate_debug(valid_game_component: GameComponent):
    """Test validate_debug with valid data."""
    assert GameComponentValidation.validate_debug(valid_game_component)

def test_validate_debug_failure(valid_game_component: GameComponent):
    valid_game_component.debug = "Not a bool"
    with pytest.raises(ValueError):
        GameComponentValidation.validate_debug(valid_game_component)

def test_validate_need_to_update(valid_game_component: GameComponent):
    """Test validate_need_to_update with valid data."""
    assert GameComponentValidation.validate_need_to_update(valid_game_component)

def test_validate_need_to_update_failure(valid_game_component: GameComponent):
    valid_game_component.need_to_update = "Not a bool"
    with pytest.raises(ValueError):
        GameComponentValidation.validate_need_to_update(valid_game_component)

def test_full_validate(valid_game_component: GameComponent):
    """Test the full_validate method with a valid GameComponent."""
    assert GameComponentValidation.full_validate(valid_game_component)

def test_validate_is_enabled(valid_game_component: GameComponent):
    """Test validate_is_enabled when component is active."""
    assert GameComponentValidation.validate_is_enabled(valid_game_component)

def test_validate_is_enabled_failure(valid_game_component: GameComponent):
    """Test validate_is_enabled raises when component is inactive."""
    valid_game_component.active = False
    with pytest.raises(ValueError):
        GameComponentValidation.validate_is_enabled(valid_game_component)

def test_validate_is_disabled(valid_game_component: GameComponent):
    with pytest.raises(ValueError):
        GameComponentValidation.validate_is_disabled(valid_game_component)

def test_validate_is_disabled_pass(valid_game_component: GameComponent):
    valid_game_component.active = False
    GameComponentValidation.validate_is_disabled(valid_game_component)
