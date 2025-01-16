from game.core.node import Node

class NodeValidator:
    """
    A validator that checks consistency of a Node (and its subclasses).
    """
    @staticmethod
    def name_is_unknown(node: 'Node') -> bool:
        return not isinstance(node.name, str)
    
    @staticmethod
    def validate_base_values(node: 'Node') -> bool:
        """
        Validate base Node values, then optionally validate UI details.
        """
        if NodeValidator.name_is_unknown(node):
            if NodeValidator.validate_is_top_level(node):
                raise ValueError(f"Node: Unknown. Failed validation. Does not have a name. Node is top-level.")
            elif NodeValidator.validate_has_parent(node):
                NodeValidator.validate_base_values(node.parent)
                raise ValueError(f"Node: Unknown. Failed validation. Does not have a name. Parent - {node.parent.name}")
            else:
                raise ValueError(f"Node: Unknown. Failed validation. Does not have a name. Parent - None")
        
        if not isinstance(node.top_level, bool):
            raise ValueError(f"Node: {node.name} - Failed validation. top_level must be a boolean.")

        return True
    
    @staticmethod
    def full_validate(node: 'Node') -> bool:
        NodeValidator.validate_is_node(node)
        NodeValidator.validate_base_values(node)
        NodeValidator.validate_relationships(node)
        return True
    
    @staticmethod
    def validate_relationships(node: 'Node') -> bool:
        if NodeValidator.validate_is_not_top_level(node):
            NodeValidator.validate_has_parent(node)
        NodeValidator.validate_children(node)
        return True
    
    @staticmethod
    def top_level_validation(node: 'Node') -> bool:
        NodeValidator.validate_is_top_level(node)
        NodeValidator.validate_base_values(node)
        NodeValidator.validate_children(node)
        return True
    
    @staticmethod
    def validate_ready_to_be_added_as_parent(node: 'Node') -> bool:
        NodeValidator.validate_is_node(node)
        NodeValidator.validate_base_values(node)
        NodeValidator.validate_children(node)
        if NodeValidator.validate_is_not_top_level(node):
            NodeValidator.validate_has_parent(node)
        return True
    
    @staticmethod
    def validate_ready_to_be_added_as_child(node: 'Node') -> bool:
        if NodeValidator.validate_is_top_level(node):
            raise ValueError(f"Node must not be top-level to be added as a child. - {node.name}")
        NodeValidator.validate_is_node(node)
        NodeValidator.validate_base_values(node)
        NodeValidator.validate_children(node)
        return True

    @staticmethod
    def validate_ready_to_link_child(parent: 'Node', child: 'Node' ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        NodeValidator.validate_ready_to_be_added_as_parent(parent)
        NodeValidator.validate_ready_to_be_added_as_child(child)
        return True
    
    @staticmethod
    def validate_ready_to_link_children(parent, children: list['Node'] ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        
        NodeValidator.validate_ready_to_be_added_as_parent(parent)
        for child in children:
            NodeValidator.validate_ready_to_be_added_as_child(child)
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
            NodeValidator.validate_base_values(child)
            NodeValidator.validate_has_parent(child)
            NodeValidator.validate_not_self(node, child)
        return True
    @staticmethod
    def validate_has_parent(node: 'Node') -> bool:
        if NodeValidator.validate_is_top_level(node):
            raise ValueError(f"{node.name} does not have parent, since it is a top-level Node.")
        NodeValidator.validate_is_node(node.parent)
        NodeValidator.validate_base_values(node.parent)
        NodeValidator.validate_not_self(node, node.parent)
        return True
    
    @staticmethod
    def validate_not_self(node1: 'Node', node2: 'Node') -> bool:
        if node1 == node2:
            raise ValueError(f"{node1.name} is the same as {node2.name}")
        if node1.name == node2.name:
            raise ValueError(f"{node1.name} has the same name as {node2.name}")
        return True