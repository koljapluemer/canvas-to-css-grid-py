import os
import pytest
from src.classes.object_manager import ObjectManager


def test_edges_have_right_symbols():
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'grid_with_complex_edge.json')
    txt_path = os.path.join(current_dir, 'flow_grid_with_complex_edge.txt')

    # Load JSON
    with open(json_path, 'r') as f:
        json_data = f.read()
    import json
    obj_manager = ObjectManager.create_from_JSON(json.loads(json_data))

    # Create grid
    grid = obj_manager.make_grid()

    # Render to flow txt (not implemented yet)
    output = grid.render_to_flow_txt()

    # Load expected output
    with open(txt_path, 'r') as f:
        expected = f.read().strip()

    assert output.strip() == expected, 'Rendered flow grid does not match expected output.'
