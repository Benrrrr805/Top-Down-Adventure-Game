from typing import Optional
class Node:
    def __init__(self, name: str = "Node",top_level: bool = False, children: list['Node']=None, parent: 'Node'=None):
        self.name: str = name
        if isinstance(children, list):
            self.children = children
        else:
            self.children: list[Node] = []
        self.parent: Node = parent
        self.top_level: bool = top_level
        self.pygame_values_set=False

    # ------------------------------------------------------------------------
    #  Relationship Management
    # ------------------------------------------------------------------------
    def add_child(self, child: 'Node') -> None:
        """
        Add a child to this node's children list (and only that).
        Does NOT set child.parent; that is now the sole job of `add_parent`.
        """
        print(f"Adding child {child.name} to parent {self.name}")
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
        self.parent: 'Node' = parent
        print(f"Parent '{parent.name}' added to child '{self.name}'")

    def remove_parent(self) -> None:
        """
        Unsets this node's `parent`.
        Does NOT remove self from parent's children list. That is now the job of `remove_child`.
        """
        print(f"Removing parent '{self.parent.name}' from child '{self.name}'")
        self.parent: Node = None
        print(f"Parent removed from child '{self.name}'")

    def get_child(self, name: str) -> Optional['Node']:
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

    def get_parent(self) -> 'Node':
        if not self.parent:
            raise ValueError(f"This node has no parent. - {self.name}")
        return self.parent

    # ------------------------------------------------------------------------
    #  Linking Helpers (Optional)
    # ------------------------------------------------------------------------
    def link_child(parent: 'Node', child: 'Node') -> None:
        """
        Example helper that links a parent to a child or children.
        """
        parent.add_child(child)
        child.add_parent(parent)

    def link_children(parent: 'Node', children: list['Node']) -> None:
        """
        Example helper that links a parent to a child or children.
        """
        for child in children:
            parent.add_child(child)
            child.add_parent(parent)

    def unlink_child(parent, child: 'Node') -> None:
        """
        Example helper that unlinks a parent from a child or children.
        """
        parent.remove_child(child)
        child.remove_parent()

    def unlink_children(parent, children: list['Node']) -> None:
        """
        Example helper that unlinks a parent from a child or children.
        """
        for child in children:
            parent.remove_child(child)
            child.remove_parent()

    def set_values_in_self(self, values: dict):
        for key, value in values.items():
            self[key] = value

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
        ancestors: list['Node'] = []
        current: 'Node' = self.parent
        while current:
            ancestors.append(current)
            current: 'Node' = current.parent
        return ancestors

    def get_descendants(self) -> list['Node']:
        """Returns a list of all descendants (children, grandchildren, etc.) of this node."""
        descendants: list['Node'] = []
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
