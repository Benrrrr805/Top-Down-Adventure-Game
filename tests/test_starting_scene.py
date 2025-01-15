import pytest
from unittest.mock import MagicMock, patch
import pygame

# Assuming your GameComponent class is in game_component.py or similar
# from game_component import GameComponent
# For brevity, we'll pretend it's imported:
from game.scenes.startingScene import StartingScene

@pytest.fixture
def mock_inactive_scene():
    scene = StartingScene("TestScene")
    scene.active = False
    return scene


def test_handle_events_if_not_active(mock_inactive_scene):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.handle_events()
    assert "TestScene is not active." in str(exc.value)

def test_update_if_not_active(mock_inactive_scene):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.update()
    assert "TestScene is not active." in str(exc.value)

def test_draw_if_not_active(mock_inactive_scene):
    with pytest.raises(ValueError) as exc:
        mock_inactive_scene.draw()
    assert "TestScene is not active." in str(exc.value)