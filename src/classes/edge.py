from dataclasses import dataclass
from typing import List
from src.classes.coordinate import Coordinate

@dataclass
class Attachment:
    node_id: str
    has_arrow: bool
    node_in_direction: str

@dataclass
class Edge:
    id: str
    sender_attachment: Attachment
    receiver_attachment: Attachment
    cells: List[Coordinate]  # List of coordinates

    def __init__(self, id, sender_attachment, receiver_attachment, cells):
        self.id = id
        self.sender_attachment = sender_attachment
        self.receiver_attachment = receiver_attachment
        self.cells = cells

class Attachment:
    def __init__(self, node_id, has_arrow, node_in_direction):
        self.node_id = node_id
        self.has_arrow = has_arrow
        self.node_in_direction = node_in_direction
