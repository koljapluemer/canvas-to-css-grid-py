import os
import pytest
from src.classes.object_manager import ObjectManager

def test_all_data_correctly_represented():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    base_txt_path = os.path.join(current_dir, 'base.txt')
    base_flow_txt_path = os.path.join(current_dir, 'base.flow.txt')

    # Load base JSON
    with open(base_json_path, 'r') as f:
        base_json_data = f.read()
    import json
    obj_manager = ObjectManager.create_from_JSON(json.loads(base_json_data))

    # Verify JSON output matches base.json
    exported_json = obj_manager.export_to_JSON()
    with open(base_json_path, 'r') as f:
        expected_json = json.load(f)
    assert exported_json == expected_json, "Exported JSON does not match base.json"

    # Verify normal txt output matches base.txt
    grid = obj_manager.make_grid()
    with open(base_txt_path, 'r') as f:
        expected_txt = f.read().strip()
    assert grid.export_to_txt().strip() == expected_txt, "Normal txt output does not match base.txt"

    # Verify flow text output matches base.flow.txt
    with open(base_flow_txt_path, 'r') as f:
        expected_flow_txt = f.read().strip()
    assert grid.render_to_flow_txt().strip() == expected_flow_txt, "Flow text output does not match base.flow.txt"
