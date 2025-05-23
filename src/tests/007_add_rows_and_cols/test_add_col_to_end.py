import os
import pytest
from src.classes.grid import Grid

def test_add_col_to_end():
    # Get paths to test files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(current_dir, 'base.txt')
    expected_path = os.path.join(current_dir, 'result_add_col_to_end.txt')
    
    # Load initial state
    with open(base_path, 'r') as f:
        base_data = f.read()
    
    # Create grid from base.txt
    grid = Grid.create_from_txt(base_data)
    
    # Add column to end
    grid.add_col_to_end()
    
    # Verify final state matches result_add_col_to_end.txt
    with open(expected_path, 'r') as f:
        expected = f.read().strip()
    actual = grid.export_to_txt()
    assert actual == expected, "Grid after adding column does not match expected result"
