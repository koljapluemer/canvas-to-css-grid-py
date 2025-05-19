from typing import Literal
from models.edge import Edge
from models.node import Node

class Cell:
    content: any
    row: int
    column: int

    def render(self) -> str:
        return "·"


class NodeCell(Cell):
    node: Node

    def render(self) -> str:
        return self.node.content


class EdgeCell(Cell):
    edge: Edge

    hasNorthConnection: bool
    hasEastConnection: bool
    hasSouthConnection: bool
    hasWestConnection: bool

    hasNorthArrow: bool
    hasEastArrow: bool
    hasSouthArrow: bool
    hasWestArrow: bool

    # use unicode arrows like
    # ↑ → ↓ ← ┐ ┌ ┘ └ ┬ ┴ ┤ ├ and so on
    # check first purely for edges, then replace with same symbol with arrowhead if needed
    def render(self) -> str:
        # First determine the basic edge shape
        if self.hasNorthConnection and self.hasSouthConnection:
            if self.hasEastConnection and self.hasWestConnection:
                base_char = "┼"  # Cross
            elif self.hasEastConnection:
                base_char = "├"  # T pointing right
            elif self.hasWestConnection:
                base_char = "┤"  # T pointing left
            else:
                base_char = "│"  # Vertical line
        elif self.hasEastConnection and self.hasWestConnection:
            if self.hasNorthConnection:
                base_char = "┴"  # T pointing up
            elif self.hasSouthConnection:
                base_char = "┬"  # T pointing down
            else:
                base_char = "─"  # Horizontal line
        elif self.hasNorthConnection and self.hasEastConnection:
            base_char = "└"  # Corner
        elif self.hasNorthConnection and self.hasWestConnection:
            base_char = "┘"  # Corner
        elif self.hasSouthConnection and self.hasEastConnection:
            base_char = "┌"  # Corner
        elif self.hasSouthConnection and self.hasWestConnection:
            base_char = "┐"  # Corner
        else:
            return "·"  # No connections

        # Add arrowheads where needed
        if base_char == "─":  # Horizontal line
            if self.hasEastArrow and self.hasWestArrow:
                return "↔"
            elif self.hasEastArrow:
                return "→"
            elif self.hasWestArrow:
                return "←"
        elif base_char == "│":  # Vertical line
            if self.hasNorthArrow and self.hasSouthArrow:
                return "↕"
            elif self.hasNorthArrow:
                return "↑"
            elif self.hasSouthArrow:
                return "↓"
        elif base_char == "└":  # Corner
            if self.hasNorthArrow:
                return "⬑"
            elif self.hasEastArrow:
                return "⬏"
        elif base_char == "┘":  # Corner
            if self.hasNorthArrow:
                return "⬏"
            elif self.hasWestArrow:
                return "⬑"
        elif base_char == "┌":  # Corner
            if self.hasSouthArrow:
                return "⬏"
            elif self.hasEastArrow:
                return "⬑"
        elif base_char == "┐":  # Corner
            if self.hasSouthArrow:
                return "⬑"
            elif self.hasWestArrow:
                return "⬏"

        return base_char


    
    
    
    
    
    
    