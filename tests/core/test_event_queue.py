import pytest
import pygame
import json
from unittest.mock import MagicMock

from game.core.event_queue import EventQueue

def test_init_queue():
    eq = EventQueue(pygame, debug=True)
    assert isinstance(eq.event_queue, list)
    assert eq.event_queue == []

def test_to_dict():
    eq = EventQueue(pygame, debug=False)
    eq.event_queue = [{"type": "MOUSEBUTTONDOWN", "timestamp": 100}]
    eq.last_mouse_pos = (100, 200)

    d = eq.to_dict()
    assert d["event_queue"] == eq.event_queue
    assert d["last_mouse_pos"] == eq.last_mouse_pos
    assert d["max_events"] == eq.max_events

def test_str():
    eq = EventQueue(pygame, debug=False)
    eq.event_queue = [{"type": "MOUSEBUTTONDOWN", "timestamp": 100}]
    eq.last_mouse_pos = (100, 200)

    d = eq.to_dict()
    s = eq.__str__()
    assert s == json.dumps(d, indent=4)

def test_validate_queue_raises_when_none():
    eq = EventQueue(pygame, debug=False)
    eq.event_queue = None
    with pytest.raises(ValueError, match="Event queue is None"):
        eq.validate_queue()

def test_validate_queue_raises_when_not_list():
    eq = EventQueue(pygame, debug=False)
    eq.event_queue = "NOT A LIST"
    with pytest.raises(ValueError, match="Event queue is not a list"):
        eq.validate_queue()

def test_validate_queue_recursive():
    eq = EventQueue(pygame, debug=False)

    eq.event_queue = []
    eq.validate_queue()

    eq.event_queue = [{"type": "MOUSEBUTTONDOWN", "timestamp": 100}]
    eq.validate_queue()

    eq.event_queue = [
        {"type": "MOUSEBUTTONDOWN", "timestamp": 100},
        {"type": "KEYDOWN", "timestamp": 200},
    ]
    eq.validate_queue()

    eq.event_queue = ["NOT A VALID EVENT"]
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.validate_queue(recursive=True)

def test_validate_event_raises_when_not_dict():
    eq = EventQueue(pygame, debug=False)
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.validate_event("NOT A VALID EVENT")

def test_validate_event_raises_when_no_type():
    eq = EventQueue(pygame, debug=False)
    with pytest.raises(ValueError, match="Event does not have a type"):
        eq.validate_event({"timestamp": 100})

def test_validate_event_raises_when_no_timestamp():
    eq = EventQueue(pygame, debug=False)
    with pytest.raises(ValueError, match="Event does not have a timestamp"):
        eq.validate_event({"type": "MOUSEBUTTONDOWN"})

def test_validate_event_raises_when_type_not_handled():
    eq = EventQueue(pygame, debug=False)
    with pytest.raises(ValueError, match="Event type not handled: MOUSEBUTTONDOWN"):
        eq.validate_event({"type": "MOUSEBUTTONDOWN_", "timestamp": 100})

def test_validate_event_success():
    eq = EventQueue(pygame, debug=False)
    eq.validate_event({"type": "MOUSEBUTTONDOWN", "timestamp": 100})

def test_add_event_success():
    eq = EventQueue(pygame, debug=False)

    event = {
        "type": "MOUSEBUTTONDOWN",
        "timestamp": 100,
    }
    eq.add_event(event)
    assert len(eq.event_queue) == 1
    assert eq.event_queue[0] == event

def test_add_event_invalid_type_raises():
    eq = EventQueue(pygame, debug=False)
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.add_event("NOT A VALID EVENT")

def test_get_last_event_empty_queue():
    eq = EventQueue(pygame, debug=False)
    assert eq.get_last_event() is None

def test_get_last_event_success():
    eq = EventQueue(pygame, debug=False)

    event = {
        "type": "MOUSEBUTTONDOWN",
        "timestamp": 100,
    }
    eq.add_event(event)
    assert eq.get_last_event() == event
    assert len(eq.event_queue) == 0

def test_has_event_empty_queue():
    eq = EventQueue(pygame, debug=False)
    assert eq.has_event("KEYDOWN") is False

def test_has_event():
    eq = EventQueue(pygame, debug=False)
    sample_event = {"type": "KEYDOWN", "timestamp": 200, "key": 32}
    eq.add_event(sample_event)

    assert eq.has_event("KEYDOWN", extras={"key": 32}) is True
    assert eq.has_event("KEYDOWN", extras={"key": 33}) is False
    assert eq.has_event("KEYDOWN") is True
    assert eq.has_event("QUIT") is False

def test_has_invalid_event():
    eq = EventQueue(pygame, debug=False)
    assert eq.has_event("INVALID_EVENT") is False

def test_remove_event():
    eq = EventQueue(pygame, debug=False)

    e1 = {"type": "KEYDOWN", "timestamp": 1}
    e2 = {"type": "QUIT", "timestamp": 2}
    eq.add_event(e1)
    eq.add_event(e2)

    eq.remove_event("KEYDOWN")
    assert eq.has_event("KEYDOWN") is False
    assert eq.has_event("QUIT") is True

def test_handle_events():
    """
    Ensure that handle_events() transforms raw pygame events 
    into the expected dictionary events in the internal queue.
    """
    mock_event_down = MagicMock()
    mock_event_down.type = pygame.MOUSEBUTTONDOWN
    mock_event_down.button = 1
    mock_event_down.pos = (100, 200)

    mock_event_up = MagicMock()
    mock_event_up.type = pygame.MOUSEBUTTONUP
    mock_event_up.button = 1
    mock_event_up.pos = (100, 200)

    pygame.init()
    pygame.display.init()

    eq = EventQueue(pygame, debug=True)
    eq.handle_events()

    down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (100, 200)})
    up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (100, 200)})
    invalid_event = pygame.event.Event(494, {"invalid": "data"})

    pygame.event.post(down)
    pygame.event.post(up)
    pygame.event.post(invalid_event)

    eq.handle_events()
    print(eq.event_queue)

    assert len(eq.event_queue) == 2
    first = eq.event_queue[0]
    assert first["type"] == "MOUSEBUTTONDOWN"
    assert first["button"] == 1
    assert first["pos"] == (100, 200)

def test_handle_mouse_motion_event():
    """
    Ensure that handle_events() transforms raw pygame MOUSEMOTION events 
    and updates last_mouse_pos without adding them to the queue.
    """
    pygame.init()
    pygame.display.init()

    eq = EventQueue(pygame, debug=True)
    motion = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (100, 200)})

    eq.handle_events()

    pygame.event.post(motion)
    eq.handle_events()

    assert len(eq.event_queue) == 0
    assert eq.last_mouse_pos == (100, 200)

def test_max_events_truncation():
    eq = EventQueue(pygame, debug=False, max_events=2)

    e1 = {"type": "KEYDOWN", "timestamp": 1}
    e2 = {"type": "KEYUP", "timestamp": 2}
    e3 = {"type": "MOUSEBUTTONDOWN", "timestamp": 3}

    eq.add_event(e1)
    eq.add_event(e2)
    eq.add_event(e3)
    eq.handle_events()
    assert len(eq.event_queue) == 2
    assert eq.event_queue[0] == e2
    assert eq.event_queue[1] == e3

def test_base_event():
    eq = EventQueue(pygame, debug=False)

    extras = {
        "key": 32,
        "mod": 0,
        "unicode": "a",
    }
    event = eq.base_event(extras)

    assert event["key"] == 32
    assert event["mod"] == 0
    assert event["unicode"] == "a"

def test_mouse_button_down_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.button = 1
    mock_event.pos = (100, 200)

    event = eq.MOUSEBUTTONDOWN(mock_event)

    assert event["type"] == "MOUSEBUTTONDOWN"
    assert event["button"] == 1
    assert event["pos"] == (100, 200)

def test_mouse_button_up_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.button = 1
    mock_event.pos = (100, 200)

    event = eq.MOUSEBUTTONUP(mock_event)

    assert event["type"] == "MOUSEBUTTONUP"
    assert event["button"] == 1
    assert event["pos"] == (100, 200)

def test_key_down_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.key = 32
    mock_event.mod = 0
    mock_event.unicode = "a"

    event = eq.KEYDOWN(mock_event)

    assert event["type"] == "KEYDOWN"
    assert event["key"] == 32
    assert event["mod"] == 0
    assert event["unicode"] == "a"

def test_key_up_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.key = 32
    mock_event.mod = 0

    event = eq.KEYUP(mock_event)

    assert event["type"] == "KEYUP"
    assert event["key"] == 32
    assert event["mod"] == 0

def test_quit_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    event = eq.QUIT(mock_event)

    assert event["type"] == "QUIT"

def test_mouse_motion_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.pos = (100, 200)
    mock_event.rel = (10, 20)
    mock_event.buttons = (1, 0, 0)

    event = eq.MOUSEMOTION(mock_event)

    assert event["type"] == "MOUSEMOTION"
    assert event["pos"] == (100, 200)
    assert event["rel"] == (10, 20)
    assert event["buttons"] == (1, 0, 0)

def test_mouse_wheel_event():
    eq = EventQueue(pygame, debug=False)

    mock_event = MagicMock()
    mock_event.flipped = 1
    mock_event.pos = (0, 0)

    event = eq.MOUSEWHEEL(mock_event)

    assert event["type"] == "MOUSEWHEEL"
    assert event["flipped"] == 1
    assert event["pos"] == (0, 0)
