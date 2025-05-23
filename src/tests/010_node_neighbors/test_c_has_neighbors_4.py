import os
import pytest
from src.classes.object_manager import ObjectManager

def test_c_has_neighbors_4():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        import json
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get node 'c'
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    
    # Assert it has 4 neighbors
    neighbors = obj_manager.find_all_neighbors(node_c)
    assert len(neighbors) == 4, f"Node 'c' should have 4 neighbors, but has {len(neighbors)}"
