import os
import pytest
from src.classes.grid import Grid

def test_correct_count_of_node_placement_cells():
    # Get the path to the test text file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    txt_path = os.path.join(data_dir, 'two-spots-for-adding-node.txt')
    
    # Load the text file
    with open(txt_path, 'r') as f:
        txt_data = f.read()
    
    # Create grid from text
    grid = Grid.create_from_txt(txt_data)
    
    # Print the grid
    print('Grid:')
    print(grid.export_to_txt())
    
    # Print all empty cells
    empty_cells = grid.get_all_empty_cells()
    print('Empty cells:', empty_cells)
    
    # Get valid node placement cells
    valid_cells = grid.get_all_valid_node_placement_cells()
    valid_coords = []
    for row in range(grid.height):
        for col in range(grid.width):
            if grid.cells[row][col] in valid_cells:
                valid_coords.append((row, col))
    print('Valid node placement cells:', valid_coords)
    
    # Verify we have exactly 2 valid cells
    assert len(valid_cells) == 2, f"Expected 2 valid node placement cells, but got {len(valid_cells)}"
