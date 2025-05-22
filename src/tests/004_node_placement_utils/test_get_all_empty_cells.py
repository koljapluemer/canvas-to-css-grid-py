import os
import json
from src.classes.object_manager import ObjectManager

def test_get_all_empty_cells():
    # Setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    json_path = os.path.join(data_dir, 'simplegrid.json')
    
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    obj_manager = ObjectManager.create_from_JSON(json_data)
    grid = obj_manager.make_grid()
    
    # Test cases
    empty_cells = grid.get_all_empty_cells()
    # should be exactly 10 empty cells
    assert len(empty_cells) == 10
    # specific (non)empty cells
    assert (0, 2) in empty_cells 
    assert (3, 0) in empty_cells  
    assert (0, 0) not in empty_cells 
    assert (4, 5) not in empty_cells 
    assert (99, 99) not in empty_cells  
