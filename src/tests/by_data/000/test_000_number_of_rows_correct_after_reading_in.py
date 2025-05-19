import pytest
from cell_grid import CellGrid

def test_number_of_rows_correct_after_reading_in():
    # Read the input file
    with open("src/tests/by_data/000/in.txt", "r") as f:
        grid_str = f.read()
    
    # Create grid from string
    grid = CellGrid.from_string(grid_str)
    
    # Verify number of rows
    assert len(grid.cells) == 2  # in.txt has 2 rows: "ab" and "cd" 