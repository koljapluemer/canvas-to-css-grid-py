import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_detect_clonable_columns():
    """Test detecting which columns can be cloned"""
    obj_manager = load_base_state()
    
    # Add some horizontal edges to make columns clonable
    # First, add a node that we can connect to
    obj_manager.add_node_at_coordinate("d", 3, 6)
    
    # Then add an edge with horizontal segments
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    node_d = next(node for node in obj_manager.nodes if node.id == 'd')
    obj_manager.draw_edge(
        sender_node=node_a,
        receiver_node=node_d,
        sender_attachment_point=(1, 2),
        receiver_attachment_point=(3, 5),
        has_arrow_sender=False,
        has_arrow_receiver=False
    )
    
    # Now check which columns are clonable
    clonable_cols = obj_manager.get_clonable_columns()
    
    # Column 2 should be clonable (contains horizontal edge without arrow)
    assert 2 in clonable_cols
    
    # Column 1 should not be clonable (contains edge with arrow)
    assert 1 not in clonable_cols
    
    # Column 0 should not be clonable (contains nodes)
    assert 0 not in clonable_cols
    
    # Column 3 should not be clonable (contains nodes)
    assert 3 not in clonable_cols
    
    # Column 4 should not be clonable (contains nodes)
    assert 4 not in clonable_cols
    
    # Column 5 should be clonable (contains horizontal edge without arrow)
    assert 5 in clonable_cols 