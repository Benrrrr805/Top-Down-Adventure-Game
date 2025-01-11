from __future__ import annotations
class Node:
    """
    A generic node in a tree-like structure that supports parenting, enabling/disabling,
    and validating hierarchical relationships.
    """

    def __init__(self, name: str, top_level: bool = False):
        self.name: str = name

        # Track geometry
        self.rect_x: int = 0
        self.rect_y: int = 0

        self.children: list['Node'] = None
        self.parent: 'Node' | None = None
        self.active: bool = False

        # Whether node needs to be updated/redrawn
        self.top_level: bool = top_level
        self.need_to_update: bool = False

    # ------------------------------------------------------------------------
    #  Private Helpers for DRY
    # ------------------------------------------------------------------------
    def _indent(self, spacing: int = 0) -> str:
        """Returns a string of spaces for indentation in logs."""
        return "    " * spacing

    def _adjust_child_position(self, child: 'Node') -> None:
        """
        If child has rect_x/rect_y, shift by this node's rect_x/rect_y.
        """
        child.rect_x += self.rect_x
        child.rect_y += self.rect_y

    # ------------------------------------------------------------------------
    #  Initialization & Basic Validation
    # ------------------------------------------------------------------------

    def full_validate(self) -> bool:
        self.validate_is_node()
        self.validate_base_values()
        self.validate_relationships()
        return True
    
    def validate_relationships(self) -> bool:
        self.validate_children()
        self.validate_has_parent()
        return True
    
    def top_level_validation(self) -> bool:
        self.validate_is_top_level()
        self.validate_base_values()
        self.validate_children()
        return True

    def validate_add_child(self) -> bool:
        self.validate_is_node()
        self.validate_base_values()
        self.validate_children()
        return True

    def validate_add_parent(self) -> bool:
        self.validate_is_node()
        self.validate_base_values()
        self.validate_children()
        self.validate_has_parent()
        return True

    def validate_ready_to_link_child(parent, child: 'Node' ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        parent.validate_add_parent()
        child.validate_add_child()
        return True

    def validate_ready_to_link_children(parent, children: list['Node'] ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        parent.validate_add_parent()
        for child in children:
            child.validate_add_child()
        return True
    
    def validate_base_values(self) -> bool:
        """Validates this node's core properties."""
        if not isinstance(self.name, str):
            if self.validate_has_parent():
                self.parent.validate_base_values()
            raise ValueError(f"Node: Unknown. Failed validation. Does not have a name. Parent - {self.parent.name}")
        if not isinstance(self.top_level, bool):
            raise ValueError(f"Node: {self.name} - Failed validation. top_level must be a boolean.")
        if not isinstance(self.need_to_update, bool):
            raise ValueError(f"Node: {self.name} - Failed validation. need_to_update must be a boolean.")
        if not isinstance(self.active, bool):
            raise ValueError(f"Node: {self.name} - Failed validation. active must be a boolean.")
        if not isinstance(self.rect_x, int):
            raise ValueError(f"Node: {self.name} - Failed validation. rect_x must be an int.")
        if not isinstance(self.rect_y, int):
            raise ValueError(f"Node: {self.name} - Failed validation. rect_y must be an int.")
        
        return True
        
    def validate_is_node(self, node) -> bool:
        if not isinstance(node, Node):
            raise ValueError(f'Expected: Node. Recieved: {type(node)}')
        return True

    def validate_is_top_level(self) -> bool:
        if not self.top_level:
            raise ValueError(f"{self.name} must be a top_level")
        return True
        
    def validate_is_not_top_level(self) -> bool:
        if self.top_level:
            raise ValueError(f"{self.name} must not be a top_level")
        return True
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
        self.validate_is_node(self.parent)
        self.validate_not_self(self.parent)
        self.parent.validate_base_values()
        return True
    
    def validate_not_self(self, node: 'Node') -> bool:
        if node == self:
            raise ValueError(f"{node.name} is the same as {self.name}")
        if node.name == self.name:
            raise ValueError(f"{node.name} has the same name as {self.name}")
        return True

    def validate_is_enabled(self) -> bool:
        if not self.active:
            raise ValueError(f"Component must be enabled - {self.name}")
        return True

    def validate_is_disabled(self) -> bool:
        if self.active:
            raise ValueError(f"Component must be disabled - {self.name}")
        return True

    # ------------------------------------------------------------------------
    #  Node State: Enable / Disable
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
    def add_child(self, child: 'Node') -> None:
        """
        Add a child to this node's children list (and only that).
        Does NOT set child.parent; that is now the sole job of `add_parent`.
        """
        print(f"Adding child {child.name} to parent {self.name}")
        self._adjust_child_position(child)
        self.children.append(child)
        print(f"Child {child.name} added to parent {self.name}")

    def remove_child(self, child: 'Node') -> None:
        """
        Remove a child from this node's children list (and only that).
        Does NOT unset child.parent; that is now the sole job of `remove_parent`.
        """
        print(f"Removing child {child.name} from parent {self.name}")
        self.children.remove(child)
        print(f"Child {child.name} removed from parent {self.name}")

    def add_parent(self, parent: 'Node') -> None:
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

    def has_child(self, child: 'Node') -> bool:
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
    def link_child(parent: 'Node', child: 'Node'):
        """
        Example helper that links a parent to a child or children.
        """
        parent.validate_ready_to_link_child(child)
        parent.add_child(child)
        child.add_parent(parent)

    def link_children(parent: 'Node', children: list['Node']):
        """
        Example helper that links a parent to a child or children.
        """
        parent.validate_ready_to_link_children(children)
        for child in children:
            parent.add_child(child)
            child.add_parent(parent)

    def unlink_child(parent, child: 'Node'):
        """
        Example helper that unlinks a parent from a child or children.
        """
        parent.remove_child(child)
        child.remove_parent()

    def unlink_children(parent, children: list['Node']):
        """
        Example helper that unlinks a parent from a child or children.
        """
        for child in children:
            parent.remove_child(child)
            child.remove_parent()

    # ------------------------------------------------------------------------
    #  Additional Relationship Queries
    # ------------------------------------------------------------------------
    def get_siblings(self) -> list['Node']:
        """Returns all siblings (nodes sharing the same parent) excluding self."""
        return (
            [c for c in self.parent.children if c is not self]
            if self.parent else []
        )

    def get_ancestors(self) -> list['Node']:
        """Returns a list of this node's ancestors up the tree."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def get_descendants(self) -> list['Node']:
        """Returns a list of all descendants (children, grandchildren, etc.) of this node."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    # ------------------------------------------------------------------------
    #  Tree Traversals
    # ------------------------------------------------------------------------
    def traverse_depth_first(self) -> list['Node']:
        """Preorder DFS of this node and descendants."""
        result = [self]
        for child in self.children:
            result.extend(child.traverse_depth_first())
        return result

    def traverse_breadth_first(self) -> list['Node']:
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
    def data(self, verbose: bool = False) -> dict:
        payload = {
            "name": self.name,
            "active": self.active,
            "top_level": self.top_level,
            "has_children": bool(self.children)
        }
        if verbose:
            payload["parent"] = self.parent.name if self.parent else None
            payload["need_to_update"] = self.need_to_update
            payload["coords"] = (self.rect_x, self.rect_y)
        return payload

    def display_data(self, data: dict, recursive: bool = False, spacing: int = 0) -> None:
        indent = self._indent(spacing)
        print(f"{indent}Node data for '{data['name']}': {data}")

        if recursive and self.children:
            for child in self.children:
                child_data = child.data(verbose=True)
                child.display_data(child_data, recursive=True, spacing=spacing + 1)
