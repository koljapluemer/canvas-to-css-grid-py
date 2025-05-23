import os
import json
import pytest
from src.classes.grid import Grid
from src.classes.object_manager import ObjectManager

def test_node_placement_correct():
    # Get paths to test files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'one-spot-for-adding-node.json')
    txt_path = os.path.join(data_dir, 'one-spot-for-adding-node.txt')
    expected_after_path = os.path.join(current_dir, 'node-added.txt')
    expected_json_path = os.path.join(current_dir, 'node-added.json')
    
    # Load initial state from JSON
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    # Create ObjectManager and Grid
    obj_manager = ObjectManager.create_from_JSON(json_data)
    grid = obj_manager.make_grid()
    
    # Verify initial state matches txt file
    with open(txt_path, 'r') as f:
        expected_initial = f.read().strip()
    actual_initial = grid.export_to_txt()
    assert actual_initial == expected_initial, "Initial grid state does not match expected txt file"
    
    # Add node 'd' at valid spot
    obj_manager.add_node_at_valid_spot(id="d")
    grid = obj_manager.make_grid()
    
    # Verify final state matches node-added.txt
    with open(expected_after_path, 'r') as f:
        expected_final = f.read().strip()
    actual_final = grid.export_to_txt()
    assert actual_final == expected_final, "Final grid state does not match node-added.txt"
    
    # Verify JSON export matches node-added.json
    with open(expected_json_path, 'r') as f:
        expected_json = json.load(f)
    actual_json = obj_manager.export_to_JSON()
    assert actual_json == expected_json, "Exported JSON does not match node-added.json"
