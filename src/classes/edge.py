from dataclasses import dataclass
from typing import List
from src.classes.coordinate import Coordinate

@dataclass
class Attachment:
    nodeId: str
    hasArrow: bool
    nodeInDirection: str

@dataclass
class Edge:
    id: str
    senderAttachment: Attachment
    receiverAttachment: Attachment
    cells: List[Coordinate]  # List of coordinates
