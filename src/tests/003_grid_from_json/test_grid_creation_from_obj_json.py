import os
import json
import pytest
from src.classes.object_manager import ObjectManager

def test_grid_creation_from_json():
    # Get the paths to the test files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'simplegrid.json')
    txt_path = os.path.join(data_dir, 'simplegrid.txt')
    
    # Load the JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Create ObjectManager from JSON
    obj_manager = ObjectManager.create_from_JSON(json_data)
    
    # Create grid from ObjectManager
    grid = obj_manager.make_grid()
    
    # Load the expected text representation
    with open(txt_path, 'r') as f:
        expected_txt = f.read().strip()
    
    # Export grid to text and compare
    actual_txt = grid.export_to_txt()
    assert actual_txt == expected_txt, "Grid text representation does not match expected text"
