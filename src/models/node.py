from typing import TYPE_CHECKING, List
from models.interfaces import CellContainer, Connectable, Renderable

if TYPE_CHECKING:
    from models.cells import Cell

class Node(CellContainer, Connectable, Renderable):
    content: str
    cells: List['Cell']
    
    def __init__(self, content: str, cells: List['Cell']):
        self.content = content
        self.cells = cells

    def get_connections(self) -> List['Connectable']:
        # Get all edges connected to this node
        connections = []
        for cell in self.cells:
            if hasattr(cell, 'edge'):
                connections.append(cell.edge)
        return connections

    def render(self) -> str:
        return self.content
        
        
        
