from dataclasses import dataclass
from typing import List
from src.classes.coordinate import Coordinate

@dataclass
class Edge:
    id: str
    senderId: str
    receiverId: str
    cells: List[Coordinate]  # List of coordinates
