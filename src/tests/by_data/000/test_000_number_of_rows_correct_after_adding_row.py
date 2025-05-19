import pytest
from cell_grid import CellGrid

def test_number_of_rows_correct_after_adding_row():
    # Read the input file
    with open("src/tests/by_data/000/in.txt", "r") as f:
        grid_str = f.read()
    
    # Create grid from string
    grid = CellGrid.from_string(grid_str)
    
    # Add a new empty row
    grid.add_empty_row_at_index(1)  # Add after first row
    
    # Verify number of rows increased by 1
    assert len(grid.cells) == 3  # Original 2 rows + 1 new row
    
    # Verify the new row is empty
    assert all(cell == "empty" for cell in grid.cells[1])
