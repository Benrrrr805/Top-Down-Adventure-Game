# tests/test_event_queue.py

import pytest
from unittest.mock import MagicMock
from game.core.event_queue import EventQueue

@pytest.fixture
def mock_pygame():
    """
    Fixture to mock the pygame module for testing.
    """
    mock_pygame = MagicMock()
    # For convenience, define some constants typically found in pygame
    mock_pygame.MOUSEBUTTONDOWN = 1
    mock_pygame.MOUSEBUTTONUP = 2
    mock_pygame.KEYDOWN = 3
    mock_pygame.KEYUP = 4
    mock_pygame.QUIT = 5
    mock_pygame.MOUSEMOTION = 6
    mock_pygame.MOUSEWHEEL = 7

    # Mock time.get_ticks() so we have a stable timestamp
    mock_pygame.time.get_ticks.return_value = 123

    return mock_pygame

def test_init_queue(mock_pygame):
    eq = EventQueue(mock_pygame, debug=True)
    eq.init_queue()
    assert isinstance(eq.event_queue, list)
    assert eq.event_queue == []

def test_validate_queue_raises_when_none(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    with pytest.raises(ValueError, match="Event queue is None"):
        eq.validate_queue()

def test_validate_queue_raises_when_not_list(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.event_queue = "NOT A LIST"
    with pytest.raises(ValueError, match="Event queue is not a list"):
        eq.validate_queue()

def test_add_event_success(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    event = {
        "type": "MOUSEBUTTONDOWN",
        "timestamp": 100
    }
    eq.add_event(event)
    assert len(eq.event_queue) == 1
    assert eq.event_queue[0] == event

def test_add_event_invalid_type_raises(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.add_event("NOT A VALID EVENT")

def test_has_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    sample_event = {"type": "KEYDOWN", "timestamp": 200, "key": 32}
    eq.add_event(sample_event)

    assert eq.has_event("KEYDOWN") is True
    assert eq.has_event("QUIT") is False

def test_remove_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    e1 = {"type": "KEYDOWN", "timestamp": 1}
    e2 = {"type": "QUIT", "timestamp": 2}
    eq.add_event(e1)
    eq.add_event(e2)

    # Remove KEYDOWN
    eq.remove_event("KEYDOWN")
    assert eq.has_event("KEYDOWN") is False
    assert eq.has_event("QUIT") is True

def test_handle_events(mock_pygame):
    """
    Ensure that handle_events() transforms raw pygame events 
    into the expected dictionary events in the internal queue.
    """
    # Setup mock events
    mock_event_down = MagicMock()
    mock_event_down.type = mock_pygame.MOUSEBUTTONDOWN
    mock_event_down.button = 1
    mock_event_down.pos = (100, 200)

    mock_event_up = MagicMock()
    mock_event_up.type = mock_pygame.MOUSEBUTTONUP
    mock_event_up.button = 1
    mock_event_up.pos = (100, 200)

    # We'll mock pygame.event.get() to return these
    mock_pygame.event.get.return_value = [mock_event_down, mock_event_up]

    eq = EventQueue(mock_pygame, debug=True)
    eq.init_queue()

    eq.handle_events()

    assert len(eq.event_queue) == 2
    first = eq.event_queue[0]
    assert first["type"] == "MOUSEBUTTONDOWN"
    assert first["button"] == 1
    assert first["pos"] == (100, 200)
    assert first["timestamp"] == 123  # from mock get_ticks

def test_max_events_truncation(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False, max_events=2)
    eq.init_queue()

    # Return no new events for this test
    mock_pygame.event.get.return_value = []

    # Add 3 events and ensure the queue is truncated down to 2
    e1 = {"type": "KEYDOWN", "timestamp": 1}
    e2 = {"type": "KEYUP", "timestamp": 2}
    e3 = {"type": "MOUSEBUTTONDOWN", "timestamp": 3}

    eq.add_event(e1)
    eq.add_event(e2)
    eq.add_event(e3)
    eq.handle_events()  # triggers the queue pop if over max

    # We expect the oldest event to be dropped
    print(eq.event_queue)
    assert len(eq.event_queue) == 2
    assert eq.event_queue[0] == e2
    assert eq.event_queue[1] == e3



