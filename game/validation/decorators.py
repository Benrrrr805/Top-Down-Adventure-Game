class ValidationDecorators:
    @staticmethod
    def validate_base_values():
        """
        Decorator that calls NodeValidator.validate_base_values,
        GameComponentValidator.validate_base_values, or
        VisualComponentValidator.validate_base_values depending on the instance type.
        """
        from game.validation.node_validator import NodeValidator
        from game.validation.game_component_validator import GameComponentValidator
        from game.validation.visual_component_validator import VisualComponentValidator
        from game.core.node import Node
        from game.core.game_component import GameComponent
        from game.core.visual_component import VisualComponent

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                valid = False
                if isinstance(node, Node):
                    valid = NodeValidator.validate_base_values(node)
                elif isinstance(node, GameComponent):
                    valid = GameComponentValidator.validate_base_values(node)
                elif isinstance(node, VisualComponent):
                    valid = VisualComponentValidator.validate_base_values(node)

                if not valid:
                    raise ValueError("Validation failed in validate_base_values.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_full_validate():
        """
        Decorator that calls NodeValidator.full_validate,
        GameComponentValidator.full_validate, or
        VisualComponentValidator.full_validate depending on the instance type.
        """
        from game.validation.node_validator import NodeValidator
        from game.validation.game_component_validator import GameComponentValidator
        from game.validation.visual_component_validator import VisualComponentValidator
        from game.core.node import Node
        from game.core.game_component import GameComponent
        from game.core.visual_component import VisualComponent

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                valid = False
                if isinstance(node, Node):
                    valid = NodeValidator.full_validate(node)
                elif isinstance(node, GameComponent):
                    valid = GameComponentValidator.full_validate(node)
                elif isinstance(node, VisualComponent):
                    valid = VisualComponentValidator.full_validate(node)

                if not valid:
                    raise ValueError("Validation failed in validate_full_validate.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_relationships():
        """
        Decorator that calls NodeValidator.validate_relationships
        (regardless of whether it's a Node, GameComponent, or VisualComponent).
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_relationships(node):
                    raise ValueError("Validation failed in validate_relationships.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def top_level_validation():
        """
        Decorator that calls NodeValidator.top_level_validation
        (regardless of whether it's a Node, GameComponent, or VisualComponent).
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.top_level_validation(node):
                    raise ValueError("Validation failed in top_level_validation.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_ready_to_be_added_as_parent():
        """
        Decorator that calls NodeValidator.validate_ready_to_be_added_as_parent.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_ready_to_be_added_as_parent(node):
                    raise ValueError("Validation failed in validate_ready_to_be_added_as_parent.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_ready_to_be_added_as_child():
        """
        Decorator that calls NodeValidator.validate_ready_to_be_added_as_child.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_ready_to_be_added_as_child(node):
                    raise ValueError("Validation failed in validate_ready_to_be_added_as_child.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_ready_to_link_child():
        """
        Decorator that calls NodeValidator.validate_ready_to_link_child with a parent and child.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(parent, child, *args, **kwargs):
                if not NodeValidator.validate_ready_to_link_child(parent, child):
                    raise ValueError("Validation failed in validate_ready_to_link_child.")
                return func(parent, child, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_ready_to_link_children():
        """
        Decorator that calls NodeValidator.validate_ready_to_link_children
        with a parent and a list of children.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(parent, children, *args, **kwargs):
                if not NodeValidator.validate_ready_to_link_children(parent, children):
                    raise ValueError("Validation failed in validate_ready_to_link_children.")
                return func(parent, children, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_node():
        """
        Decorator that calls NodeValidator.validate_is_node.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_is_node(node):
                    raise ValueError("Validation failed in validate_is_node.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_game_component():
        """
        Decorator that calls GameComponentValidator.validate_is_game_component.
        """
        from game.validation.game_component_validator import GameComponentValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not GameComponentValidator.validate_is_game_component(node):
                    raise ValueError("Validation failed in validate_is_game_component.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_visual_component():
        """
        Decorator that calls VisualComponentValidator.validate_is_visual_component.
        """
        from game.validation.visual_component_validator import VisualComponentValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not VisualComponentValidator.validate_is_visual_component(node):
                    raise ValueError("Validation failed in validate_is_visual_component.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_top_level():
        """
        Decorator that calls NodeValidator.validate_is_top_level.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_is_top_level(node):
                    raise ValueError("Validation failed in validate_is_top_level.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_not_top_level():
        """
        Decorator that calls NodeValidator.validate_is_not_top_level.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_is_not_top_level(node):
                    raise ValueError("Validation failed in validate_is_not_top_level.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_children():
        """
        Decorator that calls NodeValidator.validate_children.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_children(node):
                    raise ValueError("Validation failed in validate_children.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_has_parent():
        """
        Decorator that calls NodeValidator.validate_has_parent.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node, *args, **kwargs):
                if not NodeValidator.validate_has_parent(node):
                    raise ValueError("Validation failed in validate_has_parent.")
                return func(node, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_not_self():
        """
        Decorator that calls NodeValidator.validate_not_self with node1 and node2.
        """
        from game.validation.node_validator import NodeValidator

        def decorator(func):
            def wrapper(node1, node2, *args, **kwargs):
                if not NodeValidator.validate_not_self(node1, node2):
                    raise ValueError("Validation failed in validate_not_self.")
                return func(node1, node2, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_enabled():
        """
        Decorator that calls GameComponentValidator.validate_is_enabled (for
        GameComponent or VisualComponent).
        """
        from game.validation.game_component_validator import GameComponentValidator

        def decorator(func):
            def wrapper(game_component, *args, **kwargs):
                if not GameComponentValidator.validate_is_enabled(game_component):
                    raise ValueError("Validation failed in validate_is_enabled.")
                return func(game_component, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def validate_is_disabled():
        """
        Decorator that calls GameComponentValidator.validate_is_disabled (for
        GameComponent or VisualComponent).
        """
        from game.validation.game_component_validator import GameComponentValidator

        def decorator(func):
            def wrapper(game_component, *args, **kwargs):
                if not GameComponentValidator.validate_is_disabled(game_component):
                    raise ValueError("Validation failed in validate_is_disabled.")
                return func(game_component, *args, **kwargs)
            return wrapper
        return decorator
