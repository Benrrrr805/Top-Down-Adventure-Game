from game.core.node import Node  # Assuming your Node class is in a file named node.py
import json
import pytest
def test_node_initialization():
    # Set relationship through children=[child1_node]
    child1_node = Node(name="Child1Node", top_level=False)
    parent1_node = Node(name="Parent1Node", top_level=True, children=[child1_node])
    # Set relationship through parent=parent2_node
    parent2_node = Node(name="Parent2Node", top_level=True)
    child2_node = Node(name="Child2Node", top_level=False, parent=parent2_node)

    assert parent1_node.name == "Parent1Node"
    assert child1_node.name == "Child1Node"

    assert parent1_node.top_level is True
    assert child1_node.top_level is False

    assert parent1_node.children == [child1_node]
    assert child1_node.children == []

    assert parent1_node.parent is None
    assert child1_node.parent == parent1_node

    assert parent2_node.name == "Parent2Node"
    assert child2_node.name == "Child2Node"

    assert parent2_node.top_level is True
    assert child2_node.top_level is False

    assert parent2_node.children == [child2_node]
    assert child2_node.children == []

    assert parent2_node.parent is None
    assert child2_node.parent == parent2_node

def test_node_to_dict():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False)
    parent.link_child(child)

    d = parent.to_dict()
    assert d["name"] == "Parent"
    assert d["top_level"] is True
    assert d["attributes"] == {}
    assert len(d["children"]) == 1
    assert d["children"][0]["name"] == "Child"
    assert d["parent"] is None

def test_node_str():
    parent = Node(name="Parent")
    child = Node(name="Child")
    parent.link_child(child)

    d = parent.to_dict()
    s = parent.__str__()
    assert s == json.dumps(d, indent=4)



def test_add_and_remove_child():
    parent = Node(name="Parent")
    child = Node(name="Child")

    parent.link_child(child)
    assert child in parent.children

    parent.unlink_child(child)
    assert child not in parent.children

def test_add_and_remove_children():
    parent = Node(name="Parent")
    child1 = Node(name="Child1")
    child2 = Node(name="Child2")
    child3 = Node(name="Child3")
    parent.link_children([child1, child2, child3])

    assert child1 in parent.children
    assert child2 in parent.children
    assert child3 in parent.children
    assert child1.parent == parent
    assert child2.parent == parent
    assert child3.parent == parent

    parent.unlink_children([child1, child2, child3])
    
    assert child1 not in parent.children
    assert child2 not in parent.children
    assert child3 not in parent.children
    assert child1.parent is None
    assert child2.parent is None
    assert child3.parent is None

def test_add_and_remove_parent():
    parent = Node(name="Parent")
    child = Node(name="Child")

    child.link_parent(parent)
    assert child.parent == parent

    child.unlink_parent()
    assert child.parent is None

def test_get_child():
    parent = Node(name="Parent")
    child = Node(name="Child")
    parent.link_child(child)

    result = parent.get_child("Child")
    assert result == child

    result = parent.get_child("NonExistent")
    assert result is None

def test_get_parent():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False)
    child.link_parent(parent)

    assert child.get_parent() == parent
    
def test_has_child():
    parent = Node(name="Parent")
    child = Node(name="Child")
    grandchild = Node(name="Grandchild")
    parent.link_child(child)
    child.link_child(grandchild)

    assert parent.has_child(child) is True
    assert parent.has_child(grandchild) is True
    assert parent.has_child(Node(name="OtherNode")) is False

def test_get_node():
    parent = Node(name="Parent")
    child = Node(name="Child")
    grandchild = Node(name="Grandchild")
    other = Node(name="Other")
    parent.link_child(child)
    child.link_child(grandchild)

    result = parent.get_node("Grandchild")
    assert result == grandchild

    result = child.get_node("Parent")
    assert result == parent

    result = grandchild.get_node("Parent")
    assert result == parent

    result = grandchild.get_node("Child")
    assert result == child

    result = grandchild.get_node("Other")
    assert result is other

    result = parent.get_node("NonExistent")
    assert result is None

def test_get_siblings():
    parent = Node(name="Parent")
    child1 = Node(name="Child1")
    child2 = Node(name="Child2")
    parent.link_children([child1, child2])

    siblings = child1.get_siblings()
    assert siblings == [child2]

def test_get_ancestors():
    grandparent = Node(name="Grandparent")
    parent = Node(name="Parent")
    child = Node(name="Child")

    grandparent.link_child(parent)
    parent.link_child(child)

    ancestors = child.get_ancestors()
    assert ancestors == [parent, grandparent]

def test_get_descendants():
    parent = Node(name="Parent")
    child1 = Node(name="Child1")
    child2 = Node(name="Child2")

    parent.link_children([child1, child2])

    descendants = parent.get_descendants()
    assert child1 in descendants
    assert child2 in descendants

def test_traverse_depth_first():
    root = Node(name="Root")
    child1 = Node(name="Child1")
    child2 = Node(name="Child2")
    grandchild = Node(name="Grandchild")

    root.link_children([child1, child2])
    child1.link_child(grandchild)

    traversal = root.traverse_depth_first()
    assert traversal == [root, child1, grandchild, child2]

def test_traverse_breadth_first():
    root = Node(name="Root")
    child1 = Node(name="Child1")
    child2 = Node(name="Child2")
    grandchild = Node(name="Grandchild")

    root.link_children([child1, child2])
    child1.link_child(grandchild)

    traversal = root.traverse_breadth_first()
    assert traversal == [root, child1, child2, grandchild]
    
def test_name_is_unknown():
    # name is not a string => should return True
    node_non_string_name = Node(name=123)
    assert Node.name_is_unknown(node_non_string_name) is True

    # name is a string => should return False
    node_string_name = Node(name="ValidName")
    assert Node.name_is_unknown(node_string_name) is False

# ------------------------------------------------------------------------------
# validate_base_values
# ------------------------------------------------------------------------------
def test_validate_base_values_success():
    node = Node(name="BaseNode", top_level=True)
    assert Node.validate_base_values(node) is True

def test_validate_base_values_no_name():
    # Test branch: Node with no valid name, top-level => raise ValueError
    node = Node(name=None, top_level=True)
    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        Node.validate_base_values(node)

def test_validate_base_values_top_level_not_boolean():
    # top_level must be a boolean
    node = Node(name="BadTopLevel", top_level="not_bool")
    with pytest.raises(ValueError, match=r"top_level must be a boolean"):
        Node.validate_base_values(node)

# ------------------------------------------------------------------------------
# validate_is_node
# ------------------------------------------------------------------------------
def test_validate_is_node_success():
    node = Node(name="IsNode")
    assert Node.validate_is_node(node) is True

def test_validate_is_node_failure():
    not_a_node = "I am definitely not a Node object"
    with pytest.raises(ValueError, match=r"Expected: Node\. Recieved: str"):
        Node.validate_is_node(not_a_node)

# ------------------------------------------------------------------------------
# validate_is_top_level / validate_is_not_top_level
# ------------------------------------------------------------------------------
def test_validate_is_top_level():
    node = Node(name="TopLevel", top_level=True)
    assert Node.validate_is_top_level(node) is True
    assert Node.validate_is_not_top_level(node) is False

def test_validate_is_not_top_level():
    node = Node(name="NotTopLevel", top_level=False)
    assert Node.validate_is_not_top_level(node) is True
    assert Node.validate_is_top_level(node) is False

# ------------------------------------------------------------------------------
# validate_has_parent
# ------------------------------------------------------------------------------
def test_validate_has_parent_success():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False, parent=parent)
    assert Node.validate_has_parent(child) is True

def test_validate_has_parent_failure_top_level():
    # If top-level => should raise
    node = Node(name="LonelyTop", top_level=True)
    with pytest.raises(ValueError, match=r"should not have parent, since it is a top-level Node"):
        Node.validate_has_parent(node)

# ------------------------------------------------------------------------------
# validate_not_self
# ------------------------------------------------------------------------------
def test_validate_not_self_same_object():
    node = Node(name="SameNode")
    # If node1 == node2
    with pytest.raises(ValueError, match=r".*is the same as.*"):
        Node.validate_not_self(node, node)

def test_validate_not_self_same_name():
    n1 = Node(name="DuplicateName")
    n2 = Node(name="DuplicateName")
    with pytest.raises(ValueError, match=r".*has the same name as.*"):
        Node.validate_not_self(n1, n2)

def test_validate_not_self_different_nodes():
    n1 = Node(name="NodeA")
    n2 = Node(name="NodeB")
    assert Node.validate_not_self(n1, n2) is True

# ------------------------------------------------------------------------------
# validate_children
# ------------------------------------------------------------------------------
def test_validate_children_success():
    parent = Node(name="Parent", top_level=True)
    child1 = Node(name="Child1", top_level=False)
    child2 = Node(name="Child2", top_level=False)
    Node.link_children(parent, [child1, child2])

    assert Node.validate_children(parent) is True

def test_validate_children_failure_not_list():
    # Force children to be a non-list to test error
    # We'll dynamically override 'children' after creation
    node = Node(name="InvalidChildren", top_level=False)
    node.children = "I am not a list"

    with pytest.raises(ValueError, match=r"Children must be a list.*"):
        Node.validate_children(node)

def test_validate_children_child_invalid():
    # Child that fails base validation (no name).
    parent = Node(name="Parent", top_level=True)
    child = Node(name=None, top_level=False)
    Node.link_child(parent, child)

    with pytest.raises(ValueError, match=r"Node: Unknown. Failed validation. name must be a non-empty string."):
        Node.validate_children(parent)

# ------------------------------------------------------------------------------
# validate_relationships
# ------------------------------------------------------------------------------
def test_validate_relationships_top_level_no_parent():
    node = Node(name="TopLevel", top_level=True)
    assert Node.validate_relationships(node) is True

def test_validate_relationships_not_top_level_no_parent():
    # Not top-level, but also no parent => validate_has_parent should fail
    node = Node(name="ChildButNoParent", top_level=False)
    with pytest.raises(ValueError, match=r"does not have a parent"):
        Node.validate_relationships(node)

# ------------------------------------------------------------------------------
# full_validate
# ------------------------------------------------------------------------------
def test_full_validate_success():
    parent = Node(name="Parent", top_level=True)
    child = Node(name="Child", top_level=False)
    Node.link_child(parent, child)
    # Should pass full validation
    assert Node.full_validate(parent) is True
    assert Node.full_validate(child) is True

def test_full_validate_not_a_node():
    with pytest.raises(ValueError, match=r"Expected: Node. Recieved: str"):
        Node.full_validate("NotANode")

def test_full_validate_missing_name():
    node = Node(name=None, top_level=False)
    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        Node.full_validate(node)

# ------------------------------------------------------------------------------
# top_level_validation
# ------------------------------------------------------------------------------
def test_top_level_validation_success():
    node = Node(name="TopLevelNode", top_level=True)
    # Should validate base + children + is_top_level
    assert Node.top_level_validation(node) is True

def test_top_level_validation_fails_on_children():
    # One child is invalid (no name)
    top_level_node = Node(name="TopLevelNode", top_level=True)
    child_invalid = Node(name=None, top_level=False)
    Node.link_child(top_level_node, child_invalid)

    with pytest.raises(ValueError, match=r"Node: Unknown. Failed validation. name must be a non-empty string."):
        Node.top_level_validation(top_level_node)

def test_top_level_validation_not_top_level():
    # Should fail if node is not top-level
    node = Node(name="NotTopLevel", top_level=False)
    with pytest.raises(ValueError, match=r"Node must be top-level to be validated as top-level."):
        Node.top_level_validation(node)

# ------------------------------------------------------------------------------
# validate_ready_to_be_added_as_parent
# ------------------------------------------------------------------------------
def test_validate_ready_to_be_added_as_parent_success():
    # Valid scenario: node is top-level or not, but let's test both.
    # If not top-level => must have parent
    top_level_node = Node(name="TopLevelParent", top_level=True)
    assert Node.validate_ready_to_be_added_as_parent(top_level_node) is True

    not_top_level_parent = Node(name="NotTopParent", top_level=False, parent=Node(name="GrandParent", top_level=True))
    assert Node.validate_ready_to_be_added_as_parent(not_top_level_parent) is True

def test_validate_ready_to_be_added_as_parent_failure_not_node():
    # Should fail if object is not a node
    with pytest.raises(ValueError, match=r"Expected: Node"):
        Node.validate_ready_to_be_added_as_parent("NotNode")

def test_validate_ready_to_be_added_as_parent_children_fail():
    parent = Node(name="ParentFail", top_level=True)
    # Add a child with no name => fail
    bad_child = Node(name=None, top_level=False)
    Node.link_child(parent, bad_child)

    with pytest.raises(ValueError, match="Node: Unknown. Failed validation. name must be a non-empty string."):
        Node.validate_ready_to_be_added_as_parent(parent)

# ------------------------------------------------------------------------------
# validate_ready_to_be_added_as_child
# ------------------------------------------------------------------------------
def test_validate_ready_to_be_added_as_child_failure_if_top_level():
    # If top-level => must fail
    node = Node(name="TopLevelNode", top_level=True)
    with pytest.raises(ValueError, match=r"Node must not be top-level to be added as a child"):
        Node.validate_ready_to_be_added_as_child(node)

def test_validate_ready_to_be_added_as_child_success():
    # A valid child => not top-level, has a parent or can be parentless?
    # No requirement that child must have a parent here, but let's test both:
    node = Node(name="ChildNode", top_level=False)
    assert Node.validate_ready_to_be_added_as_child(node) is True
    assert Node.validate_ready_to_be_added_as_child(Node(name="ParentlessChild", top_level=False)) is True

# ------------------------------------------------------------------------------
# validate_ready_to_link_child
# ------------------------------------------------------------------------------
def test_validate_ready_to_link_child_success():
    parent = Node(name="ParentLink", top_level=True)
    child = Node(name="ChildLink", top_level=False)
    assert Node.validate_ready_to_link_child(parent, child) is True

def test_validate_ready_to_link_child_failure_child_top_level():
    parent = Node(name="ParentLink", top_level=True)
    child = Node(name="ChildLinkTop", top_level=True)
    with pytest.raises(ValueError, match=r"Node must not be top-level to be added as a child"):
        Node.validate_ready_to_link_child(parent, child)

# ------------------------------------------------------------------------------
# validate_ready_to_link_children
# ------------------------------------------------------------------------------
def test_validate_ready_to_link_children_success():
    parent = Node(name="Parent", top_level=True)
    child1 = Node(name="C1", top_level=False)
    child2 = Node(name="C2", top_level=False)
    assert Node.validate_ready_to_link_children(parent, [child1, child2]) is True

def test_validate_ready_to_link_children_one_child_fails():
    parent = Node(name="ParentLink", top_level=True)
    good_child = Node(name="ChildOk", top_level=False)
    bad_child = Node(name="ChildBadTopLevel", top_level=True)

    # The second child is top-level => should fail
    with pytest.raises(ValueError, match=r"Node must not be top-level"):
        Node.validate_ready_to_link_children(parent, [good_child, bad_child])
