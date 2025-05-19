from typing import TYPE_CHECKING, List
from models.interfaces import CellContainer, Connectable

if TYPE_CHECKING:
    from models.node import Node
    from models.cells import Cell

class Edge(CellContainer, Connectable):
    origin: 'Node'
    destination: 'Node'
    cells: List['Cell']
    hasArrowAtOrigin: bool
    hasArrowAtDestination: bool
    label: str|None
    
    def __init__(self, origin: 'Node', destination: 'Node', cells: List['Cell'], hasArrowAtOrigin: bool, hasArrowAtDestination: bool, label: str|None):
        self.origin = origin
        self.destination = destination
        self.cells = cells
        self.hasArrowAtOrigin = hasArrowAtOrigin
        self.hasArrowAtDestination = hasArrowAtDestination
        self.label = label

    def get_connections(self) -> List['Connectable']:
        return [self.origin, self.destination]
    
    