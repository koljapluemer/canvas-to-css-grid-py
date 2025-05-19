import pytest
from cell_grid import CellGrid

def test_number_of_nodes_correct_after_reading_in():
    # Read the input file
    with open("src/tests/by_data/000/in.txt", "r") as f:
        grid_str = f.read()
    
    # Create grid from string
    grid = CellGrid.from_string(grid_str)
    
    # Verify number of nodes
    assert len(grid.nodes) == 4  # in.txt has 4 nodes: a, b, c, d
    
    # Verify node contents
    node_contents = {node.content for node in grid.nodes}
    assert node_contents == {'a', 'b', 'c', 'd'}
