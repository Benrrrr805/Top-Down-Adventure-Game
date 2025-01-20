from game.core.node import Node  # Assuming your Node class is in a file named node.py

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
