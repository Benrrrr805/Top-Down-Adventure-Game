class Node:
    """
    A generic node in a tree-like structure that supports parenting, enabling/disabling,
    and validating hierarchical relationships.
    """

    def __init__(self, name: str, top_level: bool = False):
        self.name: str = name
        self.children: list['Node'] = []
        self.parent: 'Node' | None = None
        self.active: bool = True
        self.top_level: bool = top_level
        self.initialized: bool = False

        # Track geometry
        self.rect_x: int = 0
        self.rect_y: int = 0

        # Whether node needs to be updated/redrawn
        self.need_to_update: bool = False

    # ------------------------------------------------------------------------
    #  Private Helpers for DRY
    # ------------------------------------------------------------------------
    def _indent(self, spacing: int = 0) -> str:
        """Returns a string of spaces for indentation in logs."""
        return "    " * spacing

    def _mark_parent_needs_update(self, spacing: int = 0) -> None:
        """
        If this node has a parent and the parent's `need_to_update` is False,
        sets it to True and logs it; otherwise logs that it's already set.
        """
        if self.parent:
            indent = self._indent(spacing)
            if not self.parent.need_to_update:
                self.parent.need_to_update = True
                print(f"{indent}Parent {self.parent.name} now needs to update")
            else:
                print(f"{indent}Parent {self.parent.name} already needs to update")

    def _log_enable_disable(self, spacing: int, action: str) -> None:
        """
        Unified logging for enabling/disabling this node.
        
        :param spacing: indentation
        :param action: 'Enabling' or 'Disabling'
        """
        indent = self._indent(spacing)
        print(f"{indent}{action} {self.name}")

    def _verify_node_or_ui_component(self, child) -> None:
        """
        Ensures the child is either a Node or UIComponent, raising ValueError if not.
        """
        if not isinstance(child, Node) and not isinstance(child, UIComponent):
            raise ValueError(f"Child must be a Node or UIComponent. - {child.name}: child of {self.name}")

    def _adjust_child_position(self, child) -> None:
        """
        If child has rect_x/rect_y, shift by this node's rect_x/rect_y.
        """
        if hasattr(child, 'rect_x') and hasattr(child, 'rect_y'):
            child.rect_x += self.rect_x
            child.rect_y += self.rect_y

    def _remove_child_from_list(self, child) -> None:
        """
        Removes a child from self.children if present.
        """
        if child in self.children:
            self.children.remove(child)
        else:
            raise ValueError(f"Child {child.name} is not in {self.name}'s children")

    # ------------------------------------------------------------------------
    #  Initialization & Basic Validation
    # ------------------------------------------------------------------------
    def initialize(self) -> None:
        if self.initialized:
            raise ValueError(f"{self.name} already initialized.")
        self.initialized = True
        self.validate()

    def validate(self) -> bool:
        """Validates this node's core properties."""
        if not self.top_level and not isinstance(self.parent, Node):
            raise ValueError(f"Parent must be a Node. - {self.name}")
        if self.top_level and isinstance(self.parent, Node):
            raise ValueError(f"Top-level node must not have a parent. - {self.name}")
        if not isinstance(self.children, list):
            raise ValueError(f"Children must be a list. - {self.name}")
        if not isinstance(self.active, bool):
            raise ValueError(f"Active must be a boolean. - {self.name}")
        return True

    def validate_no_cyclical_parents(self) -> bool:
        """Ensures no cyclical reference in parent chain."""
        visited = set()
        current = self
        while current:
            if current in visited:
                raise ValueError(f"Cyclical reference detected at '{current.name}'.")
            visited.add(current)
            current = current.parent
        return True

    # ------------------------------------------------------------------------
    #  Relationship Validations
    # ------------------------------------------------------------------------
    def validate_has_parent(self) -> bool:
        if self.parent is None and not self.top_level:
            raise ValueError(f"Parent must not be None, or node must be top-level. - {self.name}")

        if self.parent is not None:
            if not isinstance(self.parent, Node):
                raise ValueError(f"Parent must be a Node. - {self.name}")
            if not self.parent.initialized:
                raise ValueError(f"Parent must be initialized. - {self.name}")
            if not self.parent.active:
                raise ValueError(f"Parent must be enabled. - {self.name}")
            if not self.parent.name:
                raise ValueError(f"Parent must have a name. - {self.name}")
            if self.parent.name == self.name:
                raise ValueError(f"Parent and child cannot have the same name. - {self.name}")
            if not self.parent.children:
                raise ValueError(f"Parent must have children. - {self.name}")
            if not self.parent.has_child(self):
                raise ValueError(f"Parent must have this child. - {self.name}")
            if self.parent.get_child(self.name) is None:
                raise ValueError(f"Parent must have this child. - {self.name}")
            if self.parent.get_child(self.name) != self:
                raise ValueError(f"Parent must have this child. - {self.name}")
        return True

    def validate_is_enabled(self) -> bool:
        if not self.initialized:
            raise ValueError(f"Component must be initialized - {self.name}")
        if not self.active:
            raise ValueError(f"Component must be enabled - {self.name}")
        return True

    def validate_is_disabled(self) -> bool:
        if not self.initialized:
            raise ValueError(f"Component must be initialized - {self.name}")
        if self.active:
            raise ValueError(f"Component must be disabled - {self.name}")
        return True

    def validate_hierarchy(self) -> bool:
        """
        Recursively validates the entire sub-tree, including cyclical references,
        so you can ensure each node is well-formed.
        """
        self.validate()
        self.validate_no_cyclical_parents()
        for child in self.children:
            child.validate_hierarchy()
        return True

    # ------------------------------------------------------------------------
    #  Node State: Enable / Disable
    # ------------------------------------------------------------------------
    def enable(self, spacing: int = 0) -> None:
        self.validate_is_disabled()
        self.validate_has_parent()

        self._log_enable_disable(spacing, "Enabling")
        self.active = True
        indent = self._indent(spacing)
        
        # Need to update self?
        if not self.need_to_update:
            self.need_to_update = True
            print(f"{indent}    Enabled {self.name}")
        else:
            print(f"{indent}    {self.name} already needs to update")

        # Enable children
        if self.children:
            print(f"{indent}    Enabling children of {self.name}")
            self.enable_children(spacing + 1)
        else:
            print(f"{indent}    No children to enable")

        # Mark parent
        self._mark_parent_needs_update(spacing)

    def disable(self, spacing: int = 0) -> None:
        self.validate_enabled()
        self._log_enable_disable(spacing, "Disabling")
        indent = self._indent(spacing)

        node_data = self.data()
        self.display_data(node_data, recursive=True)

        # Disable children
        if self.children:
            print(f"{indent}    Disabling children of {self.name}")
            self.disable_children(spacing + 1)
        else:
            print(f"{indent}    No children to disable")

        # Mark parent
        self._mark_parent_needs_update(spacing)

        # Toggle flags
        if self.active:
            self.active = False
            print(f"{indent}    Disabled {self.name}")
        else:
            print(f"{indent}    {self.name} already disabled")

        if self.need_to_update:
            self.need_to_update = False
            print(f"{indent}    Cleared {self.name}'s need_to_update flag")
        else:
            print(f"{indent}    {self.name}'s need_to_update flag already cleared")

    def enable_children(self, spacing: int = 0) -> None:
        indent = self._indent(spacing)
        # Check that we can enable
        if not self.active:
            raise ValueError(f"Component must be enabled before enabling children. - {self.name}")
        if not self.children:
            raise ValueError(f"Component has no children. - {self.name}")

        print(f"{indent}Enabling children of parent: {self.name}")
        for child in self.children:
            if not child.name:
                raise ValueError(f"Child must have a name. - some child of {self.name}")
            if not child.initialized:
                raise ValueError(f"Child '{child.name}' must be initialized. - child of {self.name}")
            if child.active:
                raise ValueError(f"Child '{child.name}' must be disabled before enabling. - child of {self.name}")
            if child.parent != self:
                raise ValueError(f"Child '{child.name}' must have this node as parent. - child of {self.name}")

            print(f"{indent}    Enabling child: {child.name}")
            child.enable(spacing + 1)

        print(f"{indent}All children of {self.name} are now enabled")

    def disable_children(self, spacing: int = 0) -> None:
        indent = self._indent(spacing)
        # Check that we can disable
        if not self.active:
            raise ValueError(f"Component must be enabled before disabling children. - {self.name}")
        if not self.children:
            raise ValueError(f"Component has no children. - {self.name}")

        print(f"{indent}Disabling children of parent: {self.name}")
        for child in self.children:
            if not child.name:
                raise ValueError(f"Child must have a name. - some child of {self.name}")
            if not child.initialized:
                raise ValueError(f"Child '{child.name}' must be initialized. - child of {self.name}")
            if not child.active:
                raise ValueError(f"Child '{child.name}' must be enabled before disabling the parent. - child of {self.name}")
            if child.parent != self:
                raise ValueError(f"Child '{child.name}' must have this node as parent. - child of {self.name}")

            print(f"{indent}    Disabling child: {child.name}")
            child.disable(spacing + 1)

        print(f"{indent}All children of {self.name} are now disabled")

    # ------------------------------------------------------------------------
    #  Relationship Management
    # ------------------------------------------------------------------------
    def add_child(self, child) -> None:
        """
        Add a child to this node's children list (and only that).
        Does NOT set child.parent; that is now the sole job of `add_parent`.
        """
        self._verify_node_or_ui_component(child)
        child.validate()
        child.validate_no_cyclical_parents()

        print(f"Adding child {child.name} to parent {self.name}")
        self._adjust_child_position(child)

        # Only add to self.children
        self.children.append(child)

        # Validate again after re-parenting, to ensure no newly created cycle
        child.validate_no_cyclical_parents()
        print(f"Child {child.name} added to parent {self.name}")

    def remove_child(self, child) -> None:
        """
        Remove a child from this node's children list (and only that).
        Does NOT unset child.parent; that is now the sole job of `remove_parent`.
        """
        self._verify_node_or_ui_component(child)
        print(f"Removing child {child.name} from parent {self.name}")
        self._remove_child_from_list(child)
        print(f"Child {child.name} removed from parent {self.name}")

    def get_child(self, name: str):
        indent = self._indent()
        print(f"{indent}Searching for child '{name}' in parent '{self.name}'")
        for c in self.children:
            if c.name == name:
                print(f"{indent}Found child '{name}' in parent '{self.name}'")
                return c
        print(f"{indent}No child named '{name}' found in parent '{self.name}'")
        return None

    def has_child(self, child) -> bool:
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

    def add_parent(self, parent: 'Node') -> None:
        """
        Sets this node's `parent` to the given `parent` (and only that).
        Does NOT automatically add self to parent's children. That is now the job of `add_child`.
        """
        print(f"Adding parent '{parent.name}' to child '{self.name}'")
        self.parent = parent
        self.validate_no_cyclical_parents()
        print(f"Parent '{parent.name}' added to child '{self.name}'")

    def remove_parent(self) -> None:
        """
        Unsets this node's `parent`.
        Does NOT remove self from parent's children list. That is now the job of `remove_child`.
        """
        if self.parent:
            print(f"Removing parent '{self.parent.name}' from child '{self.name}'")
            self.parent = None
            print(f"Parent removed from child '{self.name}'")

    # ------------------------------------------------------------------------
    #  Linking Helpers (Optional)
    # ------------------------------------------------------------------------
    def link_parent_child(self, parent: 'Node', child: 'Node'):
        """
        Example helper that adds the parent to the child AND the child to the parent,
        so references remain in sync if you still prefer that usage in some places.
        """
        child.add_parent(parent)
        parent.add_child(child)

    def unlink_parent_child(self, parent: 'Node', child: 'Node'):
        """
        Example helper that removes the parent from the child AND the child from the parent.
        """
        child.remove_parent()
        parent.remove_child(child)

    def link(self, parent, child=None, children=None):
        """
        Example helper that links a parent to a child or children.
        """
        if child:
            self.link_parent_child(parent, child)
        if children:
            for child in children:
                self.link_parent_child(parent, child)
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
            "initialized": self.initialized,
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


class UIComponent(Node):
    """Example subclass to show that `_verify_node_or_ui_component` allows UIComponent too."""
    pass
