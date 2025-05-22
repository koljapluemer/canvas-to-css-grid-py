import os
import pytest
from src.classes.grid import Grid

def test_create_from_txt():
    # Get the path to the test TXT file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(current_dir, 'simplegrid.txt')
    
    # Load the TXT file
    with open(txt_path, 'r') as f:
        txt_data = f.read()
    
    # Create Grid from TXT
    grid = Grid.create_from_txt(txt_data)
    
    # Verify the grid dimensions
    assert grid.height == 5, "Expected grid height to be 5"
    assert grid.width == 6, "Expected grid width to be 6"
