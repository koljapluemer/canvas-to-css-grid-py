from src.classes.grid import Grid
from src.classes.node import Node
from src.classes.edge import Edge
from src.classes.coordinate import Coordinate

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
            edge = Edge(
                id=edge_data['id'],
                senderId=edge_data['senderId'],
                receiverId=edge_data['receiverId'],
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
                'senderId': edge.senderId,
                'receiverId': edge.receiverId,
                'cells': [
                    {'row': cell.row, 'col': cell.col} for cell in edge.cells
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
                    grid.cells[r][c].value = node.id
        # Fill edges
        for edge in self.edges:
            for cell in edge.cells:
                grid.cells[cell.row][cell.col].value = edge.id
        return grid

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