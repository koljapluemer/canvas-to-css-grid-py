# attachmentpoint sender: "b", [1, 5]
# attachmentpoint receiver: "c", [6, 5]

import os
import pytest
import json
from src.classes.object_manager import ObjectManager

def test_find_path_from_b_to_c():
    # Load base.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_json_path = os.path.join(current_dir, 'base.json')
    with open(base_json_path, 'r') as f:
        obj_manager = ObjectManager.create_from_JSON(json.load(f))
    
    # Get nodes
    node_b = next(node for node in obj_manager.nodes if node.id == 'b')
    node_c = next(node for node in obj_manager.nodes if node.id == 'c')
    
    # Draw edge from b to c using specified attachment points
    obj_manager.draw_edge(
        sender_node=node_b,
        receiver_node=node_c,
        sender_attachment_point=(1, 5),  # South edge of b
        receiver_attachment_point=(6, 5),  # North edge of c
        has_arrow_sender=False,
        has_arrow_receiver=False
    )
    
    # Get expected output
    expected_txt_path = os.path.join(current_dir, 'txt_after_b_to_c.txt')
    with open(expected_txt_path, 'r') as f:
        expected_txt = f.read().strip()
    
    # Get actual output
    actual_txt = obj_manager.make_grid().export_to_txt()
    
    # Compare text output
    assert actual_txt == expected_txt, f"Grid after drawing edge does not match expected output.\nExpected:\n{expected_txt}\nGot:\n{actual_txt}"
    
    # Compare JSON output
    expected_json_path = os.path.join(current_dir, 'after_b_to_c.json')
    with open(expected_json_path, 'r') as f:
        expected_json = json.load(f)
    
    actual_json = obj_manager.export_to_JSON()
    
    # Compare JSON structures
    assert actual_json == expected_json, f"JSON export does not match expected output.\nExpected:\n{json.dumps(expected_json, indent=4)}\nGot:\n{json.dumps(actual_json, indent=4)}"

