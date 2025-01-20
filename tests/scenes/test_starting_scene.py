import pytest
from game.scenes.startingScene import StartingScene
from game.entities.uiComponents.containers.main_container import main_container
from game.core.game_loop import Game

@pytest.fixture
def game_values():
    g = Game()
    game_values = g.game_values
    return game_values

@pytest.fixture
def scene():
    scene = StartingScene("TestScene", top_level=True)
    return scene

def test_handle_events_if_not_active(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.handle_events()
    assert "TestScene is not active." in str(exc.value)

def test_update_if_not_active(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.update()
    assert "TestScene is not active." in str(exc.value)

def test_draw_if_not_active(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.disable()
    with pytest.raises(ValueError) as exc:
        scene.draw()
    assert "TestScene is not active." in str(exc.value)

def test_handle_events_if_active(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.enable()
    scene.handle_events()

def test_update_if_active(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.enable()
    scene.update()

def test_draw_if_active_but_no_game_values(scene: 'StartingScene'):
    scene.link_child(main_container)
    scene.enable()
    with pytest.raises(AttributeError) as exc:
        scene.draw()
    assert "'NoneType' object has no attribute 'fill'" in str(exc.value)

def test_draw_if_active_with_game_values(scene: 'StartingScene', game_values):
    scene.link_child(main_container)
    scene.enable()
    scene.set_game_values(game_values)
    scene.set_game_values_for_children(game_values)
    scene.draw()
    scene.reset_game_values()
    scene.reset_game_values_for_children()

def test_set_scene(scene: 'StartingScene', game_values):
    scene.set_scene(game_values)
    assert scene.game_values == game_values
    assert scene.main_container == main_container
    assert scene.main_menu == main_container.children[0]
    assert scene.main_menu.children == main_container.children[0].children
