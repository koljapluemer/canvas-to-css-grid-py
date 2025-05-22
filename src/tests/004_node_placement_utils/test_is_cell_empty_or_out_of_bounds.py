import os
import json
from src.classes.object_manager import ObjectManager

def test_is_cell_empty_or_out_of_bounds():
    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'simplegrid.json')

    
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    obj_manager = ObjectManager.create_from_JSON(json_data)
    grid = obj_manager.make_grid()
    
    # Test cases
    assert grid.is_cell_empty_or_out_of_bounds(0, 0) == False 
    assert grid.is_cell_empty_or_out_of_bounds(2, 2) == True   
    assert grid.is_cell_empty_or_out_of_bounds(4, 0) == True   
    assert grid.is_cell_empty_or_out_of_bounds(99, 99) == True # Out of bounds