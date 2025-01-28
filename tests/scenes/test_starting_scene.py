import pytest
from game.scenes.startingScene import StartingScene
from game.entities.uiComponents.containers.main_container import main_container
from game.core.game_loop import Game

@pytest.fixture
def scene():
    scene = StartingScene("TestScene", top_level=True)
    game_values = Game().game_values
    scene.set_game_values(game_values)
    scene.set_scene()
    scene.enable()
    return scene

def test_handle_events_if_not_active(scene: 'StartingScene'):
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.handle_events()
    assert "TestScene is not active." in str(exc.value)

def test_update_if_not_active(scene: 'StartingScene'):
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.update()
    assert "TestScene is not active." in str(exc.value)

def test_draw_if_not_active(scene: 'StartingScene'):
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.draw()
    assert "TestScene is not active." in str(exc.value)

def test_handle_events_if_active(scene: 'StartingScene'):
    scene.handle_events()

def test_update_if_active(scene: 'StartingScene'):
    scene.update()
