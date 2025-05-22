import pytest
from cell_grid import CellGrid

def test_from_string_simple():
    grid_str = """
    aa→b·
    ····c
    """
    grid = CellGrid.from_string(grid_str)
    
    # Check grid dimensions
    assert len(grid.cells) == 2
    assert len(grid.cells[0]) == 5
    
    # Check cell contents
    assert grid.cells[0][0] == "node"  # a
    assert grid.cells[0][1] == "node"  # a
    assert grid.cells[0][2] == "edge-E_W"  # →
    assert grid.cells[0][3] == "node"  # b
    assert grid.cells[0][4] == "empty"  # ·
    assert grid.cells[1][4] == "node"  # c
    
    # Check nodes
    assert len(grid.nodes) == 3  # a, b, and c nodes
    
    # Check node 'a' properties
    node_a = next(n for n in grid.nodes if n.content == 'a')
    assert node_a.row == 0
    assert node_a.col == 0
    assert node_a.width == 2
    assert node_a.height == 1

def test_from_string_invalid_node_shape():
    grid_str = """
    aaa
    a·a
    aaa
    """
    with pytest.raises(ValueError, match="Node 'a' is not a solid rectangle"):
        CellGrid.from_string(grid_str)

def test_from_string_multiple_nodes_same_letter():
    grid_str = """
    aaa→b
    ···→·
    aaa→c
    """
    with pytest.raises(ValueError, match="Node 'a' is not a solid rectangle"):
        CellGrid.from_string(grid_str)

def test_from_string_multiline_node():
    grid_str = """
    aaa→b
    aaa··
    ····c
    """
    grid = CellGrid.from_string(grid_str)
    
    # Check node 'a' properties
    node_a = next(n for n in grid.nodes if n.content == 'a')
    assert node_a.row == 0
    assert node_a.col == 0
    assert node_a.width == 3
    assert node_a.height == 2 