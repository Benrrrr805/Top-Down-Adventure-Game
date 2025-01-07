from game.core.node import Node

class GameComponent(Node):
    """
    A base class for all game components, inheriting from Node,
    and providing shared functionality across the game:
    - Helper Function System
    - Access to 'Game' (the root) for global references
    """

    def __init__(self, name):
        super().__init__(name)
        

    def initialize(self, parent, top_level: bool = False):
        # This dictionary holds each helper function by name.
        # Each entry is: { "func": <callable>, "enabled": bool, "contexts": set_of_strings }
        self.helper_functions = {}
        super().initialize(parent, top_level)
    # ----------------------------------------------------------------------
    # Helper Function System
    # ----------------------------------------------------------------------
    def add_helper_function(self, name: str, func, contexts=None, enabled=True):
        """
        Registers a named helper function with optional auto-run contexts.
        """
        if not callable(func):
            raise ValueError(f"Helper function must be callable. - {name}")
        if contexts is None:
            contexts = {"manual"}
        elif isinstance(contexts, str):
            contexts = {contexts}
        else:
            contexts = set(contexts)

        self.helper_functions[name] = {
            "func": func,
            "enabled": enabled,
            "contexts": contexts
        }

    def enable_helper_function(self, name: str):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        self.helper_functions[name]["enabled"] = True

    def disable_helper_function(self, name: str):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        self.helper_functions[name]["enabled"] = False

    def set_helper_function_contexts(self, name: str, contexts):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        if isinstance(contexts, str):
            contexts = {contexts}
        else:
            contexts = set(contexts)
        self.helper_functions[name]["contexts"] = contexts

    def get_helper_function_contexts(self, name: str):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["contexts"]

    def get_helper_function(self, name: str):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["func"]

    def call_helper_function(self, name: str, context: str = "manual", from_helper: str = None, force: bool = False):
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        info = self.helper_functions[name]
        if not info["enabled"]:
            # If you want to allow calling even if disabled, remove or modify this check
            print(f"Helper function '{name}' is disabled. Not calling.")
            return
        if not force and context not in info["contexts"]:
            print(f"Helper function '{name}' does not handle context '{context}'. Not calling.")
            return

        # Call the function
        info["func"](self, context, from_helper)

    def run_helper_functions(self, context: str, from_helper: str = None):
        """
        Calls all helper functions whose contexts include `context` and are enabled.
        """
        for name, info in self.helper_functions.items():
            if info["enabled"] and context in info["contexts"]:
                info["func"](self, context, from_helper)

    # ----------------------------------------------------------------------
    # Getting a reference to the 'root' Game
    # ----------------------------------------------------------------------
    def get_game(self):
        """
        Traverse up the parent chain until we find the Game instance
        (the top-level GameComponent). For convenience,
        we assume the root is an instance of Game.
        """
        current = self
        while current:
            if current.top_level:
                return current
            current = current.parent
        return None
