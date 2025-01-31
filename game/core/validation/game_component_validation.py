from __future__ import annotations
from typing import TYPE_CHECKING
from game.core.event_queue import EventQueue
import pygame


if TYPE_CHECKING:
    from game.core.game_component import GameComponent

class GameComponentValidation:
    """
    A class to validate GameComponent objects.
    """
    @staticmethod
    def _is_valid_pygame_instance(pygame_instance) -> bool:
        return pygame_instance is not None and pygame_instance is pygame

    @staticmethod
    def _is_valid_screen(screen: pygame.Surface) -> bool:
        return screen is not None and isinstance(screen, pygame.Surface)

    @staticmethod
    def _is_valid_display(display: pygame.Surface) -> bool:
        return display is not None and display is pygame.display

    @staticmethod
    def _is_valid_event_queue(event_queue: EventQueue) -> bool:
        return event_queue is not None and isinstance(event_queue, EventQueue)

    @staticmethod
    def _is_valid_debug_color(debug_color: tuple) -> bool:
        return isinstance(debug_color, tuple) and len(debug_color) in (3, 4)

    @staticmethod
    def _is_valid_debug(debug: bool) -> bool:
        return isinstance(debug, bool)

    @staticmethod
    def validate_pygame(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_pygame_instance(game_component.pygame):
            raise ValueError(f"GameComponent must have a pygame instance. - {game_component.name}")
        return True

    @staticmethod
    def validate_screen(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_screen(game_component.screen):
            raise ValueError(f"GameComponent must have a screen (pygame.Surface). - {game_component.name}")
        return True

    @staticmethod
    def validate_display(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_display(game_component.display):
            raise ValueError(f"GameComponent must have a display (pygame.display). - {game_component.name}")
        return True

    @staticmethod
    def validate_event_queue(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_event_queue(game_component.event_queue):
            raise ValueError(f"GameComponent must have an event_queue (EventQueue). - {game_component.name}")
        return True

    @staticmethod
    def validate_helper_functions(game_component: 'GameComponent') -> bool:
        if not isinstance(game_component.helper_functions, dict):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"helper_functions must be a dictionary."
            )
        for key, value in game_component.helper_functions.items():
            if not callable(value):
                raise ValueError(
                    f"GameComponent: {game_component.name} - Failed validation. "
                    f"Helper function '{key}' must be callable."
                )
        return True

    @staticmethod
    def validate_debug_color(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_debug_color(game_component.debug_color):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"debug_color must be an RGB or RGBA tuple."
            )
        return True

    @staticmethod
    def validate_active(game_component: 'GameComponent') -> bool:
        if not isinstance(game_component.active, bool):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"active must be a boolean."
            )
        return True


    @staticmethod
    def validate_debug(game_component: 'GameComponent') -> bool:
        if not GameComponentValidation._is_valid_debug(game_component.debug):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"debug must be a boolean."
            )
        return True

    @staticmethod
    def validate_need_to_update(game_component: 'GameComponent') -> bool:
        if not isinstance(game_component.need_to_update, bool):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"need_to_update must be a boolean."
            )
        return True

    @staticmethod
    def validate_is_game_component(game_component: 'GameComponent') -> bool:
        if not type(game_component).__name__ == 'GameComponent':
            raise ValueError(
                f"Expected game_component to be GameComponent, "
                f"but instead got type {type(game_component)}"
            )
        return True

    @staticmethod
    def validate_is_enabled(game_component: 'GameComponent') -> bool:
        if not game_component.active:
            raise ValueError(f"GameComponent must be enabled - {game_component.name}")
        return True

    @staticmethod
    def validate_is_disabled(game_component: 'GameComponent') -> bool:
        if game_component.active:
            raise ValueError(f"GameComponent must be disabled - {game_component.name}")
        return True

    @staticmethod
    def validate_base_values(game_component: 'GameComponent') -> bool:
        """
        Run the core validations for a standard GameComponent.
        """
        GameComponentValidation.validate_pygame(game_component)
        GameComponentValidation.validate_screen(game_component)
        GameComponentValidation.validate_display(game_component)
        GameComponentValidation.validate_event_queue(game_component)
        GameComponentValidation.validate_helper_functions(game_component)
        GameComponentValidation.validate_debug_color(game_component)
        GameComponentValidation.validate_active(game_component)
        GameComponentValidation.validate_debug(game_component)
        GameComponentValidation.validate_need_to_update(game_component)
        return True

    @staticmethod
    def full_validate(game_component: 'GameComponent') -> bool:
        """
        Validate that `game_component` is indeed a GameComponent
        and that its "base values" are also correct.
        """
        GameComponentValidation.validate_is_game_component(game_component)
        GameComponentValidation.validate_base_values(game_component)
        return True
