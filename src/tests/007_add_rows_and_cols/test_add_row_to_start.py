# implement this
# draw the test files first

import os
import pytest
from src.classes.object_manager import ObjectManager

def test_add_row_to_start():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    base_txt_path = os.path.join(current_dir, 'base.txt')
    result_json_path = os.path.join(current_dir, 'result_add_row_to_start.json')
    result_txt_path = os.path.join(current_dir, 'result_add_row_to_start.txt')

    # Load base JSON
    with open(base_json_path, 'r') as f:
        base_json_data = f.read()
    import json
    obj_manager = ObjectManager.create_from_JSON(json.loads(base_json_data))

    # Create grid and verify base.txt matches
    grid = obj_manager.make_grid()
    with open(base_txt_path, 'r') as f:
        expected_base = f.read().strip()
    assert grid.export_to_txt().strip() == expected_base, 'Base grid does not match expected output'

    # Add row to start
    obj_manager.add_row_to_start()

    # Verify JSON output matches
    with open(result_json_path, 'r') as f:
        expected_json = json.loads(f.read())
    actual_json = obj_manager.export_to_JSON()
    assert actual_json == expected_json, 'JSON output does not match expected output'

    # Verify grid output matches
    grid = obj_manager.make_grid()
    with open(result_txt_path, 'r') as f:
        expected_result = f.read().strip()
    assert grid.export_to_txt().strip() == expected_result, 'Resulting grid does not match expected output'