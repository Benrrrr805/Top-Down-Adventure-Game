import pytest
from unittest.mock import MagicMock

from game.core.event_queue import EventQueue


@pytest.fixture
def mock_pygame():
    """
    Fixture to mock the pygame module for testing.
    """
    mock_pg = MagicMock()
    # Define some constants typically found in pygame
    mock_pg.MOUSEBUTTONDOWN = 1
    mock_pg.MOUSEBUTTONUP = 2
    mock_pg.KEYDOWN = 3
    mock_pg.KEYUP = 4
    mock_pg.QUIT = 5
    mock_pg.MOUSEMOTION = 6
    mock_pg.MOUSEWHEEL = 7

    # Mock time.get_ticks() to provide a stable timestamp
    mock_pg.time.get_ticks.return_value = 123

    return mock_pg


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


def test_validate_queue_recursive(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)

    # Empty queue is valid
    eq.event_queue = []
    eq.validate_queue()

    # Single valid event
    eq.event_queue = [{"type": "MOUSEBUTTONDOWN", "timestamp": 100}]
    eq.validate_queue()

    # Multiple valid events
    eq.event_queue = [
        {"type": "MOUSEBUTTONDOWN", "timestamp": 100},
        {"type": "KEYDOWN", "timestamp": 200},
    ]
    eq.validate_queue()

    # Invalid event
    eq.event_queue = ["NOT A VALID EVENT"]
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.validate_queue(recursive=True)


def test_validate_event_raises_when_not_dict(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.validate_event("NOT A VALID EVENT")


def test_validate_event_raises_when_no_type(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    with pytest.raises(ValueError, match="Event does not have a type"):
        eq.validate_event({"timestamp": 100})


def test_validate_event_raises_when_no_timestamp(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    with pytest.raises(ValueError, match="Event does not have a timestamp"):
        eq.validate_event({"type": "MOUSEBUTTONDOWN"})


def test_validate_event_raises_when_type_not_handled(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    with pytest.raises(ValueError, match="Event type not handled: MOUSEBUTTONDOWN"):
        eq.validate_event({"type": "MOUSEBUTTONDOWN_", "timestamp": 100})


def test_validate_event_success(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    # Should not raise
    eq.validate_event({"type": "MOUSEBUTTONDOWN", "timestamp": 100})


def test_add_event_success(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    event = {
        "type": "MOUSEBUTTONDOWN",
        "timestamp": 100,
    }
    eq.add_event(event)
    assert len(eq.event_queue) == 1
    assert eq.event_queue[0] == event


def test_add_event_invalid_type_raises(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    with pytest.raises(ValueError, match="Event is not a dictionary"):
        eq.add_event("NOT A VALID EVENT")


def test_get_last_event_empty_queue(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    assert eq.get_last_event() is None


def test_get_last_event_success(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    event = {
        "type": "MOUSEBUTTONDOWN",
        "timestamp": 100,
    }
    eq.add_event(event)
    assert eq.get_last_event() == event
    assert len(eq.event_queue) == 0


def test_has_event_empty_queue(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    assert eq.has_event("KEYDOWN") is False


def test_has_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    sample_event = {"type": "KEYDOWN", "timestamp": 200, "key": 32}
    eq.add_event(sample_event)

    # Matching extras
    assert eq.has_event("KEYDOWN", extras={"key": 32}) is True
    # Non-matching extras
    assert eq.has_event("KEYDOWN", extras={"key": 33}) is False

    # Without extras
    assert eq.has_event("KEYDOWN") is True
    assert eq.has_event("QUIT") is False


def test_has_invalid_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()
    assert eq.has_event("INVALID_EVENT") is False


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

    # Mock pygame.event.get() to return these
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


def test_handle_mouse_motion_event(mock_pygame):
    """
    Ensure that handle_events() transforms raw pygame MOUSEMOTION events 
    and updates last_mouse_pos without adding them to the queue.
    """
    mock_event_motion = MagicMock()
    mock_event_motion.type = mock_pygame.MOUSEMOTION
    mock_event_motion.pos = (100, 200)

    mock_pygame.event.get.return_value = [mock_event_motion]

    eq = EventQueue(mock_pygame, debug=True)
    eq.init_queue()
    eq.handle_events()

    # MOUSEMOTION should not be added to the internal queue but
    # should update last_mouse_pos
    assert len(eq.event_queue) == 0
    assert eq.last_mouse_pos == (100, 200)


def test_max_events_truncation(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False, max_events=2)
    eq.init_queue()

    mock_pygame.event.get.return_value = []

    # Add 3 events and ensure the queue is truncated to 2
    e1 = {"type": "KEYDOWN", "timestamp": 1}
    e2 = {"type": "KEYUP", "timestamp": 2}
    e3 = {"type": "MOUSEBUTTONDOWN", "timestamp": 3}

    eq.add_event(e1)
    eq.add_event(e2)
    eq.add_event(e3)
    eq.handle_events()  # triggers the queue pop if over max

    # We expect the oldest event to be dropped
    assert len(eq.event_queue) == 2
    assert eq.event_queue[0] == e2
    assert eq.event_queue[1] == e3


def test_base_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    extras = {
        "key": 32,
        "mod": 0,
        "unicode": "a",
    }
    event = eq.base_event(extras)
    assert event["timestamp"] == 123
    assert event["key"] == 32
    assert event["mod"] == 0
    assert event["unicode"] == "a"


def test_mouse_button_down_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.button = 1
    mock_event.pos = (100, 200)

    event = eq.MOUSEBUTTONDOWN(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "MOUSEBUTTONDOWN"
    assert event["button"] == 1
    assert event["pos"] == (100, 200)


def test_mouse_button_up_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.button = 1
    mock_event.pos = (100, 200)

    event = eq.MOUSEBUTTONUP(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "MOUSEBUTTONUP"
    assert event["button"] == 1
    assert event["pos"] == (100, 200)


def test_key_down_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.key = 32
    mock_event.mod = 0
    mock_event.unicode = "a"

    event = eq.KEYDOWN(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "KEYDOWN"
    assert event["key"] == 32
    assert event["mod"] == 0
    assert event["unicode"] == "a"


def test_key_up_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.key = 32
    mock_event.mod = 0

    event = eq.KEYUP(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "KEYUP"
    assert event["key"] == 32
    assert event["mod"] == 0


def test_quit_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    event = eq.QUIT(mock_event)

    assert event["timestamp"] == 123
    assert event["type"] == "QUIT"


def test_mouse_motion_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.pos = (100, 200)
    mock_event.rel = (10, 20)
    mock_event.buttons = (1, 0, 0)

    event = eq.MOUSEMOTION(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "MOUSEMOTION"
    assert event["pos"] == (100, 200)
    assert event["rel"] == (10, 20)
    assert event["buttons"] == (1, 0, 0)


def test_mouse_wheel_event(mock_pygame):
    eq = EventQueue(mock_pygame, debug=False)
    eq.init_queue()

    mock_event = MagicMock()
    mock_event.flipped = 1
    mock_event.pos = (0, 0)  # if you rely on pos for mouse wheel

    event = eq.MOUSEWHEEL(mock_event)
    assert event["timestamp"] == 123
    assert event["type"] == "MOUSEWHEEL"
    assert event["flipped"] == 1
    assert event["pos"] == (0, 0)
