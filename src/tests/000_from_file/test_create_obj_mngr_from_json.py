import json
import os
import pytest
from src.classes.object_manager import ObjectManager

def test_create_from_json():
    # Get the path to the test JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'simplegrid.json')
    
    # Load the JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Create ObjectManager from JSON
    obj_manager = ObjectManager.create_from_JSON(json_data)
    
    # Validate the structure
    assert len(obj_manager.nodes) == 3, "Expected 3 nodes"
    assert len(obj_manager.edges) == 2, "Expected 2 edges"
    
    # Validate node IDs
    node_ids = [node['id'] for node in obj_manager.nodes]
    assert 'a' in node_ids, "Node 'a' not found"
    assert 'b' in node_ids, "Node 'b' not found"
    assert 'c' in node_ids, "Node 'c' not found"
    
    # Validate edge IDs
    edge_ids = [edge['id'] for edge in obj_manager.edges]
    assert '0' in edge_ids, "Edge '0' not found"
    assert '1' in edge_ids, "Edge '1' not found"
