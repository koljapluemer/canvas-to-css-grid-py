import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_detect_clonable_rows():
    """Test detecting which rows can be cloned"""
    obj_manager = load_base_state()
    
    # Add some vertical edges to make rows clonable
    # First, add a node that we can connect to
    obj_manager.add_node_at_coordinate("d", 3, 6)
    
    # Then add an edge with vertical segments
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    node_d = next(node for node in obj_manager.nodes if node.id == 'd')
    obj_manager.draw_edge(
        sender_node=node_a,
        receiver_node=node_d,
        sender_attachment_point=(2, 1),
        receiver_attachment_point=(3, 5),
        has_arrow_sender=False,
        has_arrow_receiver=False
    )
    
    # Now check which rows are clonable
    clonable_rows = obj_manager.get_clonable_rows()
    
    # Row 2 should be clonable (contains vertical edge without arrow)
    assert 2 in clonable_rows
    
    # Row 1 should not be clonable (contains edge with arrow)
    assert 1 not in clonable_rows
    
    # Row 0 should not be clonable (contains nodes)
    assert 0 not in clonable_rows
    
    # Row 3 should be clonable (contains vertical edge without arrow)
    assert 3 in clonable_rows
    
    # Row 4 should not be clonable (contains nodes)
    assert 4 not in clonable_rows 