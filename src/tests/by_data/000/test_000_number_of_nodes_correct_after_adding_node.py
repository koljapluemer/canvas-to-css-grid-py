import pytest
from cell_grid import CellGrid

def test_number_of_nodes_correct_after_adding_node():
    # Read the input file
    with open("src/tests/by_data/000/in.txt", "r") as f:
        grid_str = f.read()
    
    # Create grid from string
    grid = CellGrid.from_string(grid_str)
    
    # Add a new node
    grid.add_node_at_random_empty_cell("e")
    
    # Verify number of nodes increased by 1
    assert len(grid.nodes) == 5  # Original 4 nodes + 1 new node
    
    # Verify node contents
    node_contents = {node.content for node in grid.nodes}
    assert node_contents == {'a', 'b', 'c', 'd', 'e'}
