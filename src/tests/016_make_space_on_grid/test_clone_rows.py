import pytest
import os
import json
from src.classes.object_manager import ObjectManager

def load_base_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'simplegrid.json'), 'r') as f:
        return ObjectManager.create_from_JSON(json.load(f))

def test_clone_row():
    """Test cloning a row that contains vertical edge cells without arrows"""
    obj_manager = load_base_state()
    
    # Add some vertical edges to make a row clonable
    # First, add a node that we can connect to
    obj_manager.add_node_at_coordinate("d", 3, 6)
    
    # Then add an edge with vertical segments
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    node_d = next(node for node in obj_manager.nodes if node.id == 'd')
    obj_manager.draw_edge(
        sender_node=node_a,
        receiver_node=node_d,
        sender_attachment_point=(2, 1),
        receiver_attachment_point=(3, 5),
        has_arrow_sender=False,
        has_arrow_receiver=False
    )
    
    # Now clone the row with vertical edges
    obj_manager.clone_row(2)  # Clone row 2 which should have vertical edges
    
    grid = obj_manager.make_grid()
    assert grid.height == 6  # Original height (5) + 1
    
    # Verify the cloned row is identical to the original
    for col in range(grid.width):
        assert grid.cells[2][col].value == grid.cells[3][col].value
        if grid.cells[2][col].type == "EDGE":
            assert grid.cells[2][col].connects_to_previous_in_direction == grid.cells[3][col].connects_to_previous_in_direction
            assert grid.cells[2][col].connects_to_next_in_direction == grid.cells[3][col].connects_to_next_in_direction
            assert grid.cells[2][col].has_arrow_to_previous == grid.cells[3][col].has_arrow_to_previous
            assert grid.cells[2][col].has_arrow_to_next == grid.cells[3][col].has_arrow_to_next
    
    # Verify edge cells are updated
    edge = next(edge for edge in obj_manager.edges if edge.id == "2")
    assert len(edge.cells) == 5  # Original 4 cells + 1 from cloning
    assert edge.cells[2].row == 3  # The new cell should be in the cloned row

def test_cannot_clone_row_with_arrow():
    """Test that a row cannot be cloned if it contains an edge cell with an arrow"""
    obj_manager = load_base_state()
    
    # Add an edge with an arrow in a row
    node_a = next(node for node in obj_manager.nodes if node.id == 'a')
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    obj_manager.draw_edge(
        sender_node=node_a,
        receiver_node=node_c,
        sender_attachment_point=(2, 1),
        receiver_attachment_point=(6, 3),
        has_arrow_sender=True,  # Add an arrow
        has_arrow_receiver=False
    )
    
    # Try to clone the row with the arrow
    with pytest.raises(ValueError, match="Cannot clone row: contains edge cell with arrow"):
        obj_manager.clone_row(2) 