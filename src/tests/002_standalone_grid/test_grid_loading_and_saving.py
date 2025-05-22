import os
import pytest
from src.classes.grid import Grid

def test_grid_export_matches_input():
    # Get the path to the test TXT file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    txt_path = os.path.join(data_dir, 'simplegrid.txt')
    
    # Load the original TXT file
    with open(txt_path, 'r') as f:
        original_txt = f.read().strip()
    
    # Create Grid from TXT
    grid = Grid.create_from_txt(original_txt)
    
    # Export back to TXT
    exported_txt = grid.export_to_txt()
    
    # Compare the original and exported text
    assert exported_txt == original_txt, "Exported text does not match original text"
