import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_add_row_to_start():
    """Test adding a row to the start of the grid"""
    obj_manager = load_base_state()
    
    # Add a row to the start
    obj_manager.add_row_to_start()
    
    # Expected grid after adding row to start:
    # · · · · · ·
    # a a · b b b
    # a a 1 1 1 1
    # · 0 · · · 1
    # · 0 0 0 · 1
    # · · · c c 1
    
    grid = obj_manager.make_grid()
    assert grid.width == 6  # Width unchanged
    assert grid.height == 6  # Original height (5) + 1
    
    # Verify the new row is empty
    for col in range(grid.width):
        assert grid.is_cell_empty(0, col)
    
    # Verify existing content is shifted down
    assert grid.cells[1][0].value == "a"  # Was at (0,0)
    assert grid.cells[1][3].value == "b"  # Was at (0,3)
    assert grid.cells[5][3].value == "c"  # Was at (4,3)
    
    # Verify node positions are updated
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    assert node_a.row == 1  # Was 0
    node_b = next(node for node in obj_manager.nodes if node.id == 'b')
    assert node_b.row == 1  # Was 0
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    assert node_c.row == 5  # Was 4 