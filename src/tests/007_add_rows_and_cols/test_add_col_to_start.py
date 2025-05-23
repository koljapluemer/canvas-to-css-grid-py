import os
import pytest
from src.classes.object_manager import ObjectManager

def test_add_col_to_start():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    result_txt_path = os.path.join(current_dir, 'result_add_col_to_start.txt')

    # Load base JSON
    with open(base_json_path, 'r') as f:
        base_json_data = f.read()
    import json
    obj_manager = ObjectManager.create_from_JSON(json.loads(base_json_data))

    # Add column to start
    obj_manager.add_col_to_start()

    # Verify grid output matches
    grid = obj_manager.make_grid()
    with open(result_txt_path, 'r') as f:
        expected_result = f.read().strip()
    assert grid.export_to_txt().strip() == expected_result, 'Resulting grid does not match expected output'
