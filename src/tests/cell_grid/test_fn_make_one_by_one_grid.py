import pytest
from cell_grid import CellGrid

def test_make_one_by_one_grid():
    # Create a 1x1 grid
    grid = CellGrid.make_one_by_one_grid()
    
    # Check that the grid has exactly one row
    assert len(grid.cells) == 1
    
    # Check that the row has exactly one cell
    assert len(grid.cells[0]) == 1
    
    # Check that the cell is empty
    assert grid.cells[0][0] == "empty"
    
    # Check that the grid renders correctly
    assert grid.render() == "·"
