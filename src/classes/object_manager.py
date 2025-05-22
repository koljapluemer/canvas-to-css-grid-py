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
