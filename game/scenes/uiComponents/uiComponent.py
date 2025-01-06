# import pygame
from game.core.game_resources import GameResources
from game.settings import BLACK, RED
import os
import json
import os
import json
from game.core.node import Node

import os
import json

# Suppose these come from your game environment

class UIComponent(Node):
    """
    UIComponent is a specialized Node that supports graphical rendering,
    event handling, and text rendering via pygame. It also supports
    multiple, named helper functions that can be automatically or manually called.
    """

    def __init__(
        self,
        name: str,
        width: int,
        height: int,
        x_coordinate: int,
        y_coordinate: int,
        image_url: str = None,
        background_color=None,
        text: str = None,
        text_font=None,
        text_size: int = 24,
        text_color=BLACK,
        text_position=None
    ):
        """
        Inherits from Node, which manages parent, children, enable/disable, etc.
        """
        super().__init__(name=name, top_level=False)
        self.width = width
        self.height = height
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        self.image_url = image_url
        self.background_color = background_color

        # Text settings
        self.text = text
        self.text_font = text_font
        self.text_size = text_size
        self.text_color = text_color
        # Default text position to center if not specified
        self.text_position = text_position if text_position else (width // 2, height // 2)

        # Debug flags
        self.debug_color = None
        self.debug = False

        # pygame references
        self.pygame = None
        self.screen = None
        self.display = None
        self.event_queue = None
        self.rect = None
        self.surface = None

        # This dictionary holds each helper function by name.
        # Each entry is: { "func": <callable>, "enabled": bool, "contexts": set_of_strings }
        self.helper_functions = {}

    # ----------------------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------------------
    def initialize(self):
        if self.initialized:
            raise ValueError("UIComponent is already initialized.")
        super().initialize()  # Node-level init + validate()

        # from game.core.game_resources import GameResources
        self.pygame = GameResources.pygame
        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug
        self.event_queue = GameResources.event_queue

        # Set coordinates relative to parent if parent exists
        if self.parent:
            self.x_coordinate += self.parent.x_coordinate
            self.y_coordinate += self.parent.y_coordinate

        # Create pygame rect & surface
        self.rect = self.pygame.Rect(self.x_coordinate, self.y_coordinate, self.width, self.height)
        self.surface = self.pygame.Surface((self.width, self.height), self.pygame.SRCALPHA)

        # Load or create the font
        if self.text_font:
            self.text_font = self.pygame.font.Font(self.text_font, self.text_size)
        else:
            self.text_font = self.pygame.font.SysFont(None, self.text_size)

        # Attempt to load background image if provided
        if self.image_url is not None:
            if not os.path.exists(self.image_url):
                raise ValueError(f"Background image does not exist: {self.image_url}")
            self.background_image = self.pygame.image.load(self.image_url).convert_alpha()
            self.background_image = self.pygame.transform.scale(self.background_image, (self.width, self.height))
        else:
            self.background_image = None

        self.debug_color = BLACK
        if not self.need_to_update:
            self.need_to_update = True
        self.active = True

        print(f"Initialized UIComponent: {self.name}")

    # ----------------------------------------------------------------------
    # Validation
    # ----------------------------------------------------------------------
    def validate(self):
        """
        Node-level validations plus UI-specific checks.
        """
        super().validate()  # Node validations

        # UI-specific checks
        if self.width is None or self.height is None:
            raise ValueError("UIComponent must have a width and height.")
        if self.x_coordinate is None or self.y_coordinate is None:
            raise ValueError("UIComponent must have x and y coordinates.")
        # self.coordinates are within parents coordinates if parent exists TODO: check this
        if self.debug_color is not None and not isinstance(self.debug_color, tuple):
            raise ValueError("Debug color must be a tuple.")
        if self.debug_color is not None and len(self.debug_color) != 3 and len(self.debug_color) != 4:
            raise ValueError("Debug color must be an RGB tuple.")
        if self.text is not None and not isinstance(self.text, str):
            raise ValueError("Text must be a string.")
        if self.text_size is not None and not isinstance(self.text_size, int):
            raise ValueError("Text size must be an integer.")
        if self.text_position is not None and not isinstance(self.text_position, tuple):
            raise ValueError("Text position must be a tuple.")
        if self.text_position is not None and len(self.text_position) != 2:
            raise ValueError("Text position must be an (x, y) tuple.")
        if self.text_color is not None and not isinstance(self.text_color, tuple):
            raise ValueError("Text color must be a tuple.")
        if self.text_color is not None and len(self.text_color) != 3 and len(self.text_color) != 4:
            raise ValueError("Text color must be an RGB or RGBA tuple.")

        return True

    # ----------------------------------------------------------------------
    # Helper Function System
    # ----------------------------------------------------------------------
    def add_helper_function(
        self,
        name: str,
        func,
        contexts=None,
        enabled=True
    ):
        """
        Registers a named helper function with optional auto-run contexts.
        
        :param name: Unique string name for the helper function.
        :param func: A callable with signature func(self, context, from_helper=None).
        :param contexts: A string, list of strings, or set of strings indicating
                         when this helper function should auto-run. e.g. {"update", "draw", "handle_events"}.
                         If None, defaults to {"manual"} only.
        :param enabled: Whether the function is initially enabled.
        """
        if not callable(func):
            raise ValueError("Helper function must be callable.")
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
        """
        Updates the set of contexts for a helper function.
        """
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        if isinstance(contexts, str):
            contexts = {contexts}
        else:
            contexts = set(contexts)
        self.helper_functions[name]["contexts"] = contexts

    def get_helper_function_contexts(self, name: str):
        """
        Returns the set of contexts for the given helper function.
        """
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["contexts"]

    def get_helper_function(self, name: str):
        """
        Retrieve the helper function callable itself (if you want to do something advanced).
        """
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        return self.helper_functions[name]["func"]

    def call_helper_function(
        self,
        name: str,
        context: str = "manual",
        from_helper: str = None,
        force: bool = False
    ):
        """
        Call one helper function by name.
        
        :param context: Which context to simulate. By default "manual".
        :param from_helper: If this call originates from another helper function, pass its name here.
        :param force: If True, ignore the function's context set. 
                      (Still won't call if the function is disabled—adapt as needed.)
        """
        if name not in self.helper_functions:
            raise ValueError(f"No helper function named '{name}'.")
        info = self.helper_functions[name]
        if not info["enabled"]:
            # If you want to allow calling even if disabled, remove this check:
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
        
        :param context: Something like "update", "draw", "handle_events", "manual".
        :param from_helper: If this is triggered from some other named helper function.
        """
        for name, info in self.helper_functions.items():
            if info["enabled"] and context in info["contexts"]:
                info["func"](self, context, from_helper)

    # ----------------------------------------------------------------------
    # Event Handling
    # ----------------------------------------------------------------------
    def in_rect(self, coordinates):
        if not self.rect:
            return False
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        if not self.initialized or not self.pygame:
            return False
        return self.in_rect(self.pygame.mouse.get_pos())

    def clicked(self):
        if not self.hovering():
            return False
        for child in self.children:
            if child.active and isinstance(child, UIComponent) and child.hovering():
                return False
        for event in self.pygame.event.get():
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def handle_events_(self):
        """
        Internally handle events (for active components).
        Then run any helper functions that respond to "handle_events" context.
        """
        # Let children handle events first
        for child in self.children:
            if child.active and isinstance(child, UIComponent):
                child.handle_events()

        # Now run all enabled helper functions that respond to "handle_events".
        self.run_helper_functions("handle_events")

    def handle_events(self):
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before handling events.")
        if self.active:
            self.handle_events_()

    # ----------------------------------------------------------------------
    # Updating
    # ----------------------------------------------------------------------
    def update_(self):
        """
        Internal update: checks debug hover, updates children, runs helper functions for "update".
        """
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before updating.")

        # Debug hover color
        if self.debug and self.debug_color is not None:
            if self.hovering() and self.debug_color == BLACK:
                self.need_to_update = True
                self.debug_color = RED
            elif not self.hovering() and self.debug_color == RED:
                self.need_to_update = True
                self.debug_color = BLACK

        # Update children
        for child in self.children:
            if child.active and isinstance(child, UIComponent):
                child.update()
                if child.need_to_update:
                    self.need_to_update = True

        # Run all enabled helper functions in "update" context
        self.run_helper_functions("update")

    def update(self):
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before updating.")
        if self.active:
            self.update_()

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------
    def render_text(self):
        if not self.text or not self.initialized:
            return
        text_surface = self.text_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        if self.text_position == "center":
            text_rect.center = (self.width // 2, self.height // 2)
        else:
            text_rect.topleft = self.text_position
        self.surface.blit(text_surface, text_rect)

    def draw_(self):
        """
        Internal draw:
          - Draw background / image
          - Render text
          - Draw debug border if needed
          - Draw children
          - Run helper functions for "draw"
        """
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before drawing.")
        if not self.active or self.width == 0 or self.height == 0:
            return None

        if not self.need_to_update:
            return self.surface

        print(f"Drawing UIComponent: {self.name}")
        # Redraws every element above this one in the hierarchy TODO: optimize

        # If we need to update background
        if self.background_image is not None:
            self.surface.blit(self.background_image, (0, 0))
        elif self.background_color is not None:
            self.surface.fill(self.background_color)
        else:
            self.surface.fill((0, 0, 0, 0))

        # Render text
        self.render_text()

        # Debug border
        if self.debug and self.debug_color:
            self.pygame.draw.rect(
                self.surface, self.debug_color,
                (0, 0, self.width, self.height), 5
            )

        # Run all enabled helper functions in "draw" context
        self.run_helper_functions("draw")

        # # # Draw children
        for child in self.children:
            if isinstance(child, UIComponent) and (self.need_to_update or child.need_to_update):
                child_surface = child.draw()
                # explanation: child.x_coordinate and child.y_coordinate are relative to the parent
                if child_surface is not None:
                    x = child.x_coordinate - self.x_coordinate
                    y = child.y_coordinate - self.y_coordinate
                    self.surface.blit(child_surface, (x, y))
                child.need_to_update = False

        self.need_to_update = False

        return self.surface

    def draw(self):
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before drawing.")
        if not self.active:
            raise ValueError("UIComponent must be enabled before drawing.")
        return self.draw_()

    # ----------------------------------------------------------------------
    # Data & Display
    # ----------------------------------------------------------------------
    def data(self, recursive=False, as_json=False, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return f"Hidden so that limited recursion does not occur - {self.name}"
        visited.add(id(self))

        base_data = {
            "name": self.name,
            "active": self.active,
            "initialized": self.initialized,
            "need_to_update": self.need_to_update,
            "parent": self.parent.name if self.parent else None,
            "width": self.width,
            "height": self.height,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "image_url": self.image_url,
            "background_color": self.background_color,
            "text": self.text,
            "text_size": self.text_size,
            "text_color": self.text_color,
            "text_position": self.text_position,
            "debug_color": self.debug_color,
            "helper_functions": {
                fname: {
                    "enabled": fdata["enabled"],
                    "contexts": list(fdata["contexts"])
                }
                for fname, fdata in self.helper_functions.items()
            },
        }

        if recursive:
            child_data = []
            for child in self.children:
                if isinstance(child, UIComponent):
                    child_data.append(child.data(True, as_json=False, visited=visited))
                else:
                    child_data.append(f"Node child: {child.name}")
            base_data["children"] = child_data
        else:
            base_data["children"] = (
                f"{len(self.children)} child{('ren' if len(self.children) > 1 else '')}" if self.children else "No children"
            )

        if as_json:
            return json.dumps(base_data, indent=4)
        return base_data

    def display_data(self, data, recursive=False, indent_level=0):
        indent = "    " * indent_level
        if isinstance(data, str):
            print(f"{indent}{data}")
            return

        if indent_level == 0:
            print(f"{indent}Displaying data for UIComponent: {data['name']}")

        for key, value in data.items():
            if key == "children" and recursive and isinstance(value, list):
                print(f"{indent}  {key}:")
                for child_dict in value:
                    self.display_data(child_dict, True, indent_level + 1)
            elif key == "helper_functions":
                print(f"{indent}  {key}:")
                for fn_name, fn_info in value.items():
                    contexts_str = ", ".join(fn_info["contexts"])
                    print(f"{indent}    {fn_name} -> enabled={fn_info['enabled']}, contexts=[{contexts_str}]")
            else:
                print(f"{indent}  {key}: {value}")
        print()

    def get_rect(self):
        return self.rect
