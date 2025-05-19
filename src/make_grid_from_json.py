"""
## Goal: Take an Open Canvas JSON file and convert it to a CellGrid

- utilize pyjsoncanvas to read the JSON file

(for now, we just render nodes, not edges)

### How to treat Nodes

1. create a CellGrid with 1x1, empty (there's a function for that)
2. start the following loop until all nodes placed:
    a. Pick an *random* node that is not yet in the CellGrid
    b. Place it via the function in the CellGrid
3. render the grid

"""
import random
from pyjsoncanvas import Canvas
from cell_grid import CellGrid

def make_grid_from_json(json_path: str) -> CellGrid:
    # 1. Create initial empty grid
    grid = CellGrid.make_one_by_one_grid()
    
    # Load the canvas using PyJSONCanvas
    with open(json_path, 'r') as f:
        canvas = Canvas.from_json(f.read())
    
    # Get all nodes that need to be placed
    nodes_to_place = list(canvas.nodes)
    
    # 2. Place nodes randomly until all are placed
    while nodes_to_place:
        # Pick a random node
        node = random.choice(nodes_to_place)
        nodes_to_place.remove(node)
        
        # Extract node content based on node type
        if hasattr(node, 'file'):
            node_content = node.file
        elif hasattr(node, 'text'):
            node_content = node.text
        else:
            node_content = str(node.id)  # fallback to node ID if no content
        
        # Place the node in the grid
        grid.add_node_at_random_empty_cell(node_content)
    
    return grid

if __name__ == "__main__":
    # Example usage
    json_path = "data/json-diagrams/simple.canvas"
    grid = make_grid_from_json(json_path)
    grid.purge_redundant_columns()
    grid.purge_redundant_rows()
    print("```")
    print(grid.render())
    print("```")