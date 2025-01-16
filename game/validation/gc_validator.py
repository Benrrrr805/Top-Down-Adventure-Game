from game.core.game_component import GameComponent
from game.core.event_queue import EventQueue
from game.validation.node_validator import NodeValidator

class GameComponentValidator(NodeValidator):
    """
    A validator that checks consistency of a GameComponent (GameComponent).
    """
    
    @staticmethod
    def validate_base_values(gc: 'GameComponent') -> bool:
        """
        Validate base GameComponent values, then optionally validate UI details.
        """
        if not isinstance(gc.need_to_update, bool):
            raise ValueError(f"GameComponent: {gc.name} - Failed validation. need_to_update must be a boolean.")
        if not isinstance(gc.active, bool):
            raise ValueError(f"GameComponent: {gc.name} - Failed validation. active must be a boolean.")
        if not isinstance(gc.event_queue, EventQueue):
            raise ValueError(f"GameComponent: {gc.name} - Failed validation. event_queue must be an EventQueue.")
        if not isinstance(gc.helper_functions, dict):
            raise ValueError(f"GameComponent: {gc.name} - Failed validation. helper_functions must be a dictionary.")
        if not isinstance(gc.debug, bool):
            raise ValueError(f"GameComponent: {gc.name} - Failed validation. debug must be a boolean.")
        return True
    
    @staticmethod
    def full_validate(gc: 'GameComponent') -> bool:
        NodeValidator.full_validate(gc)
        GameComponentValidator.validate_is_gc(gc)
        GameComponentValidator.validate_base_values(gc)
        return True

    @staticmethod
    def validate_is_gc(gc: 'GameComponent') -> bool:
        if not isinstance(gc, GameComponent):
            raise ValueError(f'Expected gc to be GameComponent, but instead got type {type(gc)}')

    @staticmethod
    def validate_is_enabled(gc: 'GameComponent') -> bool:
        if not gc.active:
            raise ValueError(f"GameComponent must be enabled - {gc.name}")
        return True

    @staticmethod
    def validate_is_disabled(gc: 'GameComponent') -> bool:
        if gc.active:
            raise ValueError(f"GameComponent must be disabled - {gc.name}")
        return True