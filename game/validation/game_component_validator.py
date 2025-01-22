from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.validation.node_validator import NodeValidator
import pygame

class GameComponentValidator(NodeValidator):
    """
    A validator that checks consistency of a GameComponent (GameComponent).
    """
    
    @staticmethod
    def validate_base_values(game_component: 'GameComponent') -> bool:
        """
        Validate base GameComponent values
        self.pygame: pygame = None
        self.screen: Surface = None
        self.display: display = None
        self.event_queue: EventQueue = None
        self.helper_functions: dict = {}
        self.game_values: dict = {}
        self.active: bool = False
        self.game_values_set: bool = False
        self.debug: bool = False
        self.need_to_update: bool = False
        """
        if game_component.pygame is None or not game_component.pygame is pygame:
            raise ValueError(f"VisualComponent must have a pygame instance. - {game_component.name}")
        if game_component.screen is None or not isinstance(game_component.screen, pygame.Surface):
            raise ValueError(f"VisualComponent must have a screen. - {game_component.name}")
        if game_component.display is None or not game_component.display is pygame.display:
            raise ValueError(f"VisualComponent must have a display. - {game_component.name}")
        if game_component.event_queue is None or not game_component.event_queue is EventQueue:
            raise ValueError(f"VisualComponent must have an event_queue. - {game_component.name}")
        if not isinstance(game_component.helper_functions, dict):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. helper_functions must be a dictionary.")
        if not isinstance(game_component.game_values, dict):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. game_values must be a dictionary.")
        if not isinstance(game_component.debug_color, tuple):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. debug_color must be a tuple.")
        if len(game_component.debug_color) not in (3, 4):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. debug_color must be an RGB or RGBA tuple.")
        if not isinstance(game_component.active, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. active must be a boolean.")
        if not isinstance(game_component.game_values_set, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. game_values_set must be a boolean.")
        if not isinstance(game_component.debug, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. debug must be a boolean.")
        if not isinstance(game_component.need_to_update, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. need_to_update must be a boolean.")
        return True
    
    @staticmethod
    def full_validate(game_component: 'GameComponent') -> bool:
        GameComponentValidator.validate_is_game_component(game_component)
        GameComponentValidator.validate_base_values(game_component)
        return True

    @staticmethod
    def validate_is_game_component(game_component: 'GameComponent') -> bool:
        if not isinstance(game_component, GameComponent):
            raise ValueError(f'Expected game_component to be GameComponent, but instead got type {type(game_component)}')
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