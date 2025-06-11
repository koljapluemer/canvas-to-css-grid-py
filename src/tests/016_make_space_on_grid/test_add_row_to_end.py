import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_add_row_to_end():
    """Test adding a row to the end of the grid"""
    obj_manager = load_base_state()
    
    # Add a row to the end
    obj_manager.add_row_to_end()
    
    # Expected grid after adding row to end:
    # a a · b b b
    # a a 1 1 1 1
    # · 0 · · · 1
    # · 0 0 0 · 1
    # · · · c c 1
    # · · · · · ·
    
    grid = obj_manager.make_grid()
    assert grid.width == 6  # Width unchanged
    assert grid.height == 6  # Original height (5) + 1
    
    # Verify the new row is empty
    for col in range(grid.width):
        assert grid.is_cell_empty(5, col)
    
    # Verify existing content is unchanged
    assert grid.cells[0][0].value == "a"
    assert grid.cells[0][3].value == "b"
    assert grid.cells[4][3].value == "c" 