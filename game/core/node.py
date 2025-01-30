from typing import Optional
import json
class Node:
    instances = {}
    def __init__(self, name: str = "Node",top_level: bool = False, children: list['Node']=None, parent: 'Node'=None):
        self.name: str = name
        self.top_level: bool = top_level
        self.attributes = {}
        Node.instances[name] = self

        # If there are children, add them to this node and set self as their parent.
        if isinstance(children, list):
            self.children = children
            for child in self.children:
                child.add_parent(self)
        else:
            self.children: list[Node] = []

        # If a parent is provided, set it and add self to parent's children.
        if isinstance(parent, Node):
            self.parent = parent
            parent.add_child(self)
        else:
            self.parent: Node = parent

    def __str__(self):
        # Pretty-print the dictionary with 4-space indentation
        return json.dumps(self.to_dict(), indent=4)
    
    def to_dict(self):
        return {
            "name": self.name,
            "top_level": self.top_level,
            "attributes": self.attributes,
            "children": [c.to_dict() for c in self.children if isinstance(c, Node)],
            "parent": self.parent.name if self.parent and isinstance(self.parent, Node) else None
        }
    # ------------------------------------------------------------------------
    #  Relationship Management
    # ------------------------------------------------------------------------
    def add_child(self, child: 'Node') -> None:
        """
        Add a child to this node's children list (and only that).
        Does NOT set child.parent; that is now the sole job of `add_parent`.
        """
        self.children.append(child)

    def remove_child(self, child: 'Node') -> None:
        """
        Remove a child from this node's children list (and only that).
        Does NOT unset child.parent; that is now the sole job of `remove_parent`.
        """
        self.children.remove(child)

    def add_parent(self, parent: 'Node') -> None:
        """
        Sets this node's `parent` to the given `parent` (and only that).
        Does NOT automatically add self to parent's children. That is now the job of `add_child`.
        """
        self.parent: 'Node' = parent

    def remove_parent(self) -> None:
        """
        Unsets this node's `parent`.
        Does NOT remove self from parent's children list. That is now the job of `remove_child`.
        """
        self.parent: Node = None

    def get_node(self, name: str) -> Optional['Node']:
        if name in Node.instances:
            return Node.instances[name]
        return None

    def get_child(self, name: str) -> Optional['Node']:
        for c in self.children:
            if c.name == name:
                return c
        return None

    def get_parent(self) -> 'Node':
        return self.parent
    
    def has_child(self, child: 'Node') -> bool:
        """Checks if this node has a particular child (directly or recursively)."""
        if child in self.children:
            return True
        for c in self.children:
            if c.has_child(child):
                return True
        return False


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

    def link_parent(child: 'Node', parent: 'Node') -> None:
        """
        Example helper that links a child to a parent.
        """
        child.add_parent(parent)
        parent.add_child(child)

    def unlink_parent(child: 'Node') -> None:
        """
        Example helper that unlinks a child from a parent.
        """

        child.parent.remove_child(child)
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

# ------------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------------
    @staticmethod
    def name_is_unknown(node: 'Node') -> bool:
        return not node.name or not isinstance(node.name, str) or len(node.name) == 0
    
    @staticmethod
    def validate_base_values(node: 'Node') -> bool:
        """
        Validate base Node values, then optionally validate UI details.
        """
        if Node.name_is_unknown(node):
            raise ValueError(f"Node: Unknown. Failed validation. name must be a non-empty string.")
        if not isinstance(node.top_level, bool):
            raise ValueError(f"Node: {node.name} - Failed validation. top_level must be a boolean.")

        return True
    
    @staticmethod
    def full_validate(node: 'Node') -> bool:
        Node.validate_is_node(node)
        Node.validate_base_values(node)
        Node.validate_relationships(node)
        return True
    
    @staticmethod
    def validate_relationships(node: 'Node') -> bool:
        if Node.validate_is_not_top_level(node):
            Node.validate_has_parent(node)
        Node.validate_children(node)
        return True
    
    @staticmethod
    def top_level_validation(node: 'Node') -> bool:
        if Node.validate_is_top_level(node):
            Node.validate_base_values(node)
            Node.validate_children(node)
        else:
            raise ValueError(f"Node must be top-level to be validated as top-level. - {node.name}")
        return True
    
    @staticmethod
    def validate_ready_to_be_added_as_parent(node: 'Node') -> bool:
        Node.validate_is_node(node)
        Node.validate_base_values(node)
        Node.validate_children(node)
        if Node.validate_is_not_top_level(node):
            Node.validate_has_parent(node)
        return True
    
    @staticmethod
    def validate_ready_to_be_added_as_child(node: 'Node') -> bool:
        if Node.validate_is_top_level(node):
            raise ValueError(f"Node must not be top-level to be added as a child. - {node.name}")
        Node.validate_is_node(node)
        Node.validate_base_values(node)
        Node.validate_children(node)
        return True

    @staticmethod
    def validate_ready_to_link_child(parent: 'Node', child: 'Node' ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        Node.validate_ready_to_be_added_as_parent(parent)
        Node.validate_ready_to_be_added_as_child(child)
        return True
    
    @staticmethod
    def validate_ready_to_link_children(parent, children: list['Node'] ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        Node.validate_ready_to_be_added_as_parent(parent)
        for child in children:
            Node.validate_ready_to_be_added_as_child(child)
        return True
    
    @staticmethod  
    def validate_is_node(node: 'Node' = None) -> bool:
        """
        Validates that the given object is a Node.
        """
        if not isinstance(node, Node):
            raise ValueError(f'Expected: Node. Recieved: {type(node).__name__}')
        return True
    
    @staticmethod
    def validate_is_top_level(node: 'Node') -> bool:
        return node.top_level
    
    @staticmethod 
    def validate_is_not_top_level(node: 'Node') -> bool:
        return not node.top_level
    
    @staticmethod
    def validate_children(node: 'Node') -> bool:
        if not isinstance(node.children, list):
            raise ValueError(f"Children must be a list. - {node.name}")
        
        for child in node.children:
            Node.validate_is_node(child)
            Node.validate_base_values(child)
            Node.validate_has_parent(child)
            Node.validate_not_self(node, child)
        return True
    @staticmethod
    def validate_has_parent(node: 'Node') -> bool:
        if Node.validate_is_top_level(node):
            raise ValueError(f"{node.name} should not have parent, since it is a top-level Node.")
        if isinstance(node.parent, Node):
            Node.validate_base_values(node.parent)
            Node.validate_not_self(node, node.parent)
        else:
            raise ValueError(f"{node.name} does not have a parent.")
        return True
    
    @staticmethod
    def validate_not_self(node1: 'Node', node2: 'Node') -> bool:
        if node1 == node2:
            raise ValueError(f"{node1.name} is the same as {node2.name}")
        if node1.name == node2.name:
            raise ValueError(f"{node1.name} has the same name as {node2.name}")
        return True