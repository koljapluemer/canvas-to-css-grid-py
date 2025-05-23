import os
import pytest
from src.classes.object_manager import ObjectManager

def test_a_has_1_attachment_pt():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        import json
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get node 'a'
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    
    # Assert it has 1 valid attachment point
    attachment_points = obj_manager.get_valid_attachment_points(node_a)
    assert len(attachment_points) == 1, f"Node 'a' should have 1 valid attachment point, but has {len(attachment_points)}"
