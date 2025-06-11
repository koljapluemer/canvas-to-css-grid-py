import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_add_column_to_end():
    """Test adding a column to the end of the grid"""
    obj_manager = load_base_state()
    
    # Add a column to the end
    obj_manager.add_column_to_end()
    
    # Expected grid after adding column to end:
    # a a · b b b ·
    # a a 1 1 1 1 ·
    # · 0 · · · 1 ·
    # · 0 0 0 · 1 ·
    # · · · c c 1 ·
    
    grid = obj_manager.make_grid()
    assert grid.width == 7  # Original width (6) + 1
    assert grid.height == 5  # Height unchanged
    
    # Verify the new column is empty
    for row in range(grid.height):
        assert grid.is_cell_empty(row, 6)
    
    # Verify existing content is unchanged
    assert grid.cells[0][0].value == "a"
    assert grid.cells[0][3].value == "b"
    assert grid.cells[4][3].value == "c" 