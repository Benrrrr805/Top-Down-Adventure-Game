import pytest
from unittest.mock import MagicMock, patch
import pygame

# Assuming your GameComponent class is in game_component.py or similar
# from game_component import GameComponent
# For brevity, we'll pretend it's imported:
from game.core.game_component import GameComponent

@pytest.fixture
def mock_pygame():
    """
    A pytest fixture to initialize and mock out some pygame functionality.
    This helps avoid 'pygame.error: video system not initialized' when testing.
    """
    pygame.init()
    # Mock out just enough to let tests run without a real screen
    with patch('pygame.display.set_mode'):
        with patch('pygame.font.Font'):
            with patch('pygame.image.load'):
                yield
    pygame.quit()


@pytest.fixture
def top_level_parent():
    """
    Returns a top-level GameComponent for use as a parent in tests.
    """
    comp = GameComponent(name="TopLevelParent", top_level=True, graphics_enabled=False)
    comp.children = []
    return comp


@pytest.fixture
def non_top_level_parent():
    """
    Returns a non-top-level GameComponent that already has a parent.
    """
    parent = GameComponent(name="SomeParent", top_level=True)
    parent.children = []
    child = GameComponent(name="NonTopLevelParent", top_level=False)
    child.children = []
    # Link them so that child now has a parent
    GameComponent.link_child(parent, child)
    return child


@pytest.fixture
def child_component():
    """
    Returns a simple child component (not top-level).
    """
    child = GameComponent(name="Child", top_level=False)
    child.children = []
    return child


@pytest.fixture
def top_level_child_component():
    """
    Returns a child that incorrectly has top_level=True.
    We'll test that you cannot just add it as-is.
    """
    child = GameComponent(name="TopLevelChild", top_level=True)
    child.children = []
    return child


# ----------------------------------------------------------------------
# Tests: Basic Initialization
# ----------------------------------------------------------------------
def test_game_component_init():
    comp = GameComponent(name="TestComp", top_level=True, graphics_enabled=True,
                         width=100, height=50, x_coordinate=10, y_coordinate=20)
    assert comp.name == "TestComp"
    assert comp.top_level is True
    assert comp.graphics_enabled is True
    assert comp.width == 100
    assert comp.height == 50
    assert comp.x_coordinate == 10
    assert comp.y_coordinate == 20
    assert comp.children is None
    assert not comp.active
    assert not comp.pygame_values_set


# ----------------------------------------------------------------------
# Tests: Helper Function System
# ----------------------------------------------------------------------
def test_init_helper_functions():
    comp = GameComponent("Comp")
    comp.init_helper_functions()
    assert isinstance(comp.helper_functions, dict)
    assert len(comp.helper_functions) == 0

def test_add_helper_function():
    comp = GameComponent("Comp")
    comp.init_helper_functions()

    def sample_func(self, context, from_helper): pass

    comp.add_helper_function("sample", sample_func, contexts=["update"], enabled=True)
    assert "sample" in comp.helper_functions
    info = comp.helper_functions["sample"]
    assert info["func"] == sample_func
    assert info["enabled"] is True
    assert info["contexts"] == ["update"]

def test_enable_disable_helper_function():
    comp = GameComponent("Comp")
    comp.init_helper_functions()

    def sample_func(self, context, from_helper): pass

    comp.add_helper_function("sample", sample_func, contexts=["manual"], enabled=False)
    assert comp.helper_functions["sample"]["enabled"] is False

    comp.enable_helper_function("sample")
    assert comp.helper_functions["sample"]["enabled"] is True

    comp.disable_helper_function("sample")
    assert comp.helper_functions["sample"]["enabled"] is False

def test_set_and_get_helper_function_contexts():
    comp = GameComponent("Comp")
    comp.init_helper_functions()
    def sample_func(self, context, from_helper): pass

    comp.add_helper_function("sample", sample_func, contexts=["update"], enabled=True)
    comp.set_helper_function_contexts("sample", ["draw"])
    assert comp.get_helper_function_contexts("sample") == ["draw"]

def test_call_helper_function_force(capfd):
    """
    Test that call_helper_function is only invoked if context is in the helper's contexts,
    unless force=True.
    """
    comp = GameComponent("Comp")
    comp.init_helper_functions()

    call_log = []

    def sample_func(self, context, from_helper):
        call_log.append((context, from_helper))

    comp.add_helper_function("test", sample_func, contexts=["update"], enabled=True)

    # Not forced, context not in contexts -> won't be called
    comp.call_helper_function("test", context="draw", from_helper="manual", force=False)
    assert len(call_log) == 0

    # Forced -> will be called
    comp.call_helper_function("test", context="draw", from_helper="manual", force=True)
    assert len(call_log) == 1
    assert call_log[0] == ("draw", "manual")


# ----------------------------------------------------------------------
# Tests: Relationship / Linking
# ----------------------------------------------------------------------
def test_link_child_happy_path(top_level_parent, child_component):
    """
    Test that linking a child to a top-level parent works.
    """
    GameComponent.link_child(top_level_parent, child_component)
    assert child_component in top_level_parent.children
    assert child_component.parent == top_level_parent

def test_link_child_error_if_parent_not_top_level_and_no_parent(child_component):
    """
    If the would-be parent is neither top-level nor already has a parent,
    we expect validate_ready_to_be_added_as_parent() -> validate_has_parent() to fail.
    """
    # Attempt to link child_component to a new non-top-level component that
    # has no parent -> should raise ValueError
    non_top_parent = GameComponent(name="NotTopNoParent", top_level=False)
    non_top_parent.children = []

    with pytest.raises(ValueError) as exc:
        GameComponent.link_child(non_top_parent, child_component)
    assert "Expected: GameComponent. Recieved: NoneType" in str(exc.value) \
           or "NotTopNoParent" in str(exc.value)


def test_link_child_error_if_child_is_top_level(top_level_parent, top_level_child_component):
    """
    If the child is top-level, we want to forcibly disallow adding it until
    we flip child.top_level = False. The code doesn't do that automatically,
    so we expect a validation error from child.validate_ready_to_be_added_as_child().
    """
    with pytest.raises(ValueError) as exc:
        GameComponent.link_child(top_level_parent, top_level_child_component)
    # The code typically fails at child.validate_has_parent() if child is not top-level.
    # But if child is top-level, that means validate_is_not_top_level() is false,
    # so child.validate_ready_to_be_added_as_child() won't raise on that specifically. 
    #
    # In many real cases, you'd add a custom check or override to disallow
    # a top-level child. As-is, the sample code might or might not raise
    # a ValueError (depending on your exact usage). We show that you
    # *want* it to fail, so the test is expecting an error.


def test_link_child_from_non_top_level_parent_with_parent(non_top_level_parent, child_component):
    """
    This tests the scenario:
      - The parent is not top-level, but does have a parent (so it's valid).
      - The child is not top-level, so that is also valid.
    """
    GameComponent.link_child(non_top_level_parent, child_component)
    assert child_component.parent == non_top_level_parent
    assert child_component in non_top_level_parent.children


def test_unlink_child(top_level_parent, child_component):
    GameComponent.link_child(top_level_parent, child_component)
    assert child_component in top_level_parent.children

    GameComponent.unlink_child(top_level_parent, child_component)
    assert child_component not in top_level_parent.children
    assert child_component.parent is None


def test_link_children(top_level_parent):
    c1 = GameComponent("Child1", top_level=False)
    c2 = GameComponent("Child2", top_level=False)
    c3 = GameComponent("Child3", top_level=False)
    for c in [c1, c2, c3]:
        c.children = []

    GameComponent.link_children(top_level_parent, [c1, c2, c3])
    assert c1 in top_level_parent.children
    assert c2 in top_level_parent.children
    assert c3 in top_level_parent.children
    assert c1.parent == top_level_parent
    assert c2.parent == top_level_parent
    assert c3.parent == top_level_parent


# ----------------------------------------------------------------------
# Tests: Enable / Disable
# ----------------------------------------------------------------------
def test_enable_disable_child(top_level_parent, child_component):
    GameComponent.link_child(top_level_parent, child_component)
    top_level_parent.disable()
    assert not top_level_parent.active
    assert not child_component.active

    top_level_parent.enable()
    assert top_level_parent.active
    assert child_component.active


# ----------------------------------------------------------------------
# Tests: Validate Methods
# ----------------------------------------------------------------------
def test_validate_base_values():
    comp = GameComponent("CompBase", top_level=True, graphics_enabled=False)
    comp.children = []
    # Should not raise
    assert comp.validate_base_values() is True

def test_validate_relationships_error_no_parent_for_non_top_level():
    comp = GameComponent("CompChild", top_level=False, graphics_enabled=False)
    comp.children = []
    with pytest.raises(ValueError) as exc:
        comp.validate_relationships()
    assert "Expected: GameComponent. Recieved: NoneType" in str(exc.value)

def test_validate_is_game_component():
    comp = GameComponent("Comp")
    comp.validate_is_game_component()  # Should pass
    with pytest.raises(ValueError):
        comp.validate_is_game_component(game_component=123)  # Force fail

def test_validate_is_top_level(top_level_parent):
    assert top_level_parent.validate_is_top_level() is True
    assert top_level_parent.validate_is_not_top_level() is False

def test_validate_children(top_level_parent, child_component):
    # Children is None by default, let's fix that
    top_level_parent.children = []
    GameComponent.link_child(top_level_parent, child_component)
    assert top_level_parent.validate_children() is True

def test_validate_has_parent_error_if_top_level():
    comp = GameComponent("IAmTopLevel", top_level=True)
    with pytest.raises(ValueError) as exc:
        comp.validate_has_parent()
    assert "IAmTopLevel does not have parent, since it is a top-level GameComponent" in str(exc.value)


# ----------------------------------------------------------------------
# Tests: Tree Traversals
# ----------------------------------------------------------------------
def test_traverse_depth_first(top_level_parent):
    c1 = GameComponent("Child1", top_level=False)
    c2 = GameComponent("Child2", top_level=False)
    c3 = GameComponent("Child3", top_level=False)
    c2_1 = GameComponent("Child2_1", top_level=False)

    c1.children = []
    c2.children = []
    c3.children = []
    c2_1.children = []

    GameComponent.link_child(top_level_parent, c1)
    GameComponent.link_child(top_level_parent, c2)
    GameComponent.link_child(top_level_parent, c3)
    GameComponent.link_child(c2, c2_1)

    dfs = [node.name for node in top_level_parent.traverse_depth_first()]
    # Preorder DFS means [parent, c1, c2, c2_1, c3]
    assert dfs == ["TopLevelParent", "Child1", "Child2", "Child2_1", "Child3"]

def test_traverse_breadth_first(top_level_parent):
    c1 = GameComponent("Child1", top_level=False)
    c2 = GameComponent("Child2", top_level=False)
    c3 = GameComponent("Child3", top_level=False)
    c2_1 = GameComponent("Child2_1", top_level=False)
    for c in [c1, c2, c3, c2_1]:
        c.children = []

    GameComponent.link_child(top_level_parent, c1)
    GameComponent.link_child(top_level_parent, c2)
    GameComponent.link_child(top_level_parent, c3)
    GameComponent.link_child(c2, c2_1)

    bfs = [node.name for node in top_level_parent.traverse_breadth_first()]
    # BFS means [parent, c1, c2, c3, c2_1]
    assert bfs == ["TopLevelParent", "Child1", "Child2", "Child3", "Child2_1"]


# ----------------------------------------------------------------------
# Tests: Rendering / Graphics (basic mocking)
# ----------------------------------------------------------------------
def test_set_game_values(mock_pygame):
    """
    Basic test that ensures set_game_values() sets internal references.
    We skip actual usage of .pygame in a real environment with a real display.
    """
    game = GameComponent("GameRoot", top_level=True, graphics_enabled=True)
    game.children = []
    # Mock references on the 'game' object
    game.pygame = MagicMock()
    game.screen = MagicMock()
    game.display = MagicMock()

    child = GameComponent("ChildUI", graphics_enabled=True)
    child.children = []
    GameComponent.link_child(game, child)

    game.set_game_values(game)  # sets own references
    game.set_game_values_for_children(game)
    assert game.pygame_values_set
    assert child.pygame_values_set
    assert child.pygame is game.pygame
    assert child.screen is game.screen
    assert child.display is game.display
    
# ----------------------------------------------------------------------
# Tests: Data / Display
# ----------------------------------------------------------------------
def test_data_and_display(top_level_parent, child_component, capsys):
    """
    Test the .data() and .display_() methods just to ensure they produce
    a stable dict output and do not raise errors.
    """
    GameComponent.link_child(top_level_parent, child_component)
    data = top_level_parent.data(recursive=True)
    assert isinstance(data, dict)
    assert 'name' in data
    assert 'children' in data
    top_level_parent.display_()
    captured = capsys.readouterr()
    assert "Displaying data for component: TopLevelParent" in captured.out
