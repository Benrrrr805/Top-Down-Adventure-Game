# tests/test_game_loop.py

import pytest
from unittest.mock import MagicMock
from game.core.game_loop import Game
from game.core.event_queue import EventQueue

@pytest.fixture
def mock_game():
    g = Game()
    # Overwrite references that might open windows
    g.screen = MagicMock()
    g.display = MagicMock()
    g.clock = MagicMock()
    # Prevent actual PyGame loop from running
    g.running = False
    return g

def test_game_initialization(mock_game):
    # Basic checks
    assert mock_game.name == "Game"
    assert mock_game.top_level is True
    assert mock_game.debug is True
    assert isinstance(mock_game.event_queue, EventQueue)
    assert mock_game.running is False  # Because we overrode it

def test_game_handle_events(mock_game):
    # Mock the event queue
    mock_game.event_queue.handle_events = MagicMock()
    mock_game.is_terminated = MagicMock(return_value=False)

    mock_game.active = True
    scene = MagicMock()
    mock_game.scene = scene

    mock_game.handle_events()
    mock_game.event_queue.handle_events.assert_called_once()
    scene.handle_events.assert_called_once()

def test_game_handle_events_terminated(mock_game):
    # Mock the event queue
    mock_game.event_queue.handle_events = MagicMock()
    mock_game.is_terminated = MagicMock(return_value=True)

    mock_game.handle_events()
    mock_game.event_queue.handle_events.assert_called_once()
    assert mock_game.running is False

def test_game_update(mock_game):
    mock_game.active = True
    scene = MagicMock()
    mock_game.scene = scene

    mock_game.update()
    scene.update.assert_called_once()

def test_game_draw(mock_game):
    mock_game.active = True
    scene = MagicMock()
    mock_game.scene = scene

    mock_game.draw()
    scene.draw.assert_called_once()
