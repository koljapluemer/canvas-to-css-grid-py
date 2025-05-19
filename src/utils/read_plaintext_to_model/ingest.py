from models.meta_grid import MetaGrid
from models.grid import Grid
from models.node import Node
from models.edge import Edge
from models.cells import Cell, NodeCell, EdgeCell

def ingest(text: str) -> tuple[MetaGrid, Grid]:
    # Split input into lines and create 2D grid
    lines = text.strip().split('\n')
    char_grid = [[char for char in line.split()] for line in lines]
    
    # Initialize structures
    nodes: list[Node] = []
    edges: list[Edge] = []
    cell_grid: list[list[Cell]] = []
    
    # First pass: identify nodes and create NodeCells
    node_map = {}  # Maps node content to Node object
    for row_idx, row in enumerate(char_grid):
        cell_row = []
        for col_idx, char in enumerate(row):
            if char == '.':
                cell_row.append(Cell())
            elif char.isalnum():  # This is a node character
                if char not in node_map:
                    node = Node(char, [])
                    node_map[char] = node
                    nodes.append(node)
                node_cell = NodeCell()
                node_cell.node = node_map[char]
                node_cell.row = row_idx
                node_cell.column = col_idx
                node_map[char].cells.append(node_cell)
                cell_row.append(node_cell)
            else:
                cell_row.append(Cell())  # Placeholder for now
        cell_grid.append(cell_row)
    
    # Second pass: identify edges and create EdgeCells
    for row_idx, row in enumerate(char_grid):
        for col_idx, char in enumerate(row):
            if char in ['→', '←', '↑', '↓']:
                # Find connected nodes
                origin = None
                destination = None
                if char == '→':
                    # Look left for origin, right for destination
                    for i in range(col_idx-1, -1, -1):
                        if isinstance(cell_grid[row_idx][i], NodeCell):
                            origin = cell_grid[row_idx][i].node
                            break
                    for i in range(col_idx+1, len(row)):
                        if isinstance(cell_grid[row_idx][i], NodeCell):
                            destination = cell_grid[row_idx][i].node
                            break
                elif char == '←':
                    # Look right for origin, left for destination
                    for i in range(col_idx+1, len(row)):
                        if isinstance(cell_grid[row_idx][i], NodeCell):
                            origin = cell_grid[row_idx][i].node
                            break
                    for i in range(col_idx-1, -1, -1):
                        if isinstance(cell_grid[row_idx][i], NodeCell):
                            destination = cell_grid[row_idx][i].node
                            break
                
                if origin and destination:
                    edge_cell = EdgeCell()
                    edge_cell.edge = Edge(origin, destination, [], False, True, None)
                    edge_cell.row = row_idx
                    edge_cell.column = col_idx
                    
                    # Set arrow properties based on direction
                    if char == '→':
                        edge_cell.hasEastArrow = True
                        edge_cell.hasEastConnection = True
                        edge_cell.hasWestConnection = True
                    elif char == '←':
                        edge_cell.hasWestArrow = True
                        edge_cell.hasEastConnection = True
                        edge_cell.hasWestConnection = True
                    elif char == '↑':
                        edge_cell.hasNorthArrow = True
                        edge_cell.hasNorthConnection = True
                        edge_cell.hasSouthConnection = True
                    elif char == '↓':
                        edge_cell.hasSouthArrow = True
                        edge_cell.hasNorthConnection = True
                        edge_cell.hasSouthConnection = True
                    
                    edge_cell.edge.cells.append(edge_cell)
                    edges.append(edge_cell.edge)
                    cell_grid[row_idx][col_idx] = edge_cell
    
    # Create and return both structures
    meta_grid = MetaGrid(edges, nodes)
    grid = Grid(cell_grid)
    return meta_grid, grid
