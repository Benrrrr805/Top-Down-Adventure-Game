import pytest
from game.scenes.startingScene import StartingScene
from game.entities.uiComponents.containers.main_container import main_container
from game.core.game_loop import Game
from unittest.mock import MagicMock

@pytest.fixture
def game_values():
    g = Game()
    game_values = g.game_values
    return game_values

@pytest.fixture
def game():
    g = Game()
    return g

@pytest.fixture
def mock_scene():
    scene = StartingScene("TestScene", top_level=True)
    return scene



def test_handle_events_if_not_active(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.disable()
    with pytest.raises(ValueError) as exc:
        mock_scene.handle_events()
    assert "TestScene is not active." in str(exc.value)

def test_update_if_not_active(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.disable()
    with pytest.raises(ValueError) as exc:
        mock_scene.update()
    assert "TestScene is not active." in str(exc.value)

def test_draw_if_not_active(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.disable()
    with pytest.raises(ValueError) as exc:
        mock_scene.draw()
    assert "TestScene is not active." in str(exc.value)

def test_handle_events_if_active(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.enable()
    mock_scene.handle_events()

def test_update_if_active(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.enable()
    mock_scene.update()

def test_draw_if_active_but_no_game_values(mock_scene: 'StartingScene'):
    mock_scene.link_child(main_container)
    mock_scene.enable()
    with pytest.raises(AttributeError) as exc:
        mock_scene.draw()
    assert "'NoneType' object has no attribute 'fill'" in str(exc.value)

def test_draw_if_active_with_game_values(mock_scene: 'StartingScene', game_values):
    mock_scene.link_child(main_container)
    mock_scene.enable()
    mock_scene.set_game_values(game_values)
    mock_scene.set_game_values_for_children(game_values)
    mock_scene.draw()
    mock_scene.reset_game_values()
    mock_scene.reset_game_values_for_children()

def test_set_scene(mock_scene: 'StartingScene', game_values):
    mock_scene.set_scene(game_values)
    assert mock_scene.game_values == game_values
    assert mock_scene.main_container == main_container
    assert mock_scene.main_menu == main_container.children[0]
    assert mock_scene.main_menu.children == main_container.children[0].children
