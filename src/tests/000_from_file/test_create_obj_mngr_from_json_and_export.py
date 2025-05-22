import json
import os
import pytest
from src.classes.object_manager import ObjectManager
from src.classes.coordinate import Coordinate

def test_create_from_json_and_export():
    # Get the path to the test JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'simplegrid.json')
    
    # Load the original JSON file
    with open(json_path, 'r') as f:
        original_json = json.load(f)
    
    # Create ObjectManager from JSON
    obj_manager = ObjectManager.create_from_JSON(original_json)
    
    # Export back to JSON
    exported_json = obj_manager.export_to_JSON()
    
    # Convert coordinates in original JSON to match exported format
    processed_original = original_json.copy()
    for edge in processed_original['edges']:
        edge['cells'] = [{'row': cell[0], 'col': cell[1]} for cell in edge['cells']]
    
    # Compare the original and exported JSON
    assert exported_json == processed_original, "Exported JSON does not match original JSON"
