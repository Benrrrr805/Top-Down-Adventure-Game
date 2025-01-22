import pytest
import json
from game.core.game_component import GameComponent

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
    assert game_component.event_queue is None
    assert game_component.active is False
    assert game_component.game_values_set is False
    assert game_component.helper_functions == {}
    assert game_component.debug is False

def test_to_dict(game_component: GameComponent):
    game_component.debug = True
    d = game_component.to_dict()
    assert d["name"] == "TestComponent"
    assert d["top_level"] is True
    assert d["active"] is False
    assert d["debug"] is True
    assert d["children"] == []
    assert d["parent"] is None
    assert d["event_queue"] is None
    assert d["game_values_set"] is False
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