from enum import Enum

class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

class CellType(Enum):
    EMPTY = "EMPTY"
    NODE = "NODE"
    EDGE = "EDGE"

class Cell:
    def __init__(self, row: int, col: int, cell_type: CellType, connectsToPreviousInDirection: Direction, connectsToNextInDirection: Direction, hasArrowToPrevious: bool, hasArrowToNext: bool):
        self.value = "·"  # Default empty cell value
        self.row = row
        self.col = col
        self.cell_type = cell_type
        self.connects_to_previous_in_direction = connects_to_previous_in_direction
        self.connects_to_next_in_direction = connects_to_next_in_direction
        self.has_arrow_to_previous = has_arrow_to_previous
        self.has_arrow_to_next = has_arrow_to_next



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

    def render_flow(self) -> str:
        if self.cell_type == CellType.EMPTY:
            return "·"
        elif self.cell_type == CellType.NODE:
            return "O"
        elif self.cell_type == CellType.EDGE:
            if self.has_arrow_to_previous:
                if self.connects_to_previous_in_direction == Direction.N:
                    return "↑"
                elif self.connects_to_previous_in_direction == Direction.E:
                    return "→"
                elif self.connects_to_previous_in_direction == Direction.S:
                    return "↓"
                elif self.connects_to_previous_in_direction == Direction.W:
                    return "←"
            elif self.has_arrow_to_next:
                if self.connects_to_next_in_direction == Direction.N:
                    return "↑"
                elif self.connects_to_next_in_direction == Direction.E:
                    return "→"
                elif self.connects_to_next_in_direction == Direction.S:
                    return "↓"
                elif self.connects_to_next_in_direction == Direction.W:
                    return "←"
            else:
                # Straight edges
                # E + W: —
                if self.connects_to_previous_in_direction == Direction.E and self.connects_to_next_in_direction == Direction.W:
                    return "─"
                # N + S: │
                elif self.connects_to_previous_in_direction == Direction.N and self.connects_to_next_in_direction == Direction.S:
                    return "│"
                # Elbow connectors
                # N
                elif self.connects_to_previous_in_direction == Direction.N and self.connects_to_next_in_direction == Direction.E:
                    return "└"
                elif self.connects_to_previous_in_direction == Direction.N and self.connects_to_next_in_direction == Direction.W:
                    return "┘"
                # S
                elif self.connects_to_previous_in_direction == Direction.S and self.connects_to_next_in_direction == Direction.E:
                    return "┌"
                elif self.connects_to_previous_in_direction == Direction.S and self.connects_to_next_in_direction == Direction.W:
                    return "┐"
                # E
                elif self.connects_to_previous_in_direction == Direction.E and self.connects_to_next_in_direction == Direction.N:
                    return "└"
                elif self.connects_to_previous_in_direction == Direction.E and self.connects_to_next_in_direction == Direction.S:
                    return "┌"
                # W
                elif self.connects_to_previous_in_direction == Direction.W and self.connects_to_next_in_direction == Direction.N:
                    return "┘"
                elif self.connects_to_previous_in_direction == Direction.W and self.connects_to_next_in_direction == Direction.S:
                    return "┐"
                else:
                    return "X"
                    
