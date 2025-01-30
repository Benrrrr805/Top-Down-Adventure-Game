import pytest
import json
import pygame
from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent


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
    gc = GameComponent("TestComponent", False)
    gc.event_queue = EventQueue(pygame, True)

    # Helper functions
    gc.helper_functions = {
        "example_function": lambda x: x
    }

    gc.active = True
    gc.need_to_update = False

    return gc

@pytest.fixture
def game_component() -> GameComponent:
    return GameComponent(name="TestComponent", top_level=True)

def dummy_helper_function(component, context, from_helper):
    return True

def test_initialization(game_component: GameComponent):
    assert game_component.name == "TestComponent"
    assert game_component.top_level is True
    assert game_component.children == []
    assert game_component.parent is None
    assert game_component.active is False
    assert game_component.helper_functions == {}
    assert game_component.debug is True

def test_to_dict(game_component: GameComponent):
    d = game_component.to_dict()
    assert d["name"] == "TestComponent"
    assert d["top_level"] is True
    assert d["active"] is False
    assert d["children"] == []
    assert d["parent"] is None
    assert d["event_queue"] is None
    assert d["helper_functions"] == {}

def test_str(game_component: GameComponent):
    d = game_component.to_dict()
    s = game_component.__str__()
    assert s == json.dumps(d, indent=4)

def test_dummy_helper_function():
    assert dummy_helper_function(None, None, None) is True

def test_add_helper_function(game_component: GameComponent):
    game_component.add_helper_function("dummy", dummy_helper_function)
    assert "dummy" in game_component.helper_functions
    assert callable(game_component.helper_functions["dummy"]["func"])
    assert game_component.helper_functions["dummy"]["enabled"] is True
    assert game_component.helper_functions["dummy"]["contexts"] is None

    with pytest.raises(ValueError, match="Helper function must be callable. - dummy2"):
        game_component.add_helper_function("dummy2", "not a function")

def test_enable_disable_helper_function(game_component: GameComponent):
    game_component.add_helper_function("dummy", dummy_helper_function)
    game_component.disable_helper_function("dummy")
    assert game_component.helper_functions["dummy"]["enabled"] is False
    game_component.enable_helper_function("dummy")
    assert game_component.helper_functions["dummy"]["enabled"] is True

    with pytest.raises(ValueError, match="No helper function named 'dummy2'."):
        game_component.enable_helper_function("dummy2")

    with pytest.raises(ValueError, match="No helper function named 'dummy2'."):
        game_component.disable_helper_function("dummy2")

def test_set_and_get_helper_function_contexts(game_component: GameComponent):
    game_component.add_helper_function("dummy", dummy_helper_function)
    game_component.set_helper_function_contexts("dummy", ["update", "handle_events"])
    contexts = game_component.get_helper_function_contexts("dummy")
    assert contexts == ["update", "handle_events"]

    with pytest.raises(ValueError, match="No helper function named 'dummy2'."):
        game_component.set_helper_function_contexts("dummy2", ["update", "handle_events"])

    with pytest.raises(ValueError, match="No helper function named 'dummy2'."):
        game_component.get_helper_function_contexts("dummy2")

def test_get_helper_function(game_component: GameComponent):
    game_component.add_helper_function("dummy", dummy_helper_function)
    func = game_component.get_helper_function("dummy")
    assert callable(func)

    with pytest.raises(ValueError, match="No helper function named 'dummy2'."):
        game_component.get_helper_function("dummy2")

def test_call_helper_function(game_component: GameComponent, capsys: pytest.CaptureFixture):
    def print_context(component, context, from_helper):
        print(f"Context: {context}")

    game_component.add_helper_function("print_context", print_context, ["manual"])
    game_component.call_helper_function("print_context", context="manual")
    captured = capsys.readouterr()
    assert "Context: manual" in captured.out

    with pytest.raises(ValueError, match="No helper function named 'dummy'."):
        game_component.call_helper_function("dummy")

    game_component.disable_helper_function("print_context")
    game_component.call_helper_function("print_context", context="manual")
    captured = capsys.readouterr()
    assert "Helper function 'print_context' is disabled. Not calling." in captured.out

    game_component.enable_helper_function("print_context")
    game_component.set_helper_function_contexts("print_context", ["update"])
    game_component.call_helper_function("print_context", context="manual")
    captured = capsys.readouterr()
    assert "Helper function 'print_context' does not handle context 'manual'. Not calling." in captured.out

def test_run_helper_functions(game_component: GameComponent, capsys: pytest.CaptureFixture):
    def print_context(component, context, from_helper):
        print(f"Context: {context}")

    game_component.add_helper_function("print_context", print_context, ["update"])
    game_component.run_helper_functions("update")
    captured = capsys.readouterr()
    assert "Context: update" in captured.out

def test_enable_and_disable(game_component: GameComponent):
    game_component.enable()
    assert game_component.active is True
    assert game_component.need_to_update is True

    game_component.disable()
    assert game_component.active is False
    assert game_component.need_to_update is False

def test_update(game_component: GameComponent):
    game_component.enable()

    child: GameComponent = GameComponent(name="ChildComponent", top_level=False, parent=game_component)
    child.enable()
    game_component.children.append(child)

    game_component.update()
    assert game_component.need_to_update is True

def test_handle_events(game_component: GameComponent):
    game_component.enable()

    child: GameComponent = GameComponent(name="ChildComponent", top_level=False, parent=game_component)
    child.enable()
    game_component.children.append(child)

    game_component.handle_events()
    # No exceptions should be raised for a valid hierarchy

def test_disable_while_handling_events(game_component: GameComponent):
    game_component.enable()
    game_component.disable()
    with pytest.raises(ValueError, match="GameComponent must be enabled before handling events"):
        game_component.handle_events()

def test_disable_while_updating(game_component: GameComponent):
    game_component.enable()
    game_component.disable()
    with pytest.raises(ValueError, match="GameComponent must be enabled before updating"):
        game_component.update()

def test_enable_children(game_component: GameComponent):
    game_component.enable()

    child = GameComponent(name="ChildComponent", top_level=False, parent=game_component)
    game_component.children.append(child)
    game_component.enable_children()
    assert child.active is True

def test_disable_children(game_component: GameComponent):
    game_component.enable()

    child = GameComponent(name="ChildComponent", top_level=False, parent=game_component)
    game_component.children.append(child)
    game_component.disable_children()
    assert child.active is False

def test_link_child(game_component: GameComponent):
    child = GameComponent(name="ChildComponent", top_level=False, parent=game_component)
    game_component.link_child(child)
    assert child.parent == game_component

def test_link_children(game_component: GameComponent):
    child1 = GameComponent(name="ChildComponent1", top_level=False, parent=game_component)
    child2 = GameComponent(name="ChildComponent2", top_level=False, parent=game_component)
    game_component.link_children([child1, child2])
    assert child1.parent == game_component
    assert child2.parent == game_component

def test_validate_is_game_component(valid_game_component: GameComponent):
    """Test that validate_is_game_component succeeds with a real GameComponent."""
    assert GameComponent.validate_is_game_component(valid_game_component)

def test_validate_is_game_component_failure():
    """Test that validate_is_game_component raises ValueError if not a GameComponent."""
    not_a_game_component = object()  # or any other non-GameComponent instance
    with pytest.raises(ValueError):
        GameComponent.validate_is_game_component(not_a_game_component)

def test_validate_base_values(valid_game_component: GameComponent):
    """Test validate_base_values with all valid data."""
    assert GameComponent.validate_base_values(valid_game_component)

def test_validate_pygame(valid_game_component: GameComponent):
    """Test validate_pygame with valid attributes."""
    assert GameComponent.validate_pygame(valid_game_component)

def test_validate_pygame_failure(valid_game_component: GameComponent):
    """Test validate_pygame raises ValueError when pygame is None or incorrect."""
    valid_game_component.pygame = None
    with pytest.raises(ValueError):
        GameComponent.validate_pygame(valid_game_component)

def test_validate_screen(valid_game_component: GameComponent):
    """Test validate_screen with valid attributes."""
    assert GameComponent.validate_screen(valid_game_component)

def test_validate_screen_failure(valid_game_component: GameComponent):
    """Test validate_screen raises ValueError when the screen is invalid."""
    valid_game_component.screen = None
    with pytest.raises(ValueError):
        GameComponent.validate_screen(valid_game_component)

def test_validate_display(valid_game_component: GameComponent):
    """Test validate_display with valid attributes."""
    assert GameComponent.validate_display(valid_game_component)

def test_validate_display_failure(valid_game_component: GameComponent):
    """Test validate_display raises ValueError when display is invalid."""
    valid_game_component.display = None
    with pytest.raises(ValueError):
        GameComponent.validate_display(valid_game_component)

def test_validate_event_queue(valid_game_component: GameComponent):
    """Test validate_event_queue with valid attributes."""
    assert GameComponent.validate_event_queue(valid_game_component)

def test_validate_event_queue_failure(valid_game_component: GameComponent):
    """Test validate_event_queue raises ValueError when event_queue is invalid."""
    valid_game_component.event_queue = None
    with pytest.raises(ValueError):
        GameComponent.validate_event_queue(valid_game_component)

def test_validate_helper_functions(valid_game_component: GameComponent):
    """Test validate_helper_functions with valid data."""
    assert GameComponent.validate_helper_functions(valid_game_component)

def test_validate_helper_functions_failure(valid_game_component: GameComponent):
    valid_game_component.helper_functions = {"not_callable": 123}
    with pytest.raises(ValueError):
        GameComponent.validate_helper_functions(valid_game_component)
    valid_game_component.helper_functions = "Not a dict"
    with pytest.raises(ValueError):
        GameComponent.validate_helper_functions(valid_game_component)



def test_validate_debug_color(valid_game_component: GameComponent):
    """Test validate_debug_color with valid data."""
    assert GameComponent.validate_debug_color(valid_game_component)

def test_validate_debug_color_failure(valid_game_component: GameComponent):
    valid_game_component.debug_color = (0, 0)  # Invalid length
    with pytest.raises(ValueError):
        GameComponent.validate_debug_color(valid_game_component)

def test_validate_active(valid_game_component: GameComponent):
    """Test validate_active with valid data."""
    assert GameComponent.validate_active(valid_game_component)

def test_validate_active_failure(valid_game_component: GameComponent):
    valid_game_component.active = "Not a bool"
    with pytest.raises(ValueError):
        GameComponent.validate_active(valid_game_component)

def test_validate_debug(valid_game_component: GameComponent):
    """Test validate_debug with valid data."""
    assert GameComponent.validate_debug(valid_game_component)

def test_validate_debug_failure(valid_game_component: GameComponent):
    valid_game_component.debug = "Not a bool"
    with pytest.raises(ValueError):
        GameComponent.validate_debug(valid_game_component)

def test_validate_need_to_update(valid_game_component: GameComponent):
    """Test validate_need_to_update with valid data."""
    assert GameComponent.validate_need_to_update(valid_game_component)

def test_validate_need_to_update_failure(valid_game_component: GameComponent):
    valid_game_component.need_to_update = "Not a bool"
    with pytest.raises(ValueError):
        GameComponent.validate_need_to_update(valid_game_component)

def test_full_validate(valid_game_component: GameComponent):
    """Test the full_validate method with a valid GameComponent."""
    assert GameComponent.full_validate(valid_game_component)

def test_validate_is_enabled(valid_game_component: GameComponent):
    """Test validate_is_enabled when component is active."""
    assert GameComponent.validate_is_enabled(valid_game_component)

def test_validate_is_enabled_failure(valid_game_component: GameComponent):
    """Test validate_is_enabled raises when component is inactive."""
    valid_game_component.active = False
    with pytest.raises(ValueError):
        GameComponent.validate_is_enabled(valid_game_component)

def test_validate_is_disabled(valid_game_component: GameComponent):
    with pytest.raises(ValueError):
        GameComponent.validate_is_disabled(valid_game_component)

def test_validate_is_disabled_pass(valid_game_component: GameComponent):
    valid_game_component.active = False
    GameComponent.validate_is_disabled(valid_game_component)
