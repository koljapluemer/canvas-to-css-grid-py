import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_add_column_to_start():
    """Test adding a column to the start of the grid"""
    obj_manager = load_base_state()
    
    # Add a column to the start
    obj_manager.add_column_to_start()
    
    # Expected grid after adding column to start:
    # · a a · b b b
    # · a a 1 1 1 1
    # · · 0 · · · 1
    # · · 0 0 0 · 1
    # · · · · c c 1
    
    grid = obj_manager.make_grid()
    assert grid.width == 7  # Original width (6) + 1
    assert grid.height == 5  # Height unchanged
    
    # Verify the new column is empty
    for row in range(grid.height):
        assert grid.is_cell_empty(row, 0)
    
    # Verify existing content is shifted right
    assert grid.cells[0][1].value == "a"  # Was at (0,0)
    assert grid.cells[0][4].value == "b"  # Was at (0,3)
    assert grid.cells[4][4].value == "c"  # Was at (4,3)
    
    # Verify node positions are updated
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    assert node_a.col == 1  # Was 0
    node_b = next(node for node in obj_manager.nodes if node.id == 'b')
    assert node_b.col == 4  # Was 3
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    assert node_c.col == 4  # Was 3 