import os
import pytest
from src.classes.object_manager import ObjectManager

def test_b_has_3_attachment_pt():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        import json
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get node 'b'
    node_b = next(node for node in obj_manager.nodes if node.id == 'b')
    
    # Assert it has 3 valid attachment points
    attachment_points = obj_manager.get_valid_attachment_points(node_b)
    assert len(attachment_points) == 3, f"Node 'b' should have 3 valid attachment points, but has {len(attachment_points)}"
