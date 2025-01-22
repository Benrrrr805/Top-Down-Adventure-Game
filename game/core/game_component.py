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