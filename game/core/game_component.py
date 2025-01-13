import os
import json
import pygame
from pygame import font, surface
from game.settings import BLACK, RED, BLUE
from game.core.event_queue import EventQueue


class GameComponent:
    """
    A unified component class. It can be used:
      - As a simple game logic component (if graphics_enabled=False).
      - As a UI component with drawing & event handling (if graphics_enabled=True).
      - As a node in a tree-like structure. Supported: Parents, children, enabling, disabling
    """

    def __init__(
        self,
        name: str,
        top_level: bool = False,
        graphics_enabled: bool = False,
        width: int = 0,
        height: int = 0,
        x_coordinate: int = 0,
        y_coordinate: int = 0,
        image_url: str = None,
        background_color: tuple[int, int, int]=None,
        text: str = None,
        text_font =None,
        text_size: int = 24,
        text_color: tuple[int, int, int]=BLACK,
        text_position=None
    ):
        # --------------------------------------------------------------
        # Base node attributes
        # --------------------------------------------------------------
        self.children: list['GameComponent'] = None
        self.parent: 'GameComponent' = None
        self.top_level: bool = top_level

        # --------------------------------------------------------------
        # Base game-logic attributes
        # --------------------------------------------------------------
        self.game: 'GameComponent' = None
        self.event_queue: 'EventQueue' = None
        self.name: str = name
        self.active: bool = False
        self.pygame_values_set: bool = False
        self.helper_functions: dict = {}

        # --------------------------------------------------------------
        # Base debug attributes
        # --------------------------------------------------------------
        self.debug: bool = False
        self.need_to_update: bool = True

        # --------------------------------------------------------------
        # UI/Graphical mode toggles & attributes
        # --------------------------------------------------------------
        self.need_to_update: bool = False    
        self.pygame = None
        self.screen = None
        self.display = None
        self.debug_color: tuple[int, int, int] = None
        self.graphics_enabled: bool = graphics_enabled
        
        self.width: int = width
        self.height: int = height
        self.x_coordinate: int = x_coordinate
        self.y_coordinate: int = y_coordinate
        self.image_url: str = image_url
        self.background_color: tuple[int, int, int] = background_color

        self.text: str = text
        self.text_font = text_font
        self.text_size: int = text_size
        self.text_color: tuple[int, int, int] = text_color

        self.text_position: int = (text_position if text_position else (width // 2, height // 2))

        self.rect = None
        self.surface = None
        self.background_image = None

    # ----------------------------------------------------------------------
    # Helper Function System (from original GameComponent)
    # ----------------------------------------------------------------------
    def init_helper_functions(self):
        self.helper_functions: dict = {}

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
        self.game: GameComponent = game
        self.pygame = game.pygame
        self.screen = game.screen
        self.display = game.display
        self.debug: bool = game.debug
        self.debug_color: tuple[int, int, int] = game.debug_color
        self.event_queue: EventQueue = game.event_queue

        if self.graphics_enabled:
            if self.parent and isinstance(self.parent, GameComponent) and self.parent.graphics_enabled:
                # Offset coordinates by parent's coordinates
                self.x_coordinate: int = self.x_coordinate+self.parent.x_coordinate
                self.y_coordinate: int = self.y_coordinate+self.parent.y_coordinate

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

        self.pygame_values_set: bool = True

    def set_game_values_for_children(self, game=None):
        if game is None:
            game: GameComponent = self.game
        for child in self.children:
            # If a child is also a GameComponent, recursively set its values
            if isinstance(child, GameComponent):
                child.set_game_values_for_children(game)
                child.set_game_values(game)

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
    # Validation
    # ----------------------------------------------------------------------
    def validate_base_values(self):
        """
        Validate base GameComponent values, then optionally validate UI details.
        """
        if not isinstance(self.name, str):
            if self.validate_is_not_top_level() and self.validate_has_parent():
                self.parent.validate_base_values()
            raise ValueError(f"GameComponent: Unknown. Failed validation. Does not have a name. Parent - {self.parent.name}")
        if not isinstance(self.top_level, bool):
            raise ValueError(f"GameComponent: {self.name} - Failed validation. top_level must be a boolean.")
        if not isinstance(self.need_to_update, bool):
            raise ValueError(f"GameComponent: {self.name} - Failed validation. need_to_update must be a boolean.")
        if not isinstance(self.active, bool):
            raise ValueError(f"GameComponent: {self.name} - Failed validation. active must be a boolean.")

        # If not in graphics mode, skip checks
        if not self.graphics_enabled:
            return True

        # UI-specific checks
        if self.width is None or self.height is None:
            raise ValueError(f"GameComponent must have a width and height. - {self.name}")
        if self.x_coordinate is None or self.y_coordinate is None:
            raise ValueError(f"GameComponent must have x and y coordinates. - {self.name}")
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
    
    def full_validate(self) -> bool:
        self.validate_is_game_component()
        self.validate_base_values()
        self.validate_relationships()
        return True
    
    def validate_relationships(self) -> bool:
        self.validate_children()
        if self.validate_is_not_top_level():
            self.validate_has_parent()
        return True
    
    def top_level_validation(self) -> bool:
        self.validate_is_top_level()
        self.validate_base_values()
        self.validate_children()
        return True
    
    def validate_add_child(self) -> bool:
        self.validate_is_game_component()
        self.validate_base_values()
        self.validate_children()
        return True

    def validate_add_parent(self) -> bool:
        self.validate_is_game_component()
        self.validate_base_values()
        self.validate_children()
        if self.validate_is_not_top_level():
            self.validate_has_parent()
        return True
    
    def validate_ready_to_add_child(self) -> bool:
        self.validate_is_game_component()
        self.validate_base_values()
        self.validate_children()
        return True


    def validate_ready_to_link_child(parent, child: 'GameComponent' ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        parent.validate_add_parent()
        child.validate_add_child()
        return True

    def validate_ready_to_link_children(parent, children: list['GameComponent'] ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        parent.validate_add_parent()
        for child in children:
            child.validate_add_child()
        return True
        
    def validate_is_game_component(self, game_component=None) -> bool:
        if game_component is None:
            game_component = self
        if not isinstance(game_component, GameComponent):
            raise ValueError(f'Expected: GameComponent. Recieved: {type(game_component)}')
        return True

    def validate_is_top_level(self) -> bool:
        return self.top_level
        
    def validate_is_not_top_level(self) -> bool:
        return not self.top_level
    
    def validate_children(self) -> bool:
        if self.children is None:
            self.children = []
        if not isinstance(self.children, list):
            raise ValueError(f"Children must be a list. - {self.name}")
        if len(self.children) > 0:
            for child in self.children:
                child.validate_base_values()
                child.validate_has_parent()
                self.validate_not_self(child)
        return True

    def validate_has_parent(self) -> bool:
        if self.validate_is_top_level():
            raise ValueError(f"{self.name} does not have parent, since it is a top-level GameComponent.")
        self.validate_is_game_component(self.parent)
        self.validate_not_self(self.parent)
        self.parent.validate_base_values()
        return True
    
    def validate_not_self(self, game_component: 'GameComponent') -> bool:
        if game_component == self:
            raise ValueError(f"{game_component.name} is the same as {self.name}")
        if game_component.name == self.name:
            raise ValueError(f"{game_component.name} has the same name as {self.name}")
        return True

    def validate_is_enabled(self) -> bool:
        if not self.active:
            raise ValueError(f"GameComponent must be enabled - {self.name}")
        return True

    def validate_is_disabled(self) -> bool:
        if self.active:
            raise ValueError(f"GameComponent must be disabled - {self.name}")
        return True

    # ------------------------------------------------------------------------
    #  GameComponent State: Enable / Disable
    # ------------------------------------------------------------------------
    def enable(self) -> None:
        if not self.top_level:
            self.parent.need_to_update = True
        self.active = True
        self.need_to_update = True
        self.enable_children()

    def disable(self) -> None:
        if not self.top_level:
            self.parent.need_to_update = True
        self.active = False
        self.need_to_update = False
        self.disable_children()

    def enable_children(self) -> None:
        for child in self.children:
            child.enable()

    def disable_children(self) -> None:
        for child in self.children:
            child.disable()

    # ------------------------------------------------------------------------
    #  Relationship Management
    # ------------------------------------------------------------------------
    def add_child(self, child: 'GameComponent') -> None:
        """
        Add a child to this node's children list (and only that).
        Does NOT set child.parent; that is now the sole job of `add_parent`.
        """
        print(f"Adding child {child.name} to parent {self.name}")
        self.children.append(child)
        print(f"Child {child.name} added to parent {self.name}")

    def remove_child(self, child: 'GameComponent') -> None:
        """
        Remove a child from this node's children list (and only that).
        Does NOT unset child.parent; that is now the sole job of `remove_parent`.
        """
        print(f"Removing child {child.name} from parent {self.name}")
        self.children.remove(child)
        print(f"Child {child.name} removed from parent {self.name}")

    def add_parent(self, parent: 'GameComponent') -> None:
        """
        Sets this node's `parent` to the given `parent` (and only that).
        Does NOT automatically add self to parent's children. That is now the job of `add_child`.
        """
        print(f"Adding parent '{parent.name}' to child '{self.name}'")
        self.parent = parent
        print(f"Parent '{parent.name}' added to child '{self.name}'")

    def remove_parent(self) -> None:
        """
        Unsets this node's `parent`.
        Does NOT remove self from parent's children list. That is now the job of `remove_child`.
        """
        print(f"Removing parent '{self.parent.name}' from child '{self.name}'")
        self.parent = None
        print(f"Parent removed from child '{self.name}'")

    def get_child(self, name: str):
        for c in self.children:
            if c.name == name:
                return c
        return None

    def has_child(self, child: 'GameComponent') -> bool:
        """Checks if this node has a particular child (directly or recursively)."""
        if child in self.children:
            return True
        for c in self.children:
            if c.has_child(child):
                return True
        return False

    def get_parent(self):
        if not self.parent:
            raise ValueError(f"This node has no parent. - {self.name}")
        return self.parent

    # ------------------------------------------------------------------------
    #  Linking Helpers (Optional)
    # ------------------------------------------------------------------------
    def link_child(parent: 'GameComponent', child: 'GameComponent'):
        """
        Example helper that links a parent to a child or children.
        """
        parent.validate_ready_to_link_child(child)
        parent.add_child(child)
        child.add_parent(parent)

    def link_children(parent: 'GameComponent', children: list['GameComponent']):
        """
        Example helper that links a parent to a child or children.
        """
        parent.validate_ready_to_link_children(children)
        for child in children:
            parent.add_child(child)
            child.add_parent(parent)

    def unlink_child(parent, child: 'GameComponent'):
        """
        Example helper that unlinks a parent from a child or children.
        """
        parent.remove_child(child)
        child.remove_parent()

    def unlink_children(parent, children: list['GameComponent']):
        """
        Example helper that unlinks a parent from a child or children.
        """
        for child in children:
            parent.remove_child(child)
            child.remove_parent()

    # ------------------------------------------------------------------------
    #  Additional Relationship Queries
    # ------------------------------------------------------------------------
    def get_siblings(self) -> list['GameComponent']:
        """Returns all siblings (nodes sharing the same parent) excluding self."""
        return (
            [c for c in self.parent.children if c is not self]
            if self.parent else []
        )

    def get_ancestors(self) -> list['GameComponent']:
        """Returns a list of this node's ancestors up the tree."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def get_descendants(self) -> list['GameComponent']:
        """Returns a list of all descendants (children, grandchildren, etc.) of this node."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    # ------------------------------------------------------------------------
    #  Tree Traversals
    # ------------------------------------------------------------------------
    def traverse_depth_first(self) -> list['GameComponent']:
        """Preorder DFS of this node and descendants."""
        result = [self]
        for child in self.children:
            result.extend(child.traverse_depth_first())
        return result

    def traverse_breadth_first(self) -> list['GameComponent']:
        """BFS of this node and descendants."""
        queue = [self]
        result = []
        while queue:
            node = queue.pop(0)
            result.append(node)
            queue.extend(node.children)
        return result

    # ------------------------------------------------------------------------
    #  Data & Display
    # ------------------------------------------------------------------------
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
                    child_data.append(f"GameComponent child: {child.name}")
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
    