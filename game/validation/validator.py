from game.validation.node_validator import NodeValidator
from game.validation.game_component_validator import GameComponentValidator
from game.validation.visual_component_validator import VisualComponentValidator
from game.core.node import Node
from game.core.game_component import GameComponent
from game.core.visual_component import VisualComponent

class Validator:
    def __init__(self):
        self.node_validator: 'NodeValidator' = NodeValidator()
        self.game_component_validator = GameComponentValidator()
        self.visual_component_validator = VisualComponentValidator()

    @staticmethod
    def validate_base_values(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates the base values of a Node, GameComponent, or VisualComponent.
        """
        if isinstance(node, Node):
            return NodeValidator.validate_base_values(node)
        if isinstance(node, GameComponent):
            return GameComponentValidator.validate_base_values(node)
        if isinstance(node, VisualComponent):
            return VisualComponentValidator.validate_base_values(node)

    @staticmethod
    def validate_full_validate(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates the full values of a Node, GameComponent, or VisualComponent.
        """
        if isinstance(node, Node):
            return NodeValidator.full_validate(node)
        if isinstance(node, GameComponent):
            return GameComponentValidator.full_validate(node)
        if isinstance(node, VisualComponent):
            return VisualComponentValidator.full_validate(node)
    
    @staticmethod
    def validate_relationships(node: 'Node' | 'GameComponent' | VisualComponent) -> bool:
        """
        Validates the relationships of a Node, GameComponent, or VisualComponent.
        """
        return NodeValidator.validate_relationships(node)
    
    @staticmethod
    def top_level_validation(node: 'Node' | 'GameComponent' | VisualComponent) -> bool:
        """
        Top level validation for a Node, GameComponent, or VisualComponent.
        """
        return NodeValidator.top_level_validation(node)
    
    @staticmethod
    def validate_ready_to_be_added_as_parent(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that this node is ready to be added as a parent.
        """
        return NodeValidator.validate_ready_to_be_added_as_parent(node)
    
    @staticmethod
    def validate_ready_to_be_added_as_child(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that this node is ready to be added as a child
        """
        return NodeValidator.validate_ready_to_be_added_as_child(node)

    @staticmethod
    def validate_ready_to_link_child(parent: 'Node' | 'GameComponent' | 'VisualComponent', child: 'Node' | 'GameComponent' | 'VisualComponent' ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        return NodeValidator.validate_ready_to_link_child(parent, child)
    
    @staticmethod
    def validate_ready_to_link_children(parent: 'Node' | 'GameComponent' | 'VisualComponent', children: list['Node' | 'GameComponent' | 'VisualComponent'] ) -> bool:
        """Validates that this node is ready to be linked to a parent."""
        return NodeValidator.validate_ready_to_link_children(parent, children)
    
    @staticmethod  
    def validate_is_node(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given object is a Node.
        """
        return NodeValidator.validate_is_node(node)
    
    @staticmethod
    def validate_is_game_component(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given object is a GameComponent.
        """
        return GameComponentValidator.validate_is_game_component(node)
    
    @staticmethod
    def validate_is_visual_component(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given object is a VisualComponent.
        """
        return VisualComponentValidator.validate_is_visual_component(node)
    
    @staticmethod
    def validate_is_top_level(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given object is a top level node.
        """
        return NodeValidator.validate_is_top_level(node)
    
    @staticmethod 
    def validate_is_not_top_level(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given object is not a top level node.
        """
        return NodeValidator.validate_is_not_top_level(node)
    
    @staticmethod
    def validate_children(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates the children of the given node.
        """
        return NodeValidator.validate_children(node)
    @staticmethod
    def validate_has_parent(node: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given node has a parent.
        """
        return NodeValidator.validate_has_parent(node)
    
    @staticmethod
    def validate_not_self(node1: 'Node' | 'GameComponent' | 'VisualComponent', node2: 'Node' | 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given nodes are not the same.
        """
        return NodeValidator.validate_not_self(node1, node2)
    
    @staticmethod
    def validate_is_enabled(game_component: 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given GameComponent or VisualComponent is enabled.
        """
        return GameComponentValidator.validate_is_enabled(game_component)

    @staticmethod
    def validate_is_disabled(game_component: 'GameComponent' | 'VisualComponent') -> bool:
        """
        Validates that the given GameComponent or VisualComponent is disabled.
        """
        return GameComponentValidator.validate_is_disabled(game_component)