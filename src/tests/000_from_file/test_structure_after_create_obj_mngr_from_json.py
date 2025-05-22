import json
import os
import pytest
from src.classes.object_manager import ObjectManager

def test_create_from_json():
    # Get the path to the test JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'simplegrid.json')
        
    # Load the JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Create ObjectManager from JSON
    obj_manager = ObjectManager.create_from_JSON(json_data)
    
    # Validate the structure
    assert len(obj_manager.nodes) == 3, "Expected 3 nodes"
    assert len(obj_manager.edges) == 2, "Expected 2 edges"
    
