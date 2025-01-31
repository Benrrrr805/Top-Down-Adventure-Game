from game.core.node import Node
from game.core.validation.node_validation import NodeValidation
import pytest

def test_name_is_unknown():
    # name is not a string => should return True
    node_non_string_name = Node(name=123)
    assert NodeValidation.name_is_unknown(node_non_string_name) is True

    # name is a string => should return False
    node_string_name = Node(name="ValidName")
    assert NodeValidation.name_is_unknown(node_string_name) is False

# ------------------------------------------------------------------------------
# validate_base_values
# ------------------------------------------------------------------------------
def test_validate_base_values_success():
    node = Node(name="BaseNode", top_level=True)
    assert NodeValidation.validate_base_values(node) is True

def test_validate_base_values_no_name():
    # Test branch: Node with no valid name, top-level => raise ValueError
    node = Node(name=None, top_level=True)
    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        NodeValidation.validate_base_values(node)

def test_validate_base_values_top_level_not_boolean():
    # top_level must be a boolean
    node = Node(name="BadTopLevel", top_level="not_bool")
    with pytest.raises(ValueError, match=r"top_level must be a boolean"):
        NodeValidation.validate_base_values(node)

# ------------------------------------------------------------------------------
# validate_is_node
# ------------------------------------------------------------------------------
def test_validate_is_node_success():
    node = Node(name="IsNode")
    assert NodeValidation.validate_is_node(node) is True

def test_validate_is_node_failure():
    not_a_node = "I am definitely not a Node object"
    with pytest.raises(ValueError, match=r"Expected: Node\. Recieved: str"):
        NodeValidation.validate_is_node(not_a_node)

# ------------------------------------------------------------------------------
# validate_is_top_level / validate_is_not_top_level
# ------------------------------------------------------------------------------
def test_validate_is_top_level():
    node = Node(name="TopLevel", top_level=True)
    assert NodeValidation.validate_is_top_level(node) is True
    assert NodeValidation.validate_is_not_top_level(node) is False

def test_validate_is_not_top_level():
    node = Node(name="NotTopLevel", top_level=False)
    assert NodeValidation.validate_is_not_top_level(node) is True
    assert NodeValidation.validate_is_top_level(node) is False

# ------------------------------------------------------------------------------
# validate_has_parent
# ------------------------------------------------------------------------------
def test_validate_has_parent_success():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False, parent=parent)
    assert NodeValidation.validate_has_parent(child) is True

def test_validate_has_parent_failure_top_level():
    # If top-level => should raise
    node = Node(name="LonelyTop", top_level=True)
    with pytest.raises(ValueError, match=r"should not have parent, since it is a top-level Node"):
        NodeValidation.validate_has_parent(node)

def test_validate_has_parent_failure_invalid_parent():
    # If parent is not a Node => should raise
    node = Node(name="InvalidParent", top_level=False, parent="NotANode")
    with pytest.raises(ValueError, match="InvalidParent does not have a parent"):
        NodeValidation.validate_has_parent(node)

    invalid_parent = Node(name="InvalidParent", top_level="NotBool")
    node.parent = invalid_parent
    with pytest.raises(ValueError, match="InvalidParent does not have a valid parent"):
        NodeValidation.validate_has_parent(node)

# ------------------------------------------------------------------------------
# validate_not_self
# ------------------------------------------------------------------------------
def test_validate_not_self_same_object():
    node = Node(name="SameNode")
    # If node1 == node2
    with pytest.raises(ValueError, match=r".*is the same as.*"):
        NodeValidation.validate_not_self(node, node)

def test_validate_not_self_same_name():
    n1 = Node(name="DuplicateName")
    n2 = Node(name="DuplicateName")
    with pytest.raises(ValueError, match=r".*has the same name as.*"):
        NodeValidation.validate_not_self(n1, n2)

def test_validate_not_self_different_nodes():
    n1 = Node(name="NodeA")
    n2 = Node(name="NodeB")
    assert NodeValidation.validate_not_self(n1, n2) is True

# ------------------------------------------------------------------------------
# validate_children
# ------------------------------------------------------------------------------
def test_validate_children_success():
    parent = Node(name="Parent", top_level=True)
    child1 = Node(name="Child1", top_level=False)
    child2 = Node(name="Child2", top_level=False)
    parent.link_children([child1, child2])

    assert NodeValidation.validate_children(parent) is True

def test_validate_children_failure_not_list():
    # Force children to be a non-list to test error
    # We'll dynamically override 'children' after creation
    node = Node(name="InvalidChildren", top_level=False)
    node.children = "I am not a list"

    with pytest.raises(ValueError, match=r"Children must be a list.*"):
        NodeValidation.validate_children(node)

def test_validate_children_child_invalid():
    # Child that fails base validation (no name).
    parent = Node(name="Parent", top_level=True)
    child = Node(name=None, top_level=False)
    parent.link_child(child)

    with pytest.raises(ValueError, match=r"Node: Unknown. Failed validation. name must be a non-empty string."):
        NodeValidation.validate_children(parent)

# ------------------------------------------------------------------------------
# validate_relationships
# ------------------------------------------------------------------------------
def test_validate_relationships_top_level_no_parent():
    node = Node(name="TopLevel", top_level=True)
    assert NodeValidation.validate_relationships(node) is True

def test_validate_relationships_not_top_level_no_parent():
    # Not top-level, but also no parent => validate_has_parent should fail
    node = Node(name="ChildButNoParent", top_level=False)
    with pytest.raises(ValueError, match=r"does not have a parent"):
        NodeValidation.validate_relationships(node)

# ------------------------------------------------------------------------------
# full_validate
# ------------------------------------------------------------------------------
def test_full_validate_success():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False)
    parent.link_child(child)
    # Should pass full validation
    assert NodeValidation.full_validate(parent) is True
    assert NodeValidation.full_validate(child) is True

def test_full_validate_not_a_node():
    with pytest.raises(ValueError, match=r"Expected: Node. Recieved: str"):
        NodeValidation.full_validate("NotANode")

def test_full_validate_missing_name():
    node = Node(name=None, top_level=False)
    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        NodeValidation.full_validate(node)

# ------------------------------------------------------------------------------
# top_level_validation
# ------------------------------------------------------------------------------
def test_top_level_validation_success():
    node = Node(name="TopLevelNode", top_level=True)
    # Should validate base + children + is_top_level
    assert NodeValidation.top_level_validation(node) is True

def test_top_level_validation_fails_on_children():
    # One child is invalid (no name)
    top_level_node = Node(name="TopLevelNode", top_level=True)
    child_invalid = Node(name=None, top_level=False)
    top_level_node.link_child(child_invalid)

    with pytest.raises(ValueError, match=r"Node: Unknown. Failed validation. name must be a non-empty string."):
        NodeValidation.top_level_validation(top_level_node)

def test_top_level_validation_not_top_level():
    # Should fail if node is not top-level
    node = Node(name="NotTopLevel", top_level=False)
    with pytest.raises(ValueError, match=r"Node must be top-level to be validated as top-level."):
        NodeValidation.top_level_validation(node)

# ------------------------------------------------------------------------------
# validate_ready_to_be_added_as_parent
# ------------------------------------------------------------------------------
def test_validate_ready_to_be_added_as_parent_success():
    # Valid scenario: node is top-level or not, but let's test both.
    # If not top-level => must have parent
    top_level_node = Node(name="TopLevelParent", top_level=True)
    assert NodeValidation.validate_ready_to_be_added_as_parent(top_level_node) is True

    not_top_level_parent = Node(name="NotTopParent", top_level=False, parent=Node(name="GrandParent", top_level=True))
    assert NodeValidation.validate_ready_to_be_added_as_parent(not_top_level_parent) is True

def test_validate_ready_to_be_added_as_parent_failure_not_node():
    # Should fail if object is not a node
    with pytest.raises(ValueError, match=r"Expected: Node"):
        NodeValidation.validate_ready_to_be_added_as_parent("NotNode")

def test_validate_ready_to_be_added_as_parent_children_fail():
    parent = Node(name="ParentFail", top_level=True)
    # Add a child with no name => fail
    bad_child = Node(name=None, top_level=False)
    parent.link_child(bad_child)

    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        NodeValidation.validate_ready_to_be_added_as_parent(parent)

# ------------------------------------------------------------------------------
# validate_ready_to_be_added_as_child
# ------------------------------------------------------------------------------
def test_validate_ready_to_be_added_as_child_failure_if_top_level():
    # If top-level => must fail
    node = Node(name="TopLevelNode", top_level=True)
    with pytest.raises(ValueError, match=r"Node must not be top-level to be added as a child"):
        NodeValidation.validate_ready_to_be_added_as_child(node)

def test_validate_ready_to_be_added_as_child_success():
    # A valid child => not top-level, has a parent or can be parentless?
    # No requirement that child must have a parent here, but let's test both:
    node = Node(name="ChildNode", top_level=False)
    assert NodeValidation.validate_ready_to_be_added_as_child(node) is True
    assert NodeValidation.validate_ready_to_be_added_as_child(Node(name="ParentlessChild", top_level=False)) is True

# ------------------------------------------------------------------------------
# validate_ready_to_link_child
# ------------------------------------------------------------------------------
def test_validate_ready_to_link_child_success():
    parent = Node(name="ParentLink", top_level=True)
    child = Node(name="ChildLink", top_level=False)
    assert NodeValidation.validate_ready_to_link_child(parent, child) is True

def test_validate_ready_to_link_child_failure_child_top_level():
    parent = Node(name="ParentLink", top_level=True)
    child = Node(name="ChildLinkTop", top_level=True)
    with pytest.raises(ValueError, match=r"Node must not be top-level to be added as a child"):
        NodeValidation.validate_ready_to_link_child(parent, child)

# ------------------------------------------------------------------------------
# validate_ready_to_link_children
# ------------------------------------------------------------------------------
def test_validate_ready_to_link_children_success():
    parent = Node(name="Parent", top_level=True)
    child1 = Node(name="C1", top_level=False)
    child2 = Node(name="C2", top_level=False)
    assert NodeValidation.validate_ready_to_link_children(parent, [child1, child2]) is True

def test_validate_ready_to_link_children_one_child_fails():
    parent = Node(name="ParentLink", top_level=True)
    good_child = Node(name="ChildOk", top_level=False)
    bad_child = Node(name="ChildBadTopLevel", top_level=True)

    # The second child is top-level => should fail
    with pytest.raises(ValueError, match=r"Node must not be top-level"):
        NodeValidation.validate_ready_to_link_children(parent, [good_child, bad_child])
