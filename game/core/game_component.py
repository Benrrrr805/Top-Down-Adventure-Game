from types import FunctionType
from game.core.event_queue import EventQueue
from game.core.node import Node
import json

class GameComponent(Node):
    def __init__(self, name, top_level, children=None, parent=None):
        super().__init__(name, top_level, children, parent)
        self.event_queue: EventQueue = None
        self.active: bool = False
        self.pygame_values_set: bool = False
        self.helper_functions: dict = {}
        self.debug: bool = False

    def __str__(self):
        # Pretty-print the dictionary with 4-space indentation
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        node_data = super().to_dict()
        game_component_data = {
            "event_queue": self.event_queue.to_dict() if self.event_queue and isinstance(self.event_queue, EventQueue) else None,
            "active": self.active,
            "pygame_values_set": self.pygame_values_set,
            "helper_functions": self.helper_functions,
            "debug": self.debug
        }
        node_data.update(game_component_data)
        return node_data
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