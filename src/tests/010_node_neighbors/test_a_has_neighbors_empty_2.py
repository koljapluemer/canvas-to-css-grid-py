import os
import pytest
from src.classes.object_manager import ObjectManager

def test_a_has_neighbors_empty_2():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        import json
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get node 'a'
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    
    # Assert it has 2 empty neighbors
    empty_neighbors = obj_manager.find_all_empty_neighbors(node_a)
    assert len(empty_neighbors) == 2, f"Node 'a' should have 2 empty neighbors, but has {len(empty_neighbors)}"
