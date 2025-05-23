import pytest
from src.classes.object_manager import ObjectManager
from src.classes.edge import Edge, Attachment
from src.classes.node import Node
from src.classes.coordinate import Coordinate

def test_add_edge():
    # Create an empty ObjectManager
    obj_manager = ObjectManager()
    
    # Create test nodes
    node_a = Node(id="a", row=0, col=0, width=2, height=2)
    node_b = Node(id="b", row=0, col=3, width=3, height=1)
    
    # Add nodes to the ObjectManager
    obj_manager.add_node(node_a)
    obj_manager.add_node(node_b)
    
    # Create test coordinates
    cells = [
        Coordinate(row=2, col=1),
        Coordinate(row=3, col=1),
        Coordinate(row=3, col=2),
        Coordinate(row=3, col=3)
    ]
    
    # Create test attachments
    sender_attachment = Attachment(node_id="a", has_arrow=False, node_in_direction="W")
    receiver_attachment = Attachment(node_id="b", has_arrow=True, node_in_direction="E")
    
    # Create a test edge
    edge = Edge(
        id="test_edge",
        sender_attachment=sender_attachment,
        receiver_attachment=receiver_attachment,
        cells=cells
    )
    
    # Add the edge to the ObjectManager
    obj_manager.add_edge(edge)
    
    # Verify the edge was added
    assert len(obj_manager.edges) == 1, "Expected exactly one edge"
    assert obj_manager.edges[0] == edge, "Added edge does not match the original edge"
