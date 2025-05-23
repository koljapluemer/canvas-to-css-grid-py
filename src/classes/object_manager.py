from src.classes.grid import Grid
from src.classes.node import Node
from src.classes.edge import Edge, Attachment
from src.classes.coordinate import Coordinate
from src.classes.cell import Cell, CellType, Direction

class ObjectManager:
    def __init__(self):
        self.nodes = []
        self.edges = []

    @staticmethod
    def create_from_JSON(json_data):
        obj_manager = ObjectManager()
        for node_data in json_data.get('nodes', []):
            node = Node(**node_data)
            obj_manager.add_node(node)
        for edge_data in json_data.get('edges', []):
            cells = [Coordinate(row=cell[0], col=cell[1]) for cell in edge_data['cells']]
            sender_attachment = Attachment(
                node_id=edge_data['senderAttachment']['nodeId'],
                has_arrow=edge_data['senderAttachment']['hasArrow'],
                node_in_direction=edge_data['senderAttachment']['nodeInDirection']
            )
            receiver_attachment = Attachment(
                node_id=edge_data['receiverAttachment']['nodeId'],
                has_arrow=edge_data['receiverAttachment']['hasArrow'],
                node_in_direction=edge_data['receiverAttachment']['nodeInDirection']
            )
            edge = Edge(
                id=edge_data['id'],
                sender_attachment=sender_attachment,
                receiver_attachment=receiver_attachment,
                cells=cells
            )
            obj_manager.add_edge(edge)
        return obj_manager
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def create_needed_grid_format(self) -> tuple[int, int]:
        max_row = 0
        max_col = 0
        # Check nodes
        for node in self.nodes:
            max_row = max(max_row, node.row + node.height)
            max_col = max(max_col, node.col + node.width)
        # Check edge cells
        for edge in self.edges:
            for cell in edge.cells:
                max_row = max(max_row, cell.row + 1)
                max_col = max(max_col, cell.col + 1)
        return (max_row, max_col)

    def export_to_JSON(self):
        nodes_json = [
            {
                'id': node.id,
                'row': node.row,
                'col': node.col,
                'width': node.width,
                'height': node.height
            }
            for node in self.nodes
        ]
        edges_json = [
            {
                'id': edge.id,
                'senderAttachment': {
                    'nodeId': edge.sender_attachment.node_id,
                    'hasArrow': edge.sender_attachment.has_arrow,
                    'nodeInDirection': edge.sender_attachment.node_in_direction
                },
                'receiverAttachment': {
                    'nodeId': edge.receiver_attachment.node_id,
                    'hasArrow': edge.receiver_attachment.has_arrow,
                    'nodeInDirection': edge.receiver_attachment.node_in_direction
                },
                'cells': [
                    [cell.row, cell.col] for cell in edge.cells
                ]
            }
            for edge in self.edges
        ]
        return {'nodes': nodes_json, 'edges': edges_json}

    def make_grid(self) -> Grid:
        height, width = self.create_needed_grid_format()
        grid = Grid(width=width, height=height)
        # Fill nodes
        for node in self.nodes:
            for r in range(node.row, node.row + node.height):
                for c in range(node.col, node.col + node.width):
                    cell = Cell(r, c, CellType.NODE, None, None, False, False, value="·", occupant_id=node.id)
                    grid.cells[r][c] = cell
        # Fill edges
        for edge in self.edges:
            for i, cell in enumerate(edge.cells):
                r, c = cell.row, cell.col
                if i == 0:
                    # First cell: connects to sender node
                    connects_to_previous_in_direction = Direction[edge.sender_attachment.node_in_direction]
                    has_arrow_to_previous = edge.sender_attachment.has_arrow
                    # Connect to next cell in edge
                    next_cell = edge.cells[i + 1]
                    connects_to_next_in_direction = self._compute_direction(r, c, next_cell.row, next_cell.col)
                    has_arrow_to_next = False
                elif i == len(edge.cells) - 1:
                    # Last cell: connects to receiver node
                    connects_to_next_in_direction = Direction[edge.receiver_attachment.node_in_direction]
                    has_arrow_to_next = edge.receiver_attachment.has_arrow
                    # Connect to previous cell in edge
                    prev_cell = edge.cells[i - 1]
                    connects_to_previous_in_direction = self._compute_direction(r, c, prev_cell.row, prev_cell.col)
                    has_arrow_to_previous = False
                else:
                    # Middle cell: connects to both previous and next cells
                    prev_cell = edge.cells[i - 1]
                    next_cell = edge.cells[i + 1]
                    connects_to_previous_in_direction = self._compute_direction(r, c, prev_cell.row, prev_cell.col)
                    connects_to_next_in_direction = self._compute_direction(r, c, next_cell.row, next_cell.col)
                    has_arrow_to_previous = False
                    has_arrow_to_next = False
                edge_cell = Cell(
                    r, c, CellType.EDGE,
                    connects_to_previous_in_direction, connects_to_next_in_direction,
                    has_arrow_to_previous, has_arrow_to_next,
                    value="·", occupant_id=str(edge.id)
                )
                grid.cells[r][c] = edge_cell
        return grid

    def _compute_direction(self, r1: int, c1: int, r2: int, c2: int) -> Direction:
        if r1 < r2:
            return Direction.S
        elif r1 > r2:
            return Direction.N
        elif c1 < c2:
            return Direction.E
        elif c1 > c2:
            return Direction.W
        else:
            raise ValueError("Cells are the same")

    def add_node_at_coordinate(self, id, row, col):
        from src.classes.node import Node
        self.add_node(Node(id=id, row=row, col=col, width=1, height=1))

    def add_node_at_valid_spot(self, id):
        grid = self.make_grid()
        coord = grid.get_random_valid_node_placement_cell()
        if coord is None:
            raise ValueError("No valid placement for new node")
        row, col = coord
        self.add_node_at_coordinate(id, row, col)

    def add_row_to_start(self):
        # Increment row of all nodes
        for node in self.nodes:
            node.row += 1
        
        # Increment row of all edge cells
        for edge in self.edges:
            for cell in edge.cells:
                cell.row += 1

    def add_col_to_start(self):
        # Increment column of all nodes
        for node in self.nodes:
            node.col += 1
        
        # Increment column of all edge cells
        for edge in self.edges:
            for cell in edge.cells:
                cell.col += 1

    def get_neighboring_cell_coords(self, node) -> list[tuple[int, int]]:
        """Return all orthogonal (N, S, E, W) coordinates around the node (may be out of bounds)."""
        coords = set()
        # Top (N)
        for c in range(node.col, node.col + node.width):
            coords.add((node.row - 1, c))
        # Bottom (S)
        for c in range(node.col, node.col + node.width):
            coords.add((node.row + node.height, c))
        # Left (W)
        for r in range(node.row, node.row + node.height):
            coords.add((r, node.col - 1))
        # Right (E)
        for r in range(node.row, node.row + node.height):
            coords.add((r, node.col + node.width))
        return list(coords)

    def find_all_empty_neighbors(self, node) -> list[tuple[int, int]]:
        """Find all empty cells that are direct neighbors of a node."""
        grid = self.make_grid()
        neighbors = self.get_neighboring_cell_coords(node)
        return [coord for coord in neighbors if 0 <= coord[0] < grid.height and 0 <= coord[1] < grid.width and grid.is_cell_empty(coord[0], coord[1])]

    def get_valid_attachment_points(self, node) -> list[tuple[int, int]]:
        """Get all valid attachment points for a node.
        
        A valid attachment point must:
        1. Be an empty cell adjacent to the node (orthogonal only)
        2. Have another empty cell in the same direction for "breathing space"
        """
        grid = self.make_grid()
        valid_points = set()
        # North edge
        r = node.row - 1
        if r >= 0:
            for c in range(node.col, node.col + node.width):
                if grid.is_cell_empty(r, c):
                    breathing_r = r - 1
                    if breathing_r >= 0 and grid.is_cell_empty(breathing_r, c):
                        valid_points.add((r, c))
        # South edge
        r = node.row + node.height
        if r < grid.height:
            for c in range(node.col, node.col + node.width):
                if grid.is_cell_empty(r, c):
                    breathing_r = r + 1
                    if breathing_r < grid.height and grid.is_cell_empty(breathing_r, c):
                        valid_points.add((r, c))
        # West edge
        c = node.col - 1
        if c >= 0:
            for r in range(node.row, node.row + node.height):
                if grid.is_cell_empty(r, c):
                    breathing_c = c - 1
                    if breathing_c >= 0 and grid.is_cell_empty(r, breathing_c):
                        valid_points.add((r, c))
        # East edge
        c = node.col + node.width
        if c < grid.width:
            for r in range(node.row, node.row + node.height):
                if grid.is_cell_empty(r, c):
                    breathing_c = c + 1
                    if breathing_c < grid.width and grid.is_cell_empty(r, breathing_c):
                        valid_points.add((r, c))
        return list(valid_points)