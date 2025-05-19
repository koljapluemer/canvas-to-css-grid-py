from models.node import Node
from models.cells import Cell

class Edge:
    origin: Node
    destination: Node
    cells: list[Cell]
    hasArrowAtOrigin: bool
    hasArrowAtDestination: bool
    label: str|None
    
    
    
    