import os
import json
from src.classes.object_manager import ObjectManager

def test_is_cell_empty():
    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'simplegrid.json')

    
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    obj_manager = ObjectManager.create_from_JSON(json_data)
    grid = obj_manager.make_grid()
    
    # Test cases
    assert grid.is_cell_empty(0, 0) == False  # Cell with node 'a'
    assert grid.is_cell_empty(2, 0) == True   # Empty cell
    assert grid.is_cell_empty(99, 99) == False  # out of bounds
