import pytest
from src.classes.object_manager import ObjectManager
from src.classes.node import Node

def test_add_node():
    # Create an empty ObjectManager
    obj_manager = ObjectManager()
    
    # Create a test node
    node = Node(
        id="test_node",
        row=1,
        col=2,
        width=3,
        height=4
    )
    
    # Add the node to the ObjectManager
    obj_manager.add_node(node)
    
    # Verify the node was added
    assert len(obj_manager.nodes) == 1, "Expected exactly one node"
    assert obj_manager.nodes[0] == node, "Added node does not match the original node"
