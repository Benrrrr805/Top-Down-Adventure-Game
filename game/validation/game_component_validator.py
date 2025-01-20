from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.validation.node_validator import NodeValidator

class GameComponentValidator(NodeValidator):
    """
    A validator that checks consistency of a GameComponent (GameComponent).
    """
    
    @staticmethod
    def validate_base_values(game_component: 'GameComponent') -> bool:
        """
        Validate base GameComponent values, then optionally validate UI details.
        """
        if not isinstance(game_component.need_to_update, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. need_to_update must be a boolean.")
        if not isinstance(game_component.active, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. active must be a boolean.")
        if not isinstance(game_component.event_queue, EventQueue):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. event_queue must be an EventQueue.")
        if not isinstance(game_component.helper_functions, dict):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. helper_functions must be a dictionary.")
        if not isinstance(game_component.debug, bool):
            raise ValueError(f"GameComponent: {game_component.name} - Failed validation. debug must be a boolean.")
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