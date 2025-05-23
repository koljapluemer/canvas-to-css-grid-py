import os
import pytest
from src.classes.object_manager import ObjectManager

def test_c_has_2_attachment_pt():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        import json
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get node 'c'
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    
    # Assert it has 2 valid attachment points
    attachment_points = obj_manager.get_valid_attachment_points(node_c)
    assert len(attachment_points) == 2, f"Node 'c' should have 2 valid attachment points, but has {len(attachment_points)}"
