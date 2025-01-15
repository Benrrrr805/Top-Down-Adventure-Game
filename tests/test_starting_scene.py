import pytest
from game.scenes.startingScene import StartingScene
from game.entities.uiComponents.containers.main_container import main_container
from game.core.game_loop import Game
from unittest.mock import MagicMock

@pytest.fixture
def mock_game():
    g = Game()
    g.screen = MagicMock()
    g.display = MagicMock()
    g.clock = MagicMock()
    g.text_font = MagicMock()
    g.running = False
    return g

@pytest.fixture
def mock_inactive_scene():
    scene = StartingScene("TestScene", top_level=True)
    scene.link_child(main_container)
    scene.disable()
    return scene

@pytest.fixture
def mock_active_scene():
    scene = StartingScene("TestScene", top_level=True)
    scene.link_child(main_container)
    scene.enable()
    return scene


def test_handle_events_if_not_active(mock_inactive_scene: 'StartingScene'):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.handle_events()
    assert "TestScene is not active." in str(exc.value)

def test_update_if_not_active(mock_inactive_scene: 'StartingScene'):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.update()
    assert "TestScene is not active." in str(exc.value)

def test_draw_if_not_active(mock_inactive_scene: 'StartingScene'):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.draw()
    assert "TestScene is not active." in str(exc.value)

def test_handle_events_if_active(mock_active_scene: 'StartingScene'):
    mock_active_scene.handle_events()

def test_update_if_active(mock_active_scene: 'StartingScene'):
    mock_active_scene.update()

def test_draw_if_active_but_no_game_values(mock_active_scene: 'StartingScene'):
    with pytest.raises(AttributeError) as exc:
        mock_active_scene.draw()
    assert "'NoneType' object has no attribute 'fill'" in str(exc.value)

def test_draw_if_active_with_game_values(mock_active_scene: 'StartingScene', mock_game):
    mock_active_scene.set_game_values(mock_game)
    mock_active_scene.set_game_values_for_children(mock_game)
    mock_active_scene.draw()

def test_set_scene(mock_active_scene: 'StartingScene', mock_game):
    mock_game.pygame = MagicMock()
    mock_active_scene.set_scene(mock_game)
    assert mock_active_scene.game == mock_game
    assert mock_active_scene.main_container == main_container
    assert mock_active_scene.main_menu == main_container.children[0]
    assert mock_active_scene.main_menu.children == main_container.children[0].children