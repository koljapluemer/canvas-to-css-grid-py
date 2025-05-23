from enum import Enum

class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"


class Cell:
    def __init__(self, row: int, col: int):
        self.value = "·"  # Default empty cell value
        self.row = row
        self.col = col

# implement the doomed arrows


# ─
# │
# ┌
# ┐ 
# └ 
# ┘
# ←
# ↑
# →
# ↓
# ┼