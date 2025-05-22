from dataclasses import dataclass

@dataclass
class Node:
    id: str
    row: int
    col: int
    width: int
    height: int
