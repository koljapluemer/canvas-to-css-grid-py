from typing import TYPE_CHECKING, Literal, List, Dict, Tuple
from models.interfaces import Renderable

if TYPE_CHECKING:
    from models.edge import Edge
    from models.node import Node

class Cell(Renderable):
    content: any
    row: int
    column: int

    def render(self) -> str:
        return "."


class NodeCell(Cell):
    node: 'Node'

    def render(self) -> str:
        return self.node.content


class EdgeCell(Cell):
    edge: 'Edge'

    hasNorthConnection: bool
    hasEastConnection: bool
    hasSouthConnection: bool
    hasWestConnection: bool

    hasNorthArrow: bool
    hasEastArrow: bool
    hasSouthArrow: bool
    hasWestArrow: bool

    def __init__(self):
        super().__init__()
        self.hasNorthConnection = False
        self.hasEastConnection = False
        self.hasSouthConnection = False
        self.hasWestConnection = False
        self.hasNorthArrow = False
        self.hasEastArrow = False
        self.hasSouthArrow = False
        self.hasWestArrow = False

    # Mapping of connection patterns to their base symbols
    CONNECTION_PATTERNS: Dict[Tuple[bool, bool, bool, bool], str] = {
        # (north, east, south, west)
        (True, True, True, True): "┼",    # Cross
        (True, True, True, False): "├",   # T pointing right
        (True, False, True, True): "┤",   # T pointing left
        (True, False, True, False): "│",  # Vertical line
        (False, True, False, True): "─",  # Horizontal line
        (True, True, False, False): "└",  # Corner
        (True, False, False, True): "┘",  # Corner
        (False, True, True, False): "┌",  # Corner
        (False, False, True, True): "┐",  # Corner
    }

    # Mapping of arrow patterns to their symbols
    ARROW_PATTERNS: Dict[Tuple[bool, bool, bool, bool], Dict[str, str]] = {
        # (north, east, south, west) -> {base_symbol: arrow_symbol}
        (False, True, False, True): {  # Horizontal line
            "─": "↔",
            "→": "→",
            "←": "←"
        },
        (True, False, True, False): {  # Vertical line
            "│": "↕",
            "↑": "↑",
            "↓": "↓"
        },
        (True, True, False, False): {  # Corner
            "└": "⬑",
            "⬏": "⬏"
        },
        (True, False, False, True): {  # Corner
            "┘": "⬏",
            "⬑": "⬑"
        },
        (False, True, True, False): {  # Corner
            "┌": "⬏",
            "⬑": "⬑"
        },
        (False, False, True, True): {  # Corner
            "┐": "⬑",
            "⬏": "⬏"
        }
    }

    @classmethod
    def from_symbol(cls, symbol: str) -> Tuple[bool, bool, bool, bool, bool, bool, bool, bool]:
        """Convert a symbol back to connection and arrow states."""
        # First find the base pattern
        for (n, e, s, w), base_symbol in cls.CONNECTION_PATTERNS.items():
            if symbol == base_symbol:
                return (n, e, s, w, False, False, False, False)
            
            # Check arrow patterns
            if (n, e, s, w) in cls.ARROW_PATTERNS:
                for arrow_symbol in cls.ARROW_PATTERNS[(n, e, s, w)].values():
                    if symbol == arrow_symbol:
                        # Determine arrow directions based on the symbol
                        has_north = n and symbol in ["↑", "⬑", "⬏"]
                        has_east = e and symbol in ["→", "⬑", "⬏"]
                        has_south = s and symbol in ["↓", "⬑", "⬏"]
                        has_west = w and symbol in ["←", "⬑", "⬏"]
                        return (n, e, s, w, has_north, has_east, has_south, has_west)
        
        return (False, False, False, False, False, False, False, False)

    def render(self) -> str:
        # Get the base symbol based on connections
        connections = (
            self.hasNorthConnection,
            self.hasEastConnection,
            self.hasSouthConnection,
            self.hasWestConnection
        )
        
        base_symbol = self.CONNECTION_PATTERNS.get(connections, "·")
        
        # If no connections, return the dot
        if base_symbol == "·":
            return base_symbol
            
        # Check for arrow patterns
        if connections in self.ARROW_PATTERNS:
            arrow_patterns = self.ARROW_PATTERNS[connections]
            
            # Check for bidirectional arrows first
            if (self.hasEastArrow and self.hasWestArrow and base_symbol == "─"):
                return "↔"
            if (self.hasNorthArrow and self.hasSouthArrow and base_symbol == "│"):
                return "↕"
                
            # Check for single direction arrows
            if self.hasEastArrow and base_symbol == "─":
                return "→"
            if self.hasWestArrow and base_symbol == "─":
                return "←"
            if self.hasNorthArrow and base_symbol == "│":
                return "↑"
            if self.hasSouthArrow and base_symbol == "│":
                return "↓"
                
            # Check for corner arrows
            if self.hasNorthArrow and base_symbol == "└":
                return "⬑"
            if self.hasEastArrow and base_symbol == "└":
                return "⬏"
            if self.hasNorthArrow and base_symbol == "┘":
                return "⬏"
            if self.hasWestArrow and base_symbol == "┘":
                return "⬑"
            if self.hasSouthArrow and base_symbol == "┌":
                return "⬏"
            if self.hasEastArrow and base_symbol == "┌":
                return "⬑"
            if self.hasSouthArrow and base_symbol == "┐":
                return "⬑"
            if self.hasWestArrow and base_symbol == "┐":
                return "⬏"
        
        return base_symbol


    
    
    
    
    
    
    