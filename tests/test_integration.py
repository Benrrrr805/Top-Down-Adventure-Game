# tests/test_integration.py

import pytest
from unittest.mock import MagicMock
from game.core.game_loop import Game

def test_integration_basic_run():
    """
    Verifies that we can instantiate and run the game loop for a few ticks 
    without crashing. We'll mock out infinite loops or windows.
    """
    g = Game()
    g.screen = MagicMock()
    g.display = MagicMock()
    g.clock = MagicMock()
    # Instead of a real game loop, we do a small iteration
    g.running = True
    iteration_count = 0

    def side_effect_clock_tick(fps):
        nonlocal iteration_count
        iteration_count += 1
        # End after 3 frames
        if iteration_count >= 3:
            g.running = False
        return 16  # ms

    g.clock.tick.side_effect = side_effect_clock_tick
    g.run()

    assert iteration_count == 3
