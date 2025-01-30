from types import FunctionType
from game.core.event_queue import EventQueue
from game.core.node import Node
import json
import pygame
from pygame import Surface, display

class GameComponent(Node):
    def __init__(self, name, top_level, children=None, parent=None):
        super().__init__(name, top_level, children, parent)
        self.pygame: pygame = None
        self.screen: Surface = None
        self.display: display = None
        self.event_queue: EventQueue = None
        self.helper_functions: dict = {}
        self.game_values: dict = {}
        self.active: bool = False
        self.game_values_set: bool = False
        self.debug: bool = False
        self.debug_color: tuple[int, int, int] = None
        self.need_to_update: bool = False
        
    # ------------------------------------------------------------------------
    #  Pretty Printing
    # ------------------------------------------------------------------------

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        node_data = super().to_dict()
        game_component_data = {
            "pygame": type(self.pygame).__name__,
            "screen": type(self.screen).__name__,
            "display": type(self.display).__name__,
            "event_queue": self.event_queue.to_dict() if self.event_queue and isinstance(self.event_queue, EventQueue) else None,
            "helper_functions": self.helper_functions,
            "active": self.active,
            "game_values_set": self.game_values_set,
            "need_to_update": self.need_to_update,
            "debug": self.debug,
            "debug_color": self.debug_color,
        }
        node_data.update(game_component_data)
        return node_data
    
    # ------------------------------------------------------------------------
    # Set Game Values
    # ------------------------------------------------------------------------

    def set_game_values(self, game_values):
        if self.game_values_set:
            print(f"Game values already set for {self.name}. Skipping.")
            return False
        else:
            print(f"Setting game values for {self.name}.")

        self.game_values = game_values
        self.event_queue = game_values['event_queue']
        self.pygame: pygame = game_values['pygame']
        self.screen: Surface = game_values['screen']
        self.display: display = game_values['display']
        self.debug: bool = game_values['debug']
        self.debug_color: tuple[int, int, int] = (255, 0, 0)
        self.game_values_set = True
        return True
    
    def set_game_values_for_children(self):
        for child in self.children:
            if isinstance(child, GameComponent):
                child.set_game_values(self.game_values)
                child.set_game_values_for_children()
    
    # ------------------------------------------------------------------------
    # Reset Game Values
    # ------------------------------------------------------------------------

    def reset_game_values(self):
        self.event_queue = None
        self.pygame = None
        self.screen = None
        self.display = None
        self.debug = False
        self.debug_color = None
        self.game_values = None
        self.game_values_set = False

    def reset_game_values_for_children(self):
        for child in self.children:
            if isinstance(child, GameComponent):
                child.reset_game_values()
                child.reset_game_values_for_children()

    # ------------------------------------------------------------------------
    # Linking Children
    # ------------------------------------------------------------------------
    
    def link_child(self, child):
        super().link_child(child)
        if self.game_values_set and isinstance(child, GameComponent):
            child.set_game_values(self.game_values)
            child.set_game_values_for_children()

    def link_children(parent, children):
        for child in children:
            parent.link_child(child)

    # ----------------------------------------------------------------------
    # Helper Function System (from original GameComponent)
    # ----------------------------------------------------------------------

    def add_helper_function(self, name: str, func: FunctionType, contexts: list[str] = None, enabled: bool = True) -> None:
        """
        Registers a named helper function with optional auto-run contexts.
        """
        if not callable(func):
            raise ValueError(f"Helper function must be callable. - {name}")

        self.helper_functions[name] = {
            "func": func,
            "enabled": enabled,
            "contexts": contexts
        }

    def enable_helper_function(self, name: str) -> None:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        self.helper_functions[name]["enabled"] = True

    def disable_helper_function(self, name: str) -> None:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        self.helper_functions[name]["enabled"] = False

    def set_helper_function_contexts(self, name: str, contexts: list[str]) -> None:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        self.helper_functions[name]["contexts"] = contexts

    def get_helper_function_contexts(self, name: str) -> list[str]:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["contexts"]

    def get_helper_function(self, name: str) -> FunctionType:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["func"]

    def call_helper_function(self, name: str, context: str = "manual", from_helper: str = None, force: bool = False) -> None:
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        info: dict = self.helper_functions[name]
        if not info["enabled"]:
            print(f"Helper function '{name}' is disabled. Not calling.")
            return
        if not force and context not in info["contexts"]:
            print(f"Helper function '{name}' does not handle context '{context}'. Not calling.")
            return

        info["func"](self, context, from_helper)

    def run_helper_functions(self, context: str, from_helper: str = None) -> None:
        """
        Calls all helper functions whose contexts include `context` and are enabled.
        """
        for name, info in self.helper_functions.items():
            if info["enabled"] and context in info["contexts"]:
                info["func"](self, context, from_helper)
        
    # ----------------------------------------------------------------------
    # Event Handling
    # ----------------------------------------------------------------------
    def handle_events_(self) -> None:
        """
        Internal method to handle events recursively in children,
        then call any helper functions for 'handle_events' context.
        """
        # Let children handle events first
        for child in self.children:
            if isinstance(child, GameComponent) and child.active:
                child.handle_events()

        # Then run any helpers
        self.run_helper_functions("handle_events")

    def handle_events(self) -> None:
        """
        Public method to handle events - raises error if inactive.
        """
        if not self.active:
            raise ValueError(f"GameComponent must be enabled before handling events. - {self.name}")
        self.handle_events_()

    # ----------------------------------------------------------------------
    # Updating
    # ----------------------------------------------------------------------
    def update_(self) -> None:
        """
        Internal update logic: handle debugging color changes, update children,
        run update helpers, etc.
        """
        # Update children
        for child in self.children:
            if isinstance(child, GameComponent) and child.active:
                child.update()
                if getattr(child, 'need_to_update', False):
                    self.need_to_update: bool = True

        # Run helper functions
        self.run_helper_functions("update")

    def update(self) -> None:
        """
        Public update method - raises error if inactive.
        """
        if not self.active:
            raise ValueError(f"GameComponent must be enabled before updating. - {self.name}")
        self.update_()

    # ------------------------------------------------------------------------
    #  GameComponent State: Enable / Disable
    # ------------------------------------------------------------------------
    def enable(self) -> None:
        self.active: bool = True
        self.need_to_update: bool = True
        self.enable_children()

    def disable(self) -> None:
        self.active: bool = False
        self.need_to_update: bool = False
        self.disable_children()

    def enable_children(self) -> None:
        for child in self.children:
            if isinstance(child, GameComponent):
                child.enable()

    def disable_children(self) -> None:
        for child in self.children:
            if isinstance(child, GameComponent):
                child.disable()

# ------------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------------

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
        if not GameComponent._is_valid_pygame_instance(game_component.pygame):
            raise ValueError(f"GameComponent must have a pygame instance. - {game_component.name}")
        return True

    @staticmethod
    def validate_screen(game_component: 'GameComponent') -> bool:
        if not GameComponent._is_valid_screen(game_component.screen):
            raise ValueError(f"GameComponent must have a screen (pygame.Surface). - {game_component.name}")
        return True

    @staticmethod
    def validate_display(game_component: 'GameComponent') -> bool:
        if not GameComponent._is_valid_display(game_component.display):
            raise ValueError(f"GameComponent must have a display (pygame.display). - {game_component.name}")
        return True

    @staticmethod
    def validate_event_queue(game_component: 'GameComponent') -> bool:
        if not GameComponent._is_valid_event_queue(game_component.event_queue):
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
    def validate_game_values(game_component: 'GameComponent') -> bool:
        """
        Ensures game_values is a dict with all expected keys and correct object types.
        """
        gv = game_component.game_values
        if not isinstance(gv, dict):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values must be a dictionary."
            )

        # 'pygame' check
        if 'pygame' not in gv or not GameComponent._is_valid_pygame_instance(gv['pygame']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['pygame'] must be a pygame instance."
            )

        # 'screen' check
        if 'screen' not in gv or not GameComponent._is_valid_screen(gv['screen']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['screen'] must be a pygame.Surface."
            )

        # 'display' check
        if 'display' not in gv or not GameComponent._is_valid_display(gv['display']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['display'] must be pygame.display."
            )

        # 'event_queue' check
        if 'event_queue' not in gv or not GameComponent._is_valid_event_queue(gv['event_queue']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['event_queue'] must be EventQueue."
            )

        # 'debug' check
        if 'debug' not in gv or not GameComponent._is_valid_debug(gv['debug']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['debug'] must be a boolean."
            )

        # 'debug_color' check
        if 'debug_color' not in gv or not GameComponent._is_valid_debug_color(gv['debug_color']):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values['debug_color'] must be an RGB or RGBA tuple."
            )

        return True

    @staticmethod
    def validate_debug_color(game_component: 'GameComponent') -> bool:
        if not GameComponent._is_valid_debug_color(game_component.debug_color):
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
    def validate_game_values_set(game_component: 'GameComponent') -> bool:
        if not isinstance(game_component.game_values_set, bool):
            raise ValueError(
                f"GameComponent: {game_component.name} - Failed validation. "
                f"game_values_set must be a boolean."
            )
        return True

    @staticmethod
    def validate_debug(game_component: 'GameComponent') -> bool:
        if not GameComponent._is_valid_debug(game_component.debug):
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
        if not isinstance(game_component, GameComponent):
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
        GameComponent.validate_pygame(game_component)
        GameComponent.validate_screen(game_component)
        GameComponent.validate_display(game_component)
        GameComponent.validate_event_queue(game_component)
        GameComponent.validate_helper_functions(game_component)
        GameComponent.validate_game_values(game_component)
        GameComponent.validate_debug_color(game_component)
        GameComponent.validate_active(game_component)
        GameComponent.validate_game_values_set(game_component)
        GameComponent.validate_debug(game_component)
        GameComponent.validate_need_to_update(game_component)
        return True

    @staticmethod
    def full_validate(game_component: 'GameComponent') -> bool:
        """
        Validate that `game_component` is indeed a GameComponent
        and that its "base values" are also correct.
        """
        GameComponent.validate_is_game_component(game_component)
        GameComponent.validate_base_values(game_component)
        return True
