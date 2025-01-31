import pytest
import pygame

from game.core.event_queue import EventQueue
from game.core.game_component import GameComponent
from game.scenes.startingScene import StartingScene
from game.core.game_loop import Game  # <-- Adjust if your "Game" class is in a different path


@pytest.fixture(scope="module", autouse=True)
def pygame_setup_teardown():
    """
    Initialize pygame once for all tests, and then quit afterwards.
    This prevents leftover resources or processes after tests complete.
    """
    pygame.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.quit()


@pytest.fixture
def game_instance():
    """
    Creates and returns a fresh Game object for each test.
    This ensures no leftover state between tests.
    """
    return Game()


def test_game_inherits_from_game_component(game_instance: Game):
    """
    Ensures that the Game class is indeed a subclass of GameComponent.
    """
    assert isinstance(game_instance, GameComponent)


def test_game_initial_state(game_instance: Game):
    """
    Validates that the initial state of the Game object
    matches the default attributes set in its constructor.
    """
    assert game_instance.debug is True
    assert game_instance.frame_rate is None
    assert game_instance.show_fps is False
    assert game_instance.running is True
    assert game_instance.debug_color == (0, 0, 0)  # matches the constructor's BLACK
    assert isinstance(game_instance.display, type(pygame.display))
    assert isinstance(game_instance.screen, pygame.Surface)
    assert isinstance(game_instance.clock, pygame.time.Clock)
    assert isinstance(game_instance.event_queue, EventQueue)
    assert game_instance.active is False
    assert isinstance(game_instance.helper_functions, dict)
    assert game_instance.top_level is True
    assert game_instance.need_to_update is False
    assert game_instance.name == "Game"

    assert game_instance.pygame is pygame
    assert isinstance(game_instance.screen, pygame.Surface)
    assert game_instance.display is pygame.display
    assert game_instance.debug is True
    assert game_instance.debug_color == (0, 0, 0)  # matches the constructor's BLUE
    assert isinstance(game_instance.event_queue, EventQueue)


def test_game_close_window(game_instance: Game):
    """
    Verifies closeWindow() sets running to False.
    """
    assert game_instance.running is True
    game_instance.closeWindow()
    assert game_instance.running is False


def test_is_terminated_no_events(game_instance: Game):
    """
    With no QUIT or ESC key events in the queue, is_terminated() should be False.
    """
    # Clear the event queue or ensure it has no QUIT/ESC events
    game_instance.event_queue.event_queue = []
    assert not game_instance.is_terminated()


def test_is_terminated_quit_event(game_instance: Game):
    """
    If a QUIT event is in the queue, is_terminated() should be True.
    """
    game_instance.event_queue.event_queue = [{"type": 'QUIT'}]
    assert game_instance.is_terminated()


def test_is_terminated_esc_event(game_instance: Game):
    """
    If a KEYDOWN event with key=27 (ESC) is in the queue, is_terminated() should be True.
    """
    game_instance.event_queue.event_queue = [{"type": "KEYDOWN", "key": 27}]
    assert game_instance.is_terminated()


def test_handle_events_inactive(game_instance: Game):
    """
    Ensures handle_events() processes the event queue and checks for termination.
    When inactive, `scene.handle_events()` shouldn't be called, but no error should occur.
    """
    # Provide a QUIT event to ensure handle_events() eventually sets running=False
    game_instance.event_queue.event_queue = [{"type": "QUIT"}]
    game_instance.handle_events()
    assert not game_instance.running  # Because it saw QUIT event and closed


def test_update_inactive(game_instance: Game):
    """
    With the game inactive, update() should not attempt to update a scene,
    but should still run helper_functions if any.
    """
    # Provide a helper function
    was_called = {"flag": False}
    
    def update_helper(self, context, from_helper):
        print("Update helper ran.")
        was_called["flag"] = True

    # game_instance.helper_functions["update"] = update_helper
    game_instance.add_helper_function("update_helper", update_helper, ["update"])
    print(game_instance.helper_functions)
    game_instance.update()
    assert was_called["flag"] is True  # update helper ran
    # No scene is set, so no error should occur.


def test_draw_inactive(game_instance: Game):
    """
    With the game inactive, draw() should not attempt to draw a scene,
    but should still run any 'draw' helper functions.
    """
    was_called = {"flag": False}
    
    def draw_helper(self, context, from_helper):
        was_called["flag"] = True

    game_instance.add_helper_function("draw_helper", draw_helper, ["draw"])
    game_instance.draw()
    assert was_called["flag"] is True


def test_set_scene_enables_game(game_instance: Game):
    """
    set_scene should link the child (StartingScene), set it, assign it to self.scene,
    and then enable the game (active=True).
    """
    scene = StartingScene("Starting Scene", False)
    game_instance.set_scene(scene)

    assert game_instance.scene is scene
    assert game_instance.active is True
    # The scene itself is set to 'active' inside set_scene() or the scene’s method.
    assert scene.active is True


@pytest.mark.skip(reason="Infinite loop. Only run if you specifically want to test the main loop.")
def test_run_method(game_instance: Game):
    """
    If you wanted to test `game_instance.run()` in an automated scenario,
    you'd likely need to intercept or break the loop. This is typically
    done with mocks, or by injecting a short-circuit condition into your game loop.
    Since the requirement is to avoid mocks, we skip this by default.
    """
    # game_instance.run()
    # Without mocking or an exit condition, this will block indefinitely.
    game_instance.set_scene(StartingScene("Starting Scene", False))
    game_instance.event_queue.event_queue = [{"type": "QUIT"}]
    game_instance.running = True
    game_instance.show_fps = True
    game_instance.run()
