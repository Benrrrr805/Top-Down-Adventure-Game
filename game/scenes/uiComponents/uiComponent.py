# game/scenes/uiComponents/uiComponent.py

import os
import json
from game.core.game_component import GameComponent  # the new base class
from game.settings import BLACK, RED

class UIComponent(GameComponent):
    """
    Specialized GameComponent that supports graphical rendering,
    event handling, text rendering via pygame, etc.
    Inherits from GameComponent so it also has:
      - parent/child relationships,
      - can access the root Game via self.get_game().
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
        Constructor for UIComponent.
        :param name: Unique identifier of this component
        :param width: Pixel width of component
        :param height: Pixel height of component
        :param x_coordinate: X coordinate (relative to parent if parent is also a UIComponent)
        :param y_coordinate: Y coordinate (relative to parent if parent is also a UIComponent)
        :param image_url: Path to background image (if any)
        :param background_color: Tuple (R, G, B, [A]) or None
        :param text: Text to display (optional)
        :param text_font: Path to a TTF file or None
        :param text_size: Font size for the text (default 24)
        :param text_color: (R, G, B, [A]) for text color
        :param text_position: (x, y) offset for text, or None to center
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
        self.text_position = (
            text_position if text_position else (width // 2, height // 2)
        )

        # Debug flags
        self.debug_color = None
        self.debug = False

        # pygame references set during initialize()
        self.pygame = None
        self.screen = None
        self.display = None
        self.event_queue = None

        # Pygame Rect & Surface
        self.rect = None
        self.surface = None

        # For optional background image
        self.background_image = None

    # ----------------------------------------------------------------------
    # Initialization
    # ----------------------------------------------------------------------
    def initialize(self):
        super().initialize()  # Node-level init + validate()

        # Access the root game
        game = self.get_game()
        if not game:
            raise ValueError(
                "UIComponent requires a parent chain that eventually links to Game."
            )

        # Store references from game
        self.pygame = game.pygame
        self.screen = game.screen
        self.display = game.display
        self.debug = game.debug
        self.event_queue = game.event_queue

        # If the parent is also a UIComponent, offset the coordinates
        if self.parent and isinstance(self.parent, UIComponent):
            self.x_coordinate += self.parent.x_coordinate
            self.y_coordinate += self.parent.y_coordinate

        # Create pygame rect & surface
        self.rect = self.pygame.Rect(
            self.x_coordinate, self.y_coordinate, self.width, self.height
        )
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
            self.background_image = self.pygame.transform.scale(
                self.background_image, (self.width, self.height)
            )

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
        if self.debug_color is not None and not isinstance(self.debug_color, tuple):
            raise ValueError("Debug color must be a tuple.")
        if (
            self.debug_color is not None
            and len(self.debug_color) not in (3, 4)
        ):
            raise ValueError("Debug color must be an RGB or RGBA tuple.")
        if self.text is not None and not isinstance(self.text, str):
            raise ValueError("Text must be a string.")
        if self.text_size is not None and not isinstance(self.text_size, int):
            raise ValueError("Text size must be an integer.")
        if self.text_position is not None and not isinstance(self.text_position, tuple):
            raise ValueError("Text position must be a tuple.")
        if (
            self.text_position is not None
            and len(self.text_position) != 2
        ):
            raise ValueError("Text position must be an (x, y) tuple.")
        if self.text_color is not None and not isinstance(self.text_color, tuple):
            raise ValueError("Text color must be a tuple.")
        if (
            self.text_color is not None
            and len(self.text_color) not in (3, 4)
        ):
            raise ValueError("Text color must be an RGB or RGBA tuple.")

        return True

    # ----------------------------------------------------------------------
    # Event Handling
    # ----------------------------------------------------------------------
    def in_rect(self, coordinates):
        if not self.rect:
            return False
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        # Make sure we have pygame references
        if not self.initialized or not self.pygame:
            return False
        return self.in_rect(self.pygame.mouse.get_pos())

    def clicked(self):
        """
        Return True if the mouse button is down *within* this component
        and no child component is also hovered.
        """
        if not self.hovering():
            return False

        # If any child is also hovered, consider that the click belongs to the child
        for child in self.children:
            if child.active and isinstance(child, UIComponent) and child.hovering():
                return False

        if self.event_queue.has_event(self.pygame.MOUSEBUTTONDOWN):
            return True
        
        return False

    def handle_events_(self):
        """
        Internally handle events, then run any relevant helper functions
        (which are part of GameComponent).
        """
        # Let children handle events first
        for child in self.children:
            if child.active and isinstance(child, UIComponent):
                child.handle_events()

        # Run any helper functions for "handle_events"
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

        # If text_position == "center", override with center
        if self.text_position == "center":
            text_rect.center = (self.width // 2, self.height // 2)
        else:
            text_rect.topleft = self.text_position

        self.surface.blit(text_surface, text_rect)

    def draw_(self):
        if not self.initialized:
            raise ValueError("UIComponent must be initialized before drawing.")
        if not self.active or self.width == 0 or self.height == 0:
            return None

        if not self.need_to_update:
            # No re-draw needed, return existing surface
            return self.surface

        print(f"Drawing UIComponent: {self.name}")

        # Draw background image or fill color
        if self.background_image is not None:
            self.surface.blit(self.background_image, (0, 0))
        elif self.background_color is not None:
            self.surface.fill(self.background_color)
        else:
            # Transparent background
            self.surface.fill((0, 0, 0, 0))

        # Render text if any
        self.render_text()

        # Debug border
        if self.debug and self.debug_color:
            self.pygame.draw.rect(
                self.surface,
                self.debug_color,
                (0, 0, self.width, self.height),
                5
            )

        # Run helper functions for "draw" context
        self.run_helper_functions("draw")

        # Draw children
        for child in self.children:
            if isinstance(child, UIComponent) and (self.need_to_update or child.need_to_update):
                child_surface = child.draw()
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
            # helper_functions are now in GameComponent
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
