# import pygame
from game.core.game_resources import GameResources
from game.settings import BLACK, RED
import os
import json

class UIComponent:
    def __init__(self, name, width, height, x_coordinate, y_coordinate, 
                 background_image=None, background_color=None,  
                 text=None, text_font=None, text_size=24, text_color=BLACK, text_position=None, 
                 active=True, need_to_update=True, debug_color=BLACK, 
                 parent=None, children=None, helper_function=None, helper_function_enabled=True):
        self.pygame = GameResources.pygame
        self.screen = GameResources.screen
        self.display = GameResources.display
        self.debug = GameResources.debug

        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.height = height
        self.width = width
        self.name = name
        self.background_color = background_color
        self.rect = self.pygame.Rect(self.x_coordinate, self.y_coordinate, self.width, self.height)
        self.surface = self.pygame.Surface((self.width, self.height), self.pygame.SRCALPHA)
        self.debug_color = debug_color
        self.need_to_update = need_to_update
        if children is None:
            children = []
        self.children = children
        self.parent = parent
        self.active = active
        self.image_url = background_image

        self.text = text
        self.text_size = text_size
        self.text_font = self.pygame.font.Font(text_font, self.text_size) if text_font else self.pygame.font.SysFont(None, self.text_size)
        self.text_color = text_color
        self.text_position = text_position if text_position else (self.width // 2, self.height // 2)

        if background_image is not None and not os.path.exists(background_image):
            raise ValueError("Background image does not exist")
        if background_image is not None:
            self.background_image_url = background_image
            self.background_image = self.pygame.image.load(background_image).convert()
            self.background_image = self.pygame.transform.scale(self.background_image, (self.width, self.height))
        else:
            self.background_image = None
            self.background_image_url = None
        
        self.helper_function = helper_function
        self.helper_function_enabled = helper_function_enabled

        self.validate()

    def add_helper_function(self, helper_function):
        self.helper_function = helper_function

    def run_helper_function(self):
        if self.helper_function is not None and self.active and self.helper_function_enabled:
            self.helper_function(self)

    def enable_helper_function(self):
        self.helper_function_enabled = True

    def disable_helper_function(self):
        self.helper_function_enabled = False

    def data(self, recursive=False, as_json=False, visited=None):
        """
        Return either the data dictionary itself (default)
        or a JSON string (if as_json=True).

        :param recursive: If True, include child data (unless already visited).
        :param as_json: If True, return a JSON string of the data.
        :param visited: Used internally to track which containers have been visited.
        :return: dict or str
        """
        # If we haven't yet created a visited set, do so now.
        if visited is None:
            visited = set()

        # If we've already visited this container, return the "hidden" message.
        if id(self) in visited:
            if self is None:
                return "Hidden so that limited recursion does not occur - None"
            return f"Hidden so that limited recursion does not occur - {self.name}"

        # Mark this container as visited.
        visited.add(id(self))

        # Determine the parent data
        if self.name == "main_container":
            parent_data = "Top-level container - no parent"
        elif self.parent is None:
            parent_data = "No Parent"
        else:
            if recursive:
                # Recursively fetch the parent's data (without re-visiting)
                parent_data = self.parent.data(recursive=False, as_json=False, visited=visited)
            else:
                # Show the parent's name or a placeholder
                parent_data = getattr(self.parent, "name", "No Parent")

        # Gather children data if recursive=True, otherwise show a placeholder if children exist
        if recursive:
            children_data = []
            for child in self.children:
                child_info = child.data(recursive=True, as_json=False, visited=visited)
                children_data.append(child_info)
        else:
            if len(self.children) > 0:
                children_data = f"Hidden so that limited recursion does not occur - {len(self.children)} child{'ren' if (len(self.children) > 1) else ''}: {[child.name for child in self.children]}"
            else:
                children_data = []

        data_dict = {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "background_image": self.background_image_url,
            "background_color": self.background_color,
            "text": self.text,
            "text_size": self.text_size,
            "text_color": self.text_color,
            "text_position": self.text_position,
            "active": self.active,
            "need_to_update": self.need_to_update,
            "debug_color": self.debug_color,
            "parent": parent_data,
            "children": children_data,
        }

        # Return JSON if requested
        if as_json:
            return json.dumps(data_dict, indent=4)

        # Otherwise, return the dictionary
        return data_dict

    def display_data(self, data, recursive=False, indent_level=0):
        """
        Pretty-print the data dictionary (or placeholder text) to the console.
        :param data: A dictionary (or string) generated from self.data(...)
        :param recursive: If True, display child data recursively.
        :param indent_level: Helps control indentation for nested calls.
        """

        # If data is a string (the "Hidden..." placeholder), print and return early.
        if isinstance(data, str):
            indent = "    " * indent_level
            print(f"{indent}{data}")
            return

        indent = "    " * indent_level
        if indent_level == 0:
            print(f"{indent}Displaying data for: {data['name']}")

        for key, value in data.items():
            # Handle children
            if key == "children":
                if isinstance(value, list) and len(value) > 0:
                    print(f"{indent}  {key}:")
                    for child_dict in value:
                        self.display_data(child_dict, recursive, indent_level + 1)
                elif isinstance(value, str):
                    # "Hidden so that limited recursion does not occur"
                    print(f"{indent}  {key}: {value}")
                else:
                    # Probably an empty list
                    print(f"{indent}  {key}: []")

            # Handle parent
            elif key == "parent":
                if isinstance(value, dict):
                    print(f"{indent}  {key}:")
                    self.display_data(value, recursive, indent_level + 1)
                else:
                    print(f"{indent}  {key}: {value}")

            else:
                print(f"{indent}  {key}: {value}")

        print()

    def validate(self):
        if not self.name:
            raise ValueError("Component must have a name")
        if self.width is None or self.height is None:
            raise ValueError("Component must have a width and height")
        if self.x_coordinate is None or self.y_coordinate is None:
            raise ValueError("Component must have x and y coordinates")
        if self.debug_color is not None and not isinstance(self.debug_color, tuple):
            raise ValueError("Debug color must be a tuple")
        if self.parent is not None and not isinstance(self.parent, UIComponent):
            raise ValueError("Parent must be a UIComponent")
        if self.children is not None and not isinstance(self.children, list):
            raise ValueError("Children must be a list")
        if self.active is not None and not isinstance(self.active, bool):
            raise ValueError("Active must be a boolean")
        if self.need_to_update is not None and not isinstance(self.need_to_update, bool):
            raise ValueError("Need to update must be a boolean")
        if self.debug is not None and not isinstance(self.debug, bool):
            raise ValueError("Debug must be a boolean")
        if self.text is not None and not isinstance(self.text, str):
            raise ValueError("Text must be a string")   
        if self.text_size is not None and not isinstance(self.text_size, int):
            raise ValueError("Text size must be an integer")
        if self.text_position is not None and not isinstance(self.text_position, tuple):
            raise ValueError("Text position must be a tuple")
        if self.text_color is not None and not isinstance(self.text_color, tuple):
            raise ValueError("Text color must be a tuple")
        return True

    def validate_disabled(self):
        # validates that the component is disabled prior to enabling
        if self.active:
            raise ValueError("Component must be disabled before enabling")
        if self.parent is None and self.name != "main_container":
            raise ValueError("Component must have a parent")
        if self.parent.name is None:
            raise ValueError("Parent must have a name")
        if not self.parent.active:
            raise ValueError("Parent must be enabled before enabling child")
        if self.parent.name == self.name:
            raise ValueError("Parent and child cannot have the same name")
        return True
        
    def validate_enabled(self):
        # validates that the component is enabled prior to disabling
        if not self.active:
            raise ValueError("Component must be enabled")
        if self.parent is None and self.name != "main_container":
            raise ValueError("Component must have a parent before disabling")
        if not self.parent.active:
            raise ValueError("Parent must be enabled before disabling child")
        if self.parent.name is None:
            raise ValueError("Parent must have a name")
        if self.parent.name == self.name:
            raise ValueError("Parent and child cannot have the same name")
        return True
        
    def validate_enabled_children(self):
        # validates that the component is enabled prior to enabling children
        if not self.active:
            raise ValueError("Component must be enabled before enabling children")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Component has no children")
        for child in self.children:
            if not child.name:
                raise ValueError("Child must have a name")
            if not child.active:
                raise ValueError("Child must be disabled before enabling")
            if not child.parent:
                raise ValueError("Child must have a parent")
            if child.parent.name != self.name:
                raise ValueError("Child must have the same parent as the parent")
        return True
            
    def validate_disabled_children(self):
        # validates that the component is enabled prior to diabling children
        if not self.active:
            raise ValueError("Component must be enabled before disabling children")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Component has no children")
        for child in self.children:
            if not child.name:
                raise ValueError("Child must have a name")
            if child.active:
                raise ValueError("Child must be disabled before disabling parent")
            if not child.parent:
                raise ValueError("Child must have a parent")
            if child.parent.name != self.name:
                print(f'child.parent.name: {child.parent.name} - self.name: {self.name}')
                raise ValueError("Child must have the same parent as the parent")
        return True

    def enable(self, spacing=0):
        self.validate_disabled()
        print(f"{spacing * '     '}Enabling {self.name}")
        self.active = True
        if not self.need_to_update:
            self.need_to_update = True
            print(f"{spacing * '     '}     Enabled {self.name}")
        else:
            print(f"{spacing * '     '}     {self.name} already needs to update")
        if len(self.children) > 0:
            print(f"{spacing * '     '}     Enabling children")
            self.enable_children(spacing+1)
        else:
            print(f"{spacing * '     '}     No children to enable")
        if not self.parent.need_to_update:
            self.parent.need_to_update = True
            print(f"{spacing * '     '}     Parent: {self.parent.name} needs to update")
        else:
            print(f"{spacing * '     '}     Parent: {self.parent.name} already needs to update")

    def disable(self, spacing=0):
        validated = self.validate_enabled()    
        print(f"validated {self.name}: {validated}")
        print(f"{spacing * '     '}Disabling {self.name}")
        data = self.data(True)
        self.display_data(data, recursive=True)
        if len(self.children) > 0:
            print(f"{spacing * '     '}     Disabling children")
            self.disable_children(spacing+1)
        else:
            print(f"{spacing * '     '}     No children to disable")
        if not self.parent.need_to_update:
            self.parent.need_to_update = True
            print(f"{spacing * '     '}     Parent: {self.parent.name} needs to update")
        else:
            print(f"{spacing * '     '}     Parent: {self.parent.name} already needs to update")
        if self.active:
            self.active = False
            print(f"{spacing * '     '}     Disabled {self.name}")
        else:
            print(f"{spacing * '     '}     {self.name} already disabled")
        if self.need_to_update:
            self.need_to_update = False
            print(f"{spacing * '     '}     Disabled {self.name}'s need to update")
        else:
            print(f"{spacing * '     '}     already disabled {self.name}'s needs to update")

    def enable_children(self,spacing=0):
        self.validate_enabled_children()
        print(f"Enabling children of parent: {self.name}")
        for child in self.children:
            name = child.name
            print(f"     Enabling child: {name} of parent: {self.name}")
            child.enable(spacing)
            print(f"          Enabled child: {name} of parent: {self.name}")
        print(f"     Enabled children of parent: {self.name}")

    def disable_children(self, spacing=0):
        print(f"Disabling children of parent: {self.name}")
        validated = self.validate_disabled_children()
        print(f"validated {self.name}: {validated}")
        for child in self.children:
            name = child.name
            print(f"     Disabling child: {name} of parent: {self.name}")
            child.disable(spacing)
            print(f"          Disabled child: {name} of parent: {self.name}")
        print(f"     Disabled children of parent: {self.name}")
    
    def add_child(self, child):
        child.validate()
        if not isinstance(child, UIComponent):
            raise ValueError("Child must be a UIComponent")
        print(f"Adding child: {child.name} to parent: {self.name}")
        child.rect.x += self.rect.x
        child.rect.y += self.rect.y
        if self.children is None:
            self.children = []
        self.children.append(child)
        print(f"     Added child: {child.name} to parent: {self.name}")

    def remove_child(self, child):
        if not isinstance(child, UIComponent):
            raise ValueError("Child must be a UIComponent")
        print(f"Removing child: {child.name} from parent: {self.name}")
        child_name = child.name
        self.children.remove(child)
        print(f"     Removed child: {child_name} from parent: {self.name}")

    def get_child(self, name):
        print(f"Getting child: {name} from parent: {self.name}")
        # Returns the first child with the given name
        if isinstance(name, UIComponent):
            name = name.name
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        for child in self.children:
            if child.name == name:
                print(f"     Found child: {name} in parent: {self.name}")
                return child
        print(f"     Child: {name} not found in parent: {self.name}")
        return None
    
    def has_child(self, child):
        print(f"Checking if parent: {self.name} has child: {child.name}")
        if not isinstance(child, UIComponent):
            raise ValueError("Child must be a UIComponent")
        for c in self.children:
            if c.name == child.name:
                if len(c.children) > 0:
                    return c.has_child(child)
                print(f"     Parent: {self.name} has child: {child.name}")
                return True
        print(f"     Parent: {self.name} does not have child: {child.name}")
        return False
    
    def get_parent(self):
        print(f"Getting parent of child: {self.name}")
        if self.parent is None:
            raise ValueError("Parent must not be None")
        print(f"     Parent of child: {self.name} is: {self.parent.name}")
        return self.parent
    
    def add_parent(self, parent):
        print(f"Adding parent: {parent.name} to child: {self.name}")
        parent.validate()
        self.parent = parent
        print(f"     Added parent: {parent.name} to child: {self.name}")

    def remove_parent(self):
        print(f"Removing parent: {self.parent.name} from child: {self.name}")
        parent_name = self.parent.name
        self.parent = None
        print(f"     Removed parent: {parent_name} from child: {self.name}")

    def get_rect(self):
        return self.rect

    def in_rect(self, coordinates):
        return self.rect.collidepoint(coordinates)

    def hovering(self):
        hover = self.in_rect(self.pygame.mouse.get_pos())
        return hover
    
    def clicked(self):
        if not self.hovering():
            return False
        for child in self.children:
            if child.active and child.hovering():
                return False
        for event in self.pygame.event.get():
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                return True

    def render_text(self):
        if self.text:
            text_surface = self.text_font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            if self.text_position == "center":
                text_rect.center = (self.width // 2, self.height // 2)
            else:
                text_rect.topleft = self.text_position
            self.surface.blit(text_surface, text_rect)

    def handle_events_(self):
        for child in self.children:
            if child.active:
                child.handle_events()

    def handle_events(self):
        if self.active:
            return self.handle_events_()
        return None

    def update_(self):
        if self.debug and self.debug_color is not None:
            if self.hovering() and self.debug_color == BLACK:
                self.need_to_update = True
                self.debug_color = RED
            elif not self.hovering() and self.debug_color == RED:
                self.need_to_update = True
                self.debug_color = BLACK
        for child in self.children:
            if child.active:
                child.update()
                if child.need_to_update:
                    self.need_to_update = True
        self.run_helper_function()

    def update(self):
        if self.active:
            return self.update_()
        return None

    def draw_(self):
        if not self.active or self.width == 0 or self.height == 0:
            return None

        if self.active:
            if self.need_to_update:
                if self.background_image is not None:
                    self.surface.blit(self.background_image, (0, 0))
                elif self.background_color is not None:
                    self.surface.fill(self.background_color)
                else:
                    self.surface.fill((0, 0, 0, 0))

        # Render text
        self.render_text()

        # Redraw children selectively
        for child in self.children:
            
            if self.need_to_update or child.need_to_update:
                
                child_surface = child.draw()
                if child_surface is not None:
                    x = child.get_rect().x - self.rect.x
                    y = child.get_rect().y - self.rect.y
                    self.surface.blit(child_surface,(x, y))
                # Reset the child's update flag
                child.need_to_update = False

        # Draw the debug border if necessary
       
        if self.debug and self.debug_color is not None and self.need_to_update:
            self.pygame.draw.rect(self.surface, self.debug_color, (0, 0, self.width, self.height), 5)
            
        # Reset the UI Component's need to update flag
        if self.need_to_update:
            self.need_to_update = False
           
        return self.surface

    def draw(self):
        if self.active:
            return self.draw_()
        return None
