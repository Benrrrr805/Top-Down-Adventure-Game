import pytest
import pygame
from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.validation.game_component_validator import GameComponentValidator

@pytest.fixture
def valid_game_component():
    """
    Return a valid GameComponent with all attributes set to valid, expected types.
    """
    component = GameComponent(name="test_component", top_level=None)
    component.need_to_update = True
    component.event_queue = EventQueue(pygame, False)
    component.active = True
    component.helper_functions = {}
    component.debug = False
    return component

def test_validate_is_game_component(valid_game_component):
    """
    validate_is_game_component should raise ValueError if the argument is not a GameComponent.
    Otherwise, it should return True.
    """
    # Valid case
    assert GameComponentValidator.validate_is_game_component(valid_game_component) is True

    # Invalid case: pass something that's not GameComponent
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_is_game_component("not_a_component")
    assert "Expected game_component to be GameComponent" in str(exc.value)

def test_validate_base_values__valid(valid_game_component):
    """
    Check that validate_base_values returns True for a valid GameComponent.
    """
    assert GameComponentValidator.validate_base_values(valid_game_component) is True

def test_validate_base_values__need_to_update_not_bool(valid_game_component):
    """
    Check that validate_base_values raises ValueError if need_to_update is not bool.
    """
    valid_game_component.need_to_update = "not_bool"
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_base_values(valid_game_component)
    assert "need_to_update must be a boolean" in str(exc.value)

def test_validate_base_values__active_not_bool(valid_game_component):
    """
    Check that validate_base_values raises ValueError if active is not bool.
    """
    valid_game_component.active = "not_bool"
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_base_values(valid_game_component)
    assert "active must be a boolean" in str(exc.value)

def test_validate_base_values__event_queue_not_eventqueue(valid_game_component):
    """
    Check that validate_base_values raises ValueError if event_queue is not an EventQueue.
    """
    valid_game_component.event_queue = "not_an_event_queue"
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_base_values(valid_game_component)
    assert "event_queue must be an EventQueue" in str(exc.value)

def test_validate_base_values__helper_functions_not_dict(valid_game_component):
    """
    Check that validate_base_values raises ValueError if helper_functions is not a dict.
    """
    valid_game_component.helper_functions = []
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_base_values(valid_game_component)
    assert "helper_functions must be a dictionary" in str(exc.value)

def test_validate_base_values__debug_not_bool(valid_game_component):
    """
    Check that validate_base_values raises ValueError if debug is not bool.
    """
    valid_game_component.debug = "not_bool"
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_base_values(valid_game_component)
    assert "debug must be a boolean" in str(exc.value)

def test_validate_is_enabled(valid_game_component):
    """
    validate_is_enabled should raise a ValueError if active is False.
    """
    # Component is currently active=True in the fixture
    assert GameComponentValidator.validate_is_enabled(valid_game_component) is True

    valid_game_component.active = False
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_is_enabled(valid_game_component)
    assert "GameComponent must be enabled" in str(exc.value)

def test_validate_is_disabled(valid_game_component):
    """
    validate_is_disabled should raise a ValueError if active is True.
    """
    # Set it to inactive for valid scenario
    valid_game_component.active = False
    assert GameComponentValidator.validate_is_disabled(valid_game_component) is True

    # Now set it to True and check for ValueError
    valid_game_component.active = True
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.validate_is_disabled(valid_game_component)
    assert "GameComponent must be disabled" in str(exc.value)

def test_full_validate__valid(valid_game_component):
    """
    full_validate should return True when given a valid GameComponent.
    """
    assert GameComponentValidator.full_validate(valid_game_component) is True

def test_full_validate__not_game_component():
    """
    full_validate should raise ValueError if the object is not a GameComponent.
    """
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.full_validate("not_a_component")
    assert "Expected game_component to be GameComponent" in str(exc.value)

def test_full_validate__invalid_attributes(valid_game_component):
    """
    If the attributes are invalid, the call to base_values validation will fail.
    """
    valid_game_component.event_queue = "invalid_type"
    with pytest.raises(ValueError) as exc:
        GameComponentValidator.full_validate(valid_game_component)
    assert "event_queue must be an EventQueue" in str(exc.value)
