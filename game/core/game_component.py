import os
import json
from game.core.node import Node
from game.settings import BLACK, RED, BLUE


class GameComponent(Node):
    """
    A unified component class. It can be used:
      - As a simple game logic component (if graphics_enabled=False).
      - As a UI component with drawing & event handling (if graphics_enabled=True).

    Inherits from Node, so it can be nested in a hierarchy.
    """

    def __init__(
        self,
        name: str,
        top_level: bool = False,
        # Whether or not this component should support graphical/UI logic:
        graphics_enabled: bool = False,

        # ------------------------------------------------------------------
        # Optional UI/graphical parameters (if graphics_enabled=True)
        # ------------------------------------------------------------------
        width: int = 0,
        height: int = 0,
        x_coordinate: int = 0,
        y_coordinate: int = 0,
        image_url: str = None,
        background_color=None,
        text: str = None,
        text_font=None,
        text_size: int = 24,
        text_color=BLACK,
        text_position=None
    ):
        super().__init__(name, top_level)
        self.init_helper_functions()

        # --------------------------------------------------------------
        # Base "GameComponent" attributes (helper functions, etc.)
        # --------------------------------------------------------------
        # Potentially add any additional needed base attributes here:
        self.game = None
        self.pygame = None
        self.screen = None
        self.display = None
        self.event_queue = None

        # For debugging in both logical and UI contexts
        self.debug = False
        self.debug_color = None
        self.need_to_update = True  # For UI logic to decide whether to redraw

        # --------------------------------------------------------------
        # UI/Graphical mode toggles & attributes
        # --------------------------------------------------------------
        self.graphics_enabled = graphics_enabled
        if not self.graphics_enabled:
            # Non-UI defaults (these won't be used):
            self.width = 0
            self.height = 0
            self.x_coordinate = 0
            self.y_coordinate = 0
            self.image_url = None
            self.background_color = None
            self.text = None
            self.text_font = None
            self.text_size = None
            self.text_color = None
            self.text_position = None
            self.surface = None
            self.rect = None
            self.background_image = None

        else:
            # Store the UI parameters
            self.width = width
            self.height = height
            self.x_coordinate = x_coordinate
            self.y_coordinate = y_coordinate
            self.image_url = image_url
            self.background_color = background_color

            self.text = text
            self.text_font = text_font
            self.text_size = text_size
            self.text_color = text_color

            # If not specified, center text by default
            self.text_position = (
                text_position if text_position else (width // 2, height // 2)
            )

            self.rect = None
            self.surface = None
            self.background_image = None

        # Keep a reference to track if/when pygame stuff is set:
        self.pygame_values_set = False

    # ----------------------------------------------------------------------
    # Helper Function System (from original GameComponent)
    # ----------------------------------------------------------------------
    def init_helper_functions(self):
        self.helper_functions = {}

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
            print(f"Helper function '{name}' is disabled. Not calling.")
            return
        if not force and context not in info["contexts"]:
            print(f"Helper function '{name}' does not handle context '{context}'. Not calling.")
            return

        info["func"](self, context, from_helper)

    def run_helper_functions(self, context: str, from_helper: str = None):
        """
        Calls all helper functions whose contexts include `context` and are enabled.
        """
        for name, info in self.helper_functions.items():
            if info["enabled"] and context in info["contexts"]:
                info["func"](self, context, from_helper)

    # ----------------------------------------------------------------------
    # Linking the parent/children and setting game (pygame) references
    # ----------------------------------------------------------------------
    def set_game_values(self, game: 'GameComponent'):
        """
        Set references needed to access Pygame or global game resources.
        For UI usage, also create surfaces/rect if graphics_enabled=True.
        """
        print(f"Setting game values for {self.name}")
        self.game = game
        self.pygame = game.pygame
        self.screen = game.screen
        self.display = game.display
        self.debug = game.debug
        self.debug_color = game.debug_color
        self.event_queue = game.event_queue

        if self.graphics_enabled:
            if self.parent and isinstance(self.parent, GameComponent) and self.parent.graphics_enabled:
                # Offset coordinates by parent's coordinates
                self.x_coordinate += self.parent.x_coordinate
                self.y_coordinate += self.parent.y_coordinate

            # Create pygame Rect & Surface
            self.rect = self.pygame.Rect(self.x_coordinate, self.y_coordinate,
                                         self.width, self.height)
            self.surface = self.pygame.Surface((self.width, self.height), self.pygame.SRCALPHA)

            # Load or create the font
            if self.text_font:
                self.text_font = self.pygame.font.Font(self.text_font, self.text_size)
            else:
                # If None, use default system font
                self.text_font = self.pygame.font.SysFont(None, self.text_size)

            # Attempt to load background image if provided
            if self.image_url is not None:
                if not os.path.exists(self.image_url):
                    raise ValueError(f"Background image does not exist: {self.image_url} - {self.name}")
                img = self.pygame.image.load(self.image_url).convert_alpha()
                self.background_image = self.pygame.transform.scale(img, (self.width, self.height))

        self.pygame_values_set = True

    def set_game_values_for_children(self, game=None):
        if game is None:
            game = self.game
        for child in self.children:
            # If a child is also a GameComponent, recursively set its values
            if isinstance(child, GameComponent):
                child.set_game_values_for_children(game)
                child.set_game_values(game)

    # ----------------------------------------------------------------------
    # Validation
    # ----------------------------------------------------------------------
    def validate_base_values(self):
        """
        Validate base Node-level values, then optionally validate UI details.
        """
        super().validate_base_values()  # From Node, if it has anything to check

        # If not in graphics mode, skip checks
        if not self.graphics_enabled:
            return True

        # UI-specific checks
        if self.width is None or self.height is None:
            raise ValueError(f"UIComponent must have a width and height. - {self.name}")
        if self.x_coordinate is None or self.y_coordinate is None:
            raise ValueError(f"UIComponent must have x and y coordinates. - {self.name}")
        if self.debug_color is not None and not isinstance(self.debug_color, tuple):
            raise ValueError(f"Debug color must be a tuple. - {self.name}")
        if self.debug_color is not None and len(self.debug_color) not in (3, 4):
            raise ValueError(f"Debug color must be an RGB or RGBA tuple. - {self.name}")
        if self.text is not None and not isinstance(self.text, str):
            raise ValueError(f"Text must be a string. - {self.name}")
        if self.text_size is not None and not isinstance(self.text_size, int):
            raise ValueError(f"Text size must be an integer. - {self.name}")
        if self.text_position is not None and not isinstance(self.text_position, tuple):
            raise ValueError(f"Text position must be a tuple. - {self.name}")
        if self.text_position is not None and len(self.text_position) != 2:
            raise ValueError(f"Text position must be an (x, y) tuple. - {self.name}")
        if self.text_color is not None and not isinstance(self.text_color, tuple):
            raise ValueError(f"Text color must be a tuple. - {self.name}")
        if self.text_color is not None and len(self.text_color) not in (3, 4):
            raise ValueError(f"Text color must be an RGB or RGBA tuple. - {self.name}")

        return True

    # ----------------------------------------------------------------------
    # UI-Related Utility Functions (wrapped with graphics_enabled checks)
    # ----------------------------------------------------------------------
    def in_rect(self, coordinates):
        if not self.graphics_enabled or not self.rect:
            return False
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        """
        Return True if the mouse is over this component's rect.
        """
        if not self.graphics_enabled:
            return False
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before checking for hover. - {self.name}")
        mouse_pos = self.pygame.mouse.get_pos()
        return self.in_rect(mouse_pos)

    def clicked(self):
        """
        Return True if the mouse button is down *within* this component
        and no child component is also hovered.
        """
        if not self.graphics_enabled:
            return False
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before checking for click. - {self.name}")
        if not self.hovering():
            return False

        # If any child is also hovered, consider that the click belongs to the child
        for child in self.children:
            if child.active and isinstance(child, GameComponent) and child.graphics_enabled and child.hovering():
                return False

        if self.hovering() and self.event_queue and self.event_queue.has_event('MOUSEBUTTONDOWN'):
            print(f"Clicked on UIComponent: {self.name}")
            self.event_queue.remove_event('MOUSEBUTTONDOWN')
            return True

        return False

    # ----------------------------------------------------------------------
    # Event Handling
    # ----------------------------------------------------------------------
    def handle_events_(self):
        """
        Internal method to handle events recursively in children,
        then call any helper functions for 'handle_events' context.
        """
        # Let children handle events first
        for child in self.children:
            if child.active and isinstance(child, GameComponent):
                child.handle_events()

        # Then run any helpers
        self.run_helper_functions("handle_events")

    def handle_events(self):
        """
        Public method to handle events - raises error if inactive.
        """
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before handling events. - {self.name}")
        self.handle_events_()

    # ----------------------------------------------------------------------
    # Updating
    # ----------------------------------------------------------------------
    def update_(self):
        """
        Internal update logic: handle debugging color changes, update children,
        run update helpers, etc.
        """
        # Hover-based debug color change
        if self.graphics_enabled and self.debug and self.debug_color is not None:
            hovering = self.hovering()
            # Example: toggles between BLUE and RED
            if hovering and self.debug_color == BLUE:
                self.need_to_update = True
                self.debug_color = RED
            elif not hovering and self.debug_color == RED:
                self.need_to_update = True
                self.debug_color = BLUE

        # Update children
        for child in self.children:
            if child.active and isinstance(child, GameComponent):
                child.update()
                if getattr(child, 'need_to_update', False):
                    self.need_to_update = True

        # Run helper functions
        self.run_helper_functions("update")

    def update(self):
        """
        Public update method - raises error if inactive.
        """
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before updating. - {self.name}")
        self.update_()

    # ----------------------------------------------------------------------
    # Rendering (Only if graphics_enabled)
    # ----------------------------------------------------------------------
    def render_text(self):
        if not self.graphics_enabled:
            return
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before rendering text. - {self.name}")
        if not self.text:
            return

        text_surface = self.text_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()

        # If text_position == "center", override with center
        if self.text_position == "center":
            text_rect.center = (self.width // 2, self.height // 2)
        else:
            text_rect.topleft = self.text_position

        self.surface.blit(text_surface, text_rect)

    def draw_(self):
        if not self.graphics_enabled:
            return None
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before drawing. - {self.name}")
        if self.width == 0 or self.height == 0:
            return None

        # If we haven't changed anything, return the existing surface
        if not self.need_to_update:
            return self.surface

        print(f"Drawing UIComponent: {self.name}")

        # Draw background image or color
        if self.background_image is not None:
            self.surface.blit(self.background_image, (0, 0))
        elif self.background_color is not None:
            self.surface.fill(self.background_color)
        else:
            # Transparent background
            self.surface.fill((0, 0, 0, 0))

        # Render text if any
        self.render_text()

        # Possibly draw a debug border
        print(f"Debug: {self.debug}, Debug Color: {self.debug_color}")
        if self.debug and self.debug_color:
            self.pygame.draw.rect(
                self.surface, self.debug_color, (0, 0, self.width, self.height), 5
            )

        # Run helper functions for "draw" context
        self.run_helper_functions("draw")

        # Draw children surfaces:
        for child in self.children:
            if isinstance(child, GameComponent) and child.graphics_enabled:
                child_surface = child.draw()
                if child_surface is not None:
                    x = child.x_coordinate - self.x_coordinate
                    y = child.y_coordinate - self.y_coordinate
                    self.surface.blit(child_surface, (x, y))
                child.need_to_update = False

        self.need_to_update = False
        if not isinstance(self.surface, self.pygame.Surface):
            raise ValueError(f"UIComponent draw_() must return a pygame.Surface. - {self.name}")

        return self.surface

    def draw(self):
        if not self.graphics_enabled:
            return None
        if not self.active:
            raise ValueError(f"UIComponent must be enabled before drawing. - {self.name}")
        return self.draw_()

    def get_rect(self):
        return self.rect if self.graphics_enabled else None

    # ----------------------------------------------------------------------
    # Data & Display
    # ----------------------------------------------------------------------
    def display_(self):
        """
        Print or log the data for debugging (recursively).
        """
        data = self.data(True)
        self.display_data(data, recursive=True)

    def data(self, recursive=False, as_json=False, visited=None):
        if visited is None:
            visited = set()
        if id(self) in visited:
            return f"Hidden to prevent infinite recursion - {self.name}"
        visited.add(id(self))

        base_data = {
            "name": self.name,
            "active": self.active,
            "need_to_update": self.need_to_update,
            "parent": self.parent.name if self.parent else None,

            # UI-related (null or 0 if graphics_enabled=False)
            "graphics_enabled": self.graphics_enabled,
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

            # Helper functions
            "helper_functions": {
                fname: {
                    "enabled": fdata["enabled"],
                    "contexts": list(fdata["contexts"])
                }
                for fname, fdata in self.helper_functions.items()
            },
            "surface": str(self.surface),
            "game": str(self.game),
        }

        if recursive:
            child_data = []
            for child in self.children:
                if isinstance(child, GameComponent):
                    child_data.append(child.data(True, as_json=False, visited=visited))
                else:
                    child_data.append(f"Node child: {child.name}")
            base_data["children"] = child_data
        else:
            count = len(self.children)
            base_data["children"] = (
                f"{count} child{'ren' if count > 1 else ''}" if count else "No children"
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
            print(f"{indent}Displaying data for component: {data['name']}")

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
