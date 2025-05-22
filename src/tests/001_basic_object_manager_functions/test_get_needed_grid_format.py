import os
import json
from src.classes.object_manager import ObjectManager

def test_get_needed_grid_format():
    # Get the path to the test JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '5_by_6.json')

    # Load the JSON file
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    # Create ObjectManager from JSON
    obj_manager = ObjectManager.create_from_JSON(json_data)

    # Get needed grid format
    needed_format = obj_manager.create_needed_grid_format()

    assert needed_format == (5, 6), f"Expected (5, 6), got {needed_format}"
